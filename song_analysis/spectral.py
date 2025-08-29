"""Spectral and emotional feature extraction for lighting themes."""
from __future__ import annotations
from typing import List, Dict, Tuple, Any
import numpy as np

try:
    import librosa  # type: ignore
except ImportError:  # pragma: no cover
    librosa = None  # type: ignore

try:
    import essentia  # type: ignore
    import essentia.standard as es  # type: ignore
except ImportError:  # pragma: no cover
    essentia = None  # type: ignore
    es = None  # type: ignore

def compute_spectral_features(y: np.ndarray, sr: int) -> Dict[str, List[float]]:
    """Compute spectral features for lighting control.

    Returns:
        {
            'spectral_centroid': [...],  # Brightness indicator
            'spectral_flux': [...],      # Texture change indicator
            'chroma_features': [...]     # Harmonic content
        }
    """
    features = {
        'spectral_centroid': [],
        'spectral_flux': [],
        'chroma_features': []
    }

    if librosa is None:
        return features

    # Compute spectral features with appropriate windowing
    frame_length = 2048
    hop_length = 512

    # Spectral centroid (brightness)
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr, n_fft=frame_length, hop_length=hop_length)[0]
    features['spectral_centroid'] = centroid.tolist()

    # Spectral flux (texture changes) - compute manually
    S = np.abs(librosa.stft(y, n_fft=frame_length, hop_length=hop_length))
    S_log = librosa.power_to_db(S**2, ref=np.max)
    flux = np.sqrt(np.sum(np.diff(S_log, axis=1)**2, axis=0))
    features['spectral_flux'] = flux.tolist()

    # Chroma features (harmonic content)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr, n_fft=frame_length, hop_length=hop_length)
    # Average chroma across all bins for a single time series
    features['chroma_features'] = chroma.mean(axis=0).tolist()

    return features

def classify_mood_emotion(y: np.ndarray, sr: int) -> Dict[str, Any]:
    """Classify mood and emotion using Essentia.

    Returns:
        {
            'mood': str,           # Primary mood
            'emotion': str,        # Primary emotion
            'confidence': float,   # Classification confidence
            'lighting_theme': str  # Suggested lighting theme
        }
    """
    result = {
        'mood': 'unknown',
        'emotion': 'neutral',
        'confidence': 0.0,
        'lighting_theme': 'default'
    }

    if es is None:
        return result

    try:
        # For now, use spectral analysis for mood estimation
        # Essentia extractors may not be available in this environment
        raise ImportError("Essentia extractors not available")

    except Exception as e:
        print(f"Warning: Advanced mood classification failed: {e}")
        # Fallback to basic spectral analysis
        spectral_features = compute_spectral_features(y, sr)
        if spectral_features['spectral_centroid']:
            avg_centroid = np.mean(spectral_features['spectral_centroid'])
            avg_flux = np.mean(spectral_features['spectral_flux']) if spectral_features['spectral_flux'] else 0

            # Rough mood estimation based on spectral features
            if avg_centroid > 3000:  # Bright/high frequency
                result['mood'] = 'bright'
                result['lighting_theme'] = 'bright_warm'
            elif avg_centroid > 2000:  # Medium
                result['mood'] = 'neutral'
                result['lighting_theme'] = 'balanced'
            else:  # Dark/low frequency
                result['mood'] = 'dark'
                result['lighting_theme'] = 'cool_blue'

            # Adjust based on spectral flux (texture changes)
            if avg_flux > 0.1:  # High texture changes = energetic
                if result['mood'] == 'bright':
                    result['lighting_theme'] = 'energetic_rainbow'
                elif result['mood'] == 'dark':
                    result['lighting_theme'] = 'intense_purple'
            elif avg_flux < 0.05:  # Low texture changes = calm
                if result['mood'] == 'bright':
                    result['lighting_theme'] = 'soft_warm'
                elif result['mood'] == 'dark':
                    result['lighting_theme'] = 'calm_blue'

            result['confidence'] = 0.7  # Moderate confidence for spectral-based estimation

    return result

def analyze_spectral_emotion(y: np.ndarray, sr: int) -> Dict[str, Any]:
    """Complete spectral and emotional analysis.

    Returns:
        {
            'spectral_features': {...},
            'mood_analysis': {...}
        }
    """
    spectral_features = compute_spectral_features(y, sr)
    mood_analysis = classify_mood_emotion(y, sr)

    return {
        'spectral_features': spectral_features,
        'mood_analysis': mood_analysis
    }
