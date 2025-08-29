"""Spectral and emotional feature extraction for lighting themes."""
from __future__ import annotations
from typing import List, Dict, Tuple, Any, Optional
import numpy as np

try:
    import librosa  # type: ignore
except ImportError:  # pragma: no cover
    librosa = None  # type: ignore

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
    """Classify mood and emotion using spectral analysis.

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

    if librosa is None:
        print("!!!!!Librosa is not available.")
        return result

    try:
        # Use spectral analysis for mood estimation
        spectral_features = compute_spectral_features(y, sr)
        if spectral_features['spectral_centroid']:
            avg_centroid = np.mean(spectral_features['spectral_centroid'])
            avg_flux = np.mean(spectral_features['spectral_flux']) if spectral_features['spectral_flux'] else 0

            # Enhanced mood estimation based on spectral features
            if avg_centroid > 3500:  # Very bright/high frequency
                result['mood'] = 'bright'
                result['emotion'] = 'energetic'
                result['lighting_theme'] = 'bright_warm'
            elif avg_centroid > 2500:  # Bright/medium frequency
                result['mood'] = 'bright'
                result['emotion'] = 'uplifting'
                result['lighting_theme'] = 'warm_white'
            elif avg_centroid > 1500:  # Medium frequency
                result['mood'] = 'neutral'
                result['emotion'] = 'balanced'
                result['lighting_theme'] = 'balanced'
            else:  # Dark/low frequency
                result['mood'] = 'dark'
                result['emotion'] = 'calm'
                result['lighting_theme'] = 'cool_blue'

            # Adjust based on spectral flux (texture changes)
            if avg_flux > 0.15:  # High texture changes = very energetic
                if result['mood'] == 'bright':
                    result['lighting_theme'] = 'energetic_bright'
                    result['emotion'] = 'excited'
                elif result['mood'] == 'neutral':
                    result['lighting_theme'] = 'dynamic_white'
                    result['emotion'] = 'active'
                else:
                    result['lighting_theme'] = 'medium_bright'
                    result['emotion'] = 'mysterious'
            elif avg_flux > 0.08:  # Medium texture changes = moderate energy
                if result['mood'] == 'bright':
                    result['lighting_theme'] = 'soft_light'
                    result['emotion'] = 'joyful'
                elif result['mood'] == 'dark':
                    result['lighting_theme'] = 'calm_blue'
                    result['emotion'] = 'peaceful'
            else:  # Low texture changes = calm
                if result['mood'] == 'bright':
                    result['lighting_theme'] = 'gentle_warm'
                    result['emotion'] = 'serene'
                elif result['mood'] == 'dark':
                    result['lighting_theme'] = 'deep_blue'
                    result['emotion'] = 'meditative'

            result['confidence'] = 0.8  # Good confidence for enhanced spectral-based estimation

    except Exception as e:
        # If spectral analysis fails, return basic result
        result['mood'] = 'neutral'
        result['emotion'] = 'neutral'
        result['confidence'] = 0.5
        result['lighting_theme'] = 'balanced'

    return result

def analyze_spectral_emotion(y: np.ndarray, sr: int, sections: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """Complete spectral and emotional analysis.

    Args:
        y: Audio signal
        sr: Sample rate
        sections: Optional list of song sections with start/end times

    Returns:
        {
            'spectral_features': {...},
            'mood_analysis': {...},
            'section_moods': [...]  # Only if sections provided
        }
    """
    spectral_features = compute_spectral_features(y, sr)
    mood_analysis = classify_mood_emotion(y, sr)
    
    result = {
        'spectral_features': spectral_features,
        'mood_analysis': mood_analysis
    }
    
    # Analyze mood for each section if sections are provided
    if sections:
        section_moods = []
        for section in sections:
            start_time = section['start']
            end_time = section['end']
            
            # Convert time to sample indices
            start_sample = int(start_time * sr)
            end_sample = int(end_time * sr)
            
            # Extract section audio
            if start_sample < len(y) and end_sample <= len(y):
                section_audio = y[start_sample:end_sample]
                
                # Analyze this section
                section_spectral = compute_spectral_features(section_audio, sr)
                section_mood = classify_mood_emotion(section_audio, sr)
                
                section_analysis = {
                    'section': section['section'],
                    'start': start_time,
                    'end': end_time,
                    'duration': end_time - start_time,
                    'spectral_features': section_spectral,
                    'mood_analysis': section_mood
                }
                section_moods.append(section_analysis)
        
        result['section_moods'] = section_moods
    
    return result
