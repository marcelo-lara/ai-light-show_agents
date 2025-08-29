# Song Analysis (Lighting Show Preparation)

A modular Python package that analyzes songs to generate comprehensive JSON summaries for AI-driven lighting show design. Extracts musical features from MP3 files and stems to provide context for LLM-based lighting planning.

## Module Architecture

The analysis pipeline is organized into specialized modules, each handling a specific aspect of musical feature extraction:

### Core Analysis Modules
- **`analyze_song.py`** - Main orchestration script that coordinates all analysis modules
- **`audio_io.py`** - Audio file loading and preprocessing utilities
- **`stems.py`** - Automatic stem separation using Spleeter when stems are missing

### Feature Extraction Modules
- **`rhythm.py`** - Tempo estimation, beat detection, and percussive onset analysis
- **`harmony.py`** - Musical key estimation and harmonic analysis
- **`vocals.py`** - Vocal activity detection and pitch contour extraction
- **`energy.py`** - RMS-based energy curve computation for dynamic analysis
- **`structure.py`** - Song section segmentation (intro, verse, chorus, etc.)
- **`events.py`** - Detection of musical events (drops, climaxes, builds)
- **`spectral.py`** - Spectral features and emotional mood classification

### Utilities
- **`schema.py`** - Data structure definitions and validation
- **`smoke_test.py`** - Integration testing and validation

## Output Schema

The analysis generates a comprehensive JSON structure with all musical features:

```json
{
  "tempo": 128,
  "key": "Dm",
  "structure": [
    {"section": "intro", "start": 0.0, "end": 12.0},
    {"section": "verse", "start": 12.0, "end": 24.0}
  ],
  "beats": [0.46, 0.92, 1.38, ...],
  "drums": {
    "kick_onsets": [27.60, 28.12, 28.64, ...],
    "snare_onsets": [34.17, 34.69, 35.21, ...]
  },
  "vocals": {
    "active_sections": [
      {"start": 13.59, "end": 44.96},
      {"start": 54.09, "end": 90.09}
    ],
    "pitch_contour": [220.0, 233.0, 247.0, ...]
  },
  "energy_curve": [0.1, 0.15, 0.12, ...],
  "events": [
    {"type": "drop", "time": 52.0},
    {"type": "climax", "time": 80.0}
  ],
  "spectral_emotion": {
    "spectral_features": {
      "spectral_centroid": [2324, 3303, 4168, ...],
      "spectral_flux": [0.05, 0.08, 0.12, ...],
      "chroma_features": [0.3, 0.4, 0.2, ...]
    },
    "mood_analysis": {
      "mood": "bright",
      "emotion": "excited",
      "confidence": 0.8,
      "lighting_theme": "energetic_bright"
    },
    "section_moods": [
      {
        "section": "intro",
        "start": 0.0,
        "end": 34.2,
        "duration": 34.2,
        "spectral_features": {...},
        "mood_analysis": {
          "mood": "neutral",
          "emotion": "active",
          "lighting_theme": "dynamic_white"
        }
      }
    ]
  }
}
```

## Feature Descriptions

### Musical Foundation
- **Tempo & Beats**: BPM estimation and beat timestamps for rhythmic lighting cues
- **Key**: Musical key for potential color harmony mapping
- **Structure**: Section segmentation for scene changes and transitions

### Rhythmic Elements
- **Drum Onsets**: Kick and snare detection for percussive lighting triggers
- **Energy Curve**: Dynamic intensity analysis for automated lighting levels
- **Events**: Macro musical events (drops, climaxes) for impactful lighting cues

### Vocal & Harmonic Content
- **Vocal Activity**: Continuous vocal sections for face/front lighting priority
- **Pitch Contour**: Melodic motion for pan/tilt and color temperature mapping

### Emotional & Spectral Analysis
- **Spectral Features**: Brightness (centroid), texture changes (flux), and harmonic content (chroma)
- **Mood Classification**: Overall song mood and emotion with lighting theme suggestions
- **Section Moods**: Per-section emotional analysis for dynamic theme transitions

## Usage

### Basic Analysis
```bash
python song_analysis/analyze_song.py \
  --song songs/born_slippy.mp3 \
  --stems stems/born_slippy \
  --out data/born_slippy.analysis.json
```

### Advanced Options
```bash
# Disable automatic stem separation
python song_analysis/analyze_song.py \
  --song songs/born_slippy.mp3 \
  --stems stems/born_slippy \
  --out data/born_slippy.analysis.json \
  --no-split

# Use 2-stem separation instead of 4-stem
python song_analysis/analyze_song.py \
  --song songs/born_slippy.mp3 \
  --stems stems/born_slippy \
  --out data/born_slippy.analysis.json \
  --stems-model 2stems
```

## Installation

Install dependencies (CPU-optimized):
```bash
pip install -r song_analysis/requirements.txt
```

The package uses librosa for core audio analysis with fallback heuristics when Essentia is unavailable.

### Automatic Stem Splitting

If required stems (`vocals.wav`, `drums.wav`) are missing, the script automatically generates them using Spleeter:
- Default: 4 stems (vocals, drums, bass, other)
- Optional: 2 stems (vocals, accompaniment)
- Stems are saved directly in the `--stems` directory

## Lighting Design Applications

The extracted features enable various lighting automation strategies:

- **Rhythmic Sync**: Beat-aligned strobe effects and chase patterns
- **Dynamic Intensity**: Energy curve-driven dimmer automation
- **Emotional Themes**: Mood-based color palette and lighting theme selection
- **Section Transitions**: Structure-aware scene changes
- **Event Triggers**: Drop/climax detection for spectacular effects
- **Vocal Enhancement**: Front lighting during vocal sections
- **Spectral Mapping**: Brightness and texture features for dynamic effects

## Notes

- **Section Segmentation**: Uses heuristic clustering; consider ML models for higher accuracy
- **Drum Classification**: Band-energy based detection; ML classifiers available for improved precision
- **Mood Analysis**: Spectral-based classification with high confidence; provides detailed lighting theme suggestions
- **Pitch Tracking**: Sparse contour; apply smoothing filters for continuous motion mapping
- **Performance**: Optimized for CPU processing with minimal dependencies
- **Extensibility**: Modular design allows easy addition of new analysis features
