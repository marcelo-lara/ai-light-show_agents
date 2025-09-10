import { useEffect, useRef, useState } from 'preact/hooks';
import { useWebSocket } from '../hooks/useWebSocket';
import WaveSurfer from 'wavesurfer.js';
import './AudioPlayer.css';

export function AudioPlayer() {
  const { currentSong, isPlaying, currentTime, sendMessage } = useWebSocket();
  const waveformRef = useRef<HTMLDivElement>(null);
  const wavesurferRef = useRef<WaveSurfer | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [duration, setDuration] = useState(0);

  // Initialize WaveSurfer instance
  useEffect(() => {
    // Only initialize WaveSurfer when both the container is available AND we have a song
    if (!waveformRef.current || !currentSong) {
      if (!waveformRef.current) {
        console.log('⏳ Waiting for waveform container to be available...');
      }
      if (!currentSong) {
        console.log('⏳ Waiting for song to be loaded...');
      }
      return;
    }

    console.log('🎵 Initializing WaveSurfer...');

    const wavesurfer = WaveSurfer.create({
      container: waveformRef.current,
      waveColor: '#4a9eff',
      progressColor: '#007acc',
      cursorColor: '#ffffff',
      barWidth: 2,
      barGap: 1,
      height: 60,
      normalize: true,
      interact: true,
    });

    wavesurferRef.current = wavesurfer;
    console.log('✅ WaveSurfer instance created successfully');

    // Event listeners
    wavesurfer.on('ready', () => {
      console.log(`✅ Audio file loaded successfully`);
      setIsLoading(false);
      setDuration(wavesurfer.getDuration());
    });

    wavesurfer.on('loading', (percent: number) => {
      console.log(`⏳ Loading audio: ${percent}% - WaveSurfer is processing the audio file`);
      setIsLoading(percent < 100);
    });

    wavesurfer.on('error', (error) => {
      console.error(`❌ WaveSurfer error:`, error);
      setIsLoading(false);
    });

    wavesurfer.on('decode', () => {
      console.log(`🎵 Audio file decoded successfully`);
    });

    wavesurfer.on('load', () => {
      console.log(`📡 Audio file load event triggered`);
    });

    wavesurfer.on('interaction', () => {
      const time = wavesurfer.getCurrentTime();
      sendMessage('seek_audio', { time });
    });

    wavesurfer.on('play', () => {
      sendMessage('play_audio');
    });

    wavesurfer.on('pause', () => {
      sendMessage('pause_audio');
    });

    // Now load the audio file
    console.log(`🎵 Loading audio file: ${currentSong}.mp3`);
    setIsLoading(true);
    
    const audioUrl = `/songs/${currentSong}.mp3`;
    console.log(`🔗 Full audio URL: ${audioUrl}`);
    
    // Test if the audio file is accessible via fetch
    fetch(audioUrl, { method: 'HEAD' })
      .then(response => {
        console.log(`🌐 Audio file HEAD request:`, {
          status: response.status,
          ok: response.ok,
          headers: {
            'content-type': response.headers.get('content-type'),
            'content-length': response.headers.get('content-length')
          }
        });
      })
      .catch(error => {
        console.error(`❌ Audio file HEAD request failed:`, error);
      });

    try {
      console.log(`🎵 Calling wavesurfer.load() with URL: ${audioUrl}`);
      wavesurfer.load(audioUrl);
    } catch (error) {
      console.error(`❌ Failed to load audio: ${error}`);
      setIsLoading(false);
    }

    return () => {
      console.log('🧹 Cleaning up WaveSurfer instance');
      wavesurfer.destroy();
    };
  }, [sendMessage, currentSong]);

  // Remove the separate audio loading useEffect since it's now consolidated above

  // Sync playback state with WebSocket
  useEffect(() => {
    if (!wavesurferRef.current) return;

    if (isPlaying && !wavesurferRef.current.isPlaying()) {
      wavesurferRef.current.play();
    } else if (!isPlaying && wavesurferRef.current.isPlaying()) {
      wavesurferRef.current.pause();
    }
  }, [isPlaying]);

  // Sync current time with WebSocket
  useEffect(() => {
    if (!wavesurferRef.current || !duration) return;

    const wavesurferTime = wavesurferRef.current.getCurrentTime();
    const timeDiff = Math.abs(wavesurferTime - currentTime);

    // Only seek if there's a significant difference (avoid feedback loops)
    if (timeDiff > 0.5) {
      wavesurferRef.current.seekTo(currentTime / duration);
    }
  }, [currentTime, duration]);

  const handlePlayPause = () => {
    if (!wavesurferRef.current || !currentSong || isLoading) {
      console.warn('⚠️ Cannot play/pause: audio not ready');
      return;
    }

    if (isPlaying) {
      sendMessage('pause_audio');
    } else {
      sendMessage('play_audio');
    }
  };

  const handleStop = () => {
    if (!wavesurferRef.current || isLoading) {
      console.warn('⚠️ Cannot stop: audio not ready');
      return;
    }
    sendMessage('stop_audio');
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div class="card audio-player">
     
      {!currentSong ? (
        <div class="no-song">
          <p class="muted">No song loaded</p>
        </div>
      ) : (
        <>

          <div class="waveform-container">
            {isLoading && (
              <div class="loading-overlay">
                <span>Loading {currentSong}.mp3...</span>
              </div>
            )}
            <div ref={waveformRef} class="waveform" />
          </div>

          <div class="player-controls">
            <div class="playback-controls">
              <button 
                onClick={handlePlayPause} 
                disabled={isLoading}
                class={`play-pause-btn ${isPlaying ? 'playing' : 'paused'}`}
              >
                {isPlaying ? '⏸️' : '▶️'}
              </button>
              
              <button 
                onClick={handleStop} 
                disabled={isLoading}
                class="stop-btn"
              >
                ⏹️
              </button>
            </div>

            <div class="time-display">
              <span class="current-time">{formatTime(currentTime)}</span>
              <span class="time-separator">/</span>
              <span class="total-time">{formatTime(duration)}</span>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
