# Song Analysis (Lighting Show Preparation)

Generates a JSON summary for an MP3 + stems suitable as context for an LLM to design a lighting plan.

## Output Schema
```
{
  "tempo": 128,                 # Estimated BPM (rounded)
  "key": "Dm",                  # Musical key 
  "structure": [                # Coarse sectional segmentation
    {"section": "intro", "start": 0.0, "end": 12.0},
    ...
  ],
  "beats": [0.46, 0.92, ...],   # Beat timestamps (seconds)
  "drums": {
    "kick_onsets": [...],       # Kick-like onset times (band-energy heuristic)
    "snare_onsets": [...]       # Snare-like onset times
  },
  "vocals": {
    "active_sections": [        # Continuous vocal activity ranges (RMS > percentile threshold)
      {"start": 12.1, "end": 36.0}, ...
    ],
    "pitch_contour": [220.0, ...]  # Simplified f0 track (piptrack peak per frame)
  },
  "energy_curve": [0.1, ...],   # RMS-based half-overlap energy window (≈0.5s)
  "events": [                   # Derived macro musical events
    {"type": "drop", "time": 52.0},
    {"type": "climax", "time": 80.0}
  ]
}
```

## Rationale (LLM-Relevant Features)
- Tempo & beats: drive strobe rate, chases, accent alignment.
- Key: optional color harmony mapping (e.g. circle-of-fifths palette shifts).
- Structure: macro scene changes (intro, verse, build, chorus, break, outro).
- Kick / snare onsets: rhythmic anchor for dimmer bumps, blinders, strobes.
- Vocal activity: prioritize face/front lighting; mute it during instrumental builds.
- Pitch contour: map melodic motion to pan/tilt, color temperature, gobo rotation.
- Energy curve: intensity automation, build detection, dynamic FX scaling.
- Events (drop/climax): trigger impactful cues (color invert, audience blinders, haze bursts).

Optional future additions (not yet implemented to keep dependencies minimal): chord progression, spectral brightness, bass energy curve, per-stem energy ratios, silence spans, transient density, tension curve.

## Usage
```
python song_analysis/analyze_song.py \
  --song songs/born_slippy.mp3 \
  --stems stems/born_slippy \
  --out data/born_slippy.analysis.json
```

Install deps (CPU):
```
pip install -r song_analysis/requirements.txt
```
(Install `essentia` wheel matching your Python version; if unavailable the script falls back to librosa heuristics.)

### Automatic Stem Splitting
If the required stems (at least `vocals.wav`, `drums.wav`) are missing inside the provided `--stems` folder, the script will attempt to generate them using Spleeter (default 4 stems: vocals, drums, bass, other). Control this behavior:

```
--no-split            # disable automatic separation
--stems-model 2stems  # use 2 stems instead of 4
```
Resulting stem files are placed directly inside the `--stems` directory.

## Notes
- Section segmentation is heuristic; refine by integrating a dedicated structural segmentation model if higher fidelity is needed.
- Kick/snare classification uses simple band energy; for higher accuracy consider a lightweight ML onset classifier.
- Pitch contour is sparse and un-smoothed; apply median filtering if needed for smoother motion mapping.
