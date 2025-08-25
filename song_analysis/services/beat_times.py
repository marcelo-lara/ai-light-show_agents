import librosa
import collections
import numpy as np

# Compatibility shim for NumPy deprecated aliases used by some dependencies
# (e.g., madmom uses np.float which was removed in recent NumPy versions).
# Map removed NumPy aliases (e.g., np.float) to built-ins at runtime.
# Use setattr in a loop to keep the code compact and reduce static analysis
# false-positives from direct attribute assignments.
_np_aliases = {'float': float, 'int': int, 'bool': bool, 'complex': complex}
for _name, _val in _np_aliases.items():
    if not hasattr(np, _name):
        try:
            setattr(np, _name, _val)
        except Exception:
            # If we can't set the attribute for any reason, continue.
            pass
# Compatibility shim: some third-party packages (e.g., madmom) still import
# MutableSequence from `collections` which was moved to `collections.abc` in
# recent Python versions. Provide the attribute on the `collections` module
# to avoid ImportError on Python 3.10+.
try:
    if not hasattr(collections, 'MutableSequence'):
        import collections.abc as _collections_abc
        try:
            setattr(collections, 'MutableSequence', _collections_abc.MutableSequence)
        except Exception:
            # If we cannot set the attribute for some reason, continue.
            pass
except Exception:
    pass

try:
    from BeatNet.BeatNet import BeatNet
except ModuleNotFoundError as e:
    import sys
    msg = (
        "A required package is missing for BeatNet (likely 'pyaudio').\n"
        "On Debian/Ubuntu install the PortAudio dev package and then install PyAudio:\n"
        "    sudo apt-get update && sudo apt-get install -y portaudio19-dev\n"
        "    pip install pyaudio\n"
        "If you're using a virtualenv, activate it before running pip."
    )
    print(msg, file=sys.stderr)
    raise


def create_safe_beatnet(model=1, mode='offline', inference_model='DBN', plot=None, thread=False, **kwargs):
    """Create a BeatNet instance and attach a safe DBN processor wrapper.

    The wrapper only modifies the processor instance attached to the
    BeatNet object (no changes to site-packages). It avoids calling
    ``np.asarray(results)[:,1]`` on a heterogeneous list by selecting the
    best HMM via scalar log-probabilities.
    """
    plot = plot or []
    bn = BeatNet(model, mode=mode, inference_model=inference_model, plot=plot, thread=thread, **kwargs)

    try:
        # Prepare reference to madmom's helper if available
        import madmom.features.downbeats as _mdb_mod
        _process_dbn_fn = getattr(_mdb_mod, '_process_dbn', None)
    except Exception:
        _process_dbn_fn = None

    try:
        proc = getattr(bn, 'estimator', None)
        if proc is not None and _process_dbn_fn is not None and hasattr(proc, 'process'):
            # Create a safe process method bound to the processor instance
            def _safe_process(self, activations, **kwargs):
                import itertools as _it
                import numpy as _np

                first = 0
                if self.threshold:
                    idx = _np.nonzero(activations >= self.threshold)[0]
                    if idx.any():
                        first = max(first, _np.min(idx))
                        last = min(len(activations), _np.max(idx) + 1)
                    else:
                        last = first
                    activ_ = activations[first:last]
                else:
                    activ_ = activations

                if not _np.any(activ_):
                    return _np.empty((0, 2))

                results = list(self.map(_process_dbn_fn, zip(self.hmms, _it.repeat(activ_))))

                # Safely extract scalar log-probabilities and choose best HMM
                logps = []
                for r in results:
                    try:
                        logps.append(float(r[1]))
                    except Exception:
                        logps.append(_np.nan)
                best = int(_np.nanargmax(_np.array(logps)))

                path, _ = results[best]
                st = self.hmms[best].transition_model.state_space
                om = self.hmms[best].observation_model
                positions = st.state_positions[path]
                beat_numbers = positions.astype(int) + 1

                if self.correct:
                    beats = _np.empty(0, dtype=int)
                    beat_range = om.pointers[path] >= 1
                    idx2 = _np.nonzero(_np.diff(beat_range.astype(int)))[0] + 1
                    if beat_range[0]:
                        idx2 = _np.r_[0, idx2]
                    if beat_range[-1]:
                        idx2 = _np.r_[idx2, beat_range.size]
                    if idx2.any():
                        for left, right in idx2.reshape((-1, 2)):
                            peak = _np.argmax(activ_[left:right]) // 2 + left
                            beats = _np.hstack((beats, peak))
                else:
                    beats = _np.nonzero(_np.diff(beat_numbers))[0] + 1

                return _np.vstack(((beats + first) / float(self.fps),
                                   beat_numbers[beats])).T

            try:
                import types
                proc.process = types.MethodType(_safe_process, proc)
            except Exception:
                proc.process = _safe_process
    except Exception:
        # If anything fails, return the original BeatNet instance unmodified
        pass

    return bn

def extract_beats(audio_file_path):
    """
    Extracts beat and downbeat times from an audio file using BeatNet.

    Args:
        audio_file_path (str): The path to the audio file.

    Returns:
        tuple: A tuple containing two NumPy arrays:
               - beat_times (float): The beat times in seconds.
               - downbeat_times (float): The downbeat times in seconds.
    """
    # Initialize the BeatNet estimator in offline mode using the helper that
    # ensures a safe DBN processor is attached. This keeps all fixes local to
    # this repository and avoids touching site-packages.
    estimator = create_safe_beatnet(1, mode='offline', inference_model='DBN', plot=[], thread=False)

    try:
        # Load the audio file. BeatNet is optimized for 22050 Hz.
        # It handles the resampling internally if you provide a file path.
        output_results = estimator.process(audio_file_path)

        # The output is expected to be a 2-column array: [time, event_type].
        # But BeatNet may return nested or inhomogeneous sequences. Normalize
        # defensively: iterate, attempt to coerce rows to two floats, and
        # collect valid events.
        valid_rows = []
        if output_results is None:
            raise ValueError("BeatNet returned None")

        # If it's already a well-formed numeric 2D ndarray, use it directly.
        # Otherwise fall back to a safe, per-row coercion path that tolerates
        # object-dtype arrays and nested sequences.
        if isinstance(output_results, np.ndarray) and getattr(output_results, 'ndim', None) == 2 and np.issubdtype(output_results.dtype, np.number):
            arr = output_results.astype(float)
        else:
            # Build an iterable of rows. If output_results isn't iterable, treat
            # it as a single row container.
            try:
                seq = list(output_results)
            except Exception:
                seq = [output_results]

            for idx, row in enumerate(seq):
                try:
                    # Handle a few row shapes:
                    # - simple sequence/tuple/ndarray: take first two numeric-like entries
                    # - nested structures: try to drill into sub-sequences to find scalars
                    t = ev = None
                    if isinstance(row, (list, tuple, np.ndarray)):
                        # Try straightforward float coercion for first two elements
                        try:
                            t = float(row[0])
                            ev = float(row[1])
                        except Exception:
                            # Fallback: scan items for numeric scalars
                            flat = []
                            for item in row:
                                if len(flat) >= 2:
                                    break
                                try:
                                    flat.append(float(item))
                                except Exception:
                                    # If item is itself iterable, try its first element
                                    try:
                                        it = iter(item)
                                        first = next(it)
                                        flat.append(float(first))
                                    except Exception:
                                        continue
                            if len(flat) >= 2:
                                t, ev = flat[0], flat[1]
                    else:
                        # row not a sequence: try treating it like (time,event)
                        try:
                            t = float(row[0])
                            ev = float(row[1])
                        except Exception:
                            # give up on this row
                            raise

                    if t is None or ev is None:
                        # couldn't extract two numeric values from this row
                        raise ValueError("row did not contain two numeric values")

                    valid_rows.append((t, ev))
                except Exception:
                    # skip malformed rows
                    continue

            if not valid_rows:
                raise ValueError("No valid beat/downbeat events returned by BeatNet")

            # Convert collected valid rows to a numeric array
            arr = np.array(valid_rows, dtype=float)

        # Now arr is a 2D numeric array. Extract beats (event == 1) and downbeats (event == 2).
        if arr.size == 0 or arr.shape[1] < 2:
            raise ValueError("Unexpected shape from BeatNet output")

        beat_times = arr[arr[:, 1] == 1, 0]
        downbeat_times = arr[arr[:, 1] == 2, 0]

        return np.asarray(beat_times, dtype=float), np.asarray(downbeat_times, dtype=float)

    except Exception:
        # Do not swallow errors or return fallbacks — re-raise so the caller sees the real failure.
        raise

# --- Example Usage ---
if __name__ == '__main__':
    audio_file = "/home/darkangel/ai-light-show_agents/songs/born_slippy.mp3"

    print(f"Starting beat detection for: {audio_file}")
    
    # Run the function
    beats, downbeats = extract_beats(audio_file)

    if beats.size > 0:
        print("\n--- Detected Beats ---")
        # Print the first 20 beat times to keep the output concise
        for i, beat_time in enumerate(beats[:20]):
            print(f"Beat {i+1}: {beat_time:.3f} seconds")
        
        print("\n--- Detected Downbeats ---")
        # Print the first 5 downbeat times
        for i, downbeat_time in enumerate(downbeats[:5]):
            print(f"Downbeat {i+1}: {downbeat_time:.3f} seconds")
        
        print(f"\nTotal beats detected: {len(beats)}")
        print(f"Total downbeats detected: {len(downbeats)}")
    else:
        print("No beats were detected or an error occurred. Check the file path and format.")