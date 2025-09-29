import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Volume2, VolumeX } from 'lucide-react';

const MusicToggle = () => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [volume, setVolume] = useState(0.3);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    // Create audio element with a free lofi track
    // In a real app, you'd host your own audio file
    audioRef.current = new Audio();
    audioRef.current.loop = true;
    audioRef.current.volume = volume;
    
    // For demo purposes, we'll use a placeholder
    // You would replace this with your actual lofi/chill music file
    // audioRef.current.src = '/path/to/your/lofi-music.mp3';
    
    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }
    };
  }, [volume]);

  const toggleMusic = async () => {
    if (!audioRef.current) return;

    if (isPlaying) {
      audioRef.current.pause();
      setIsPlaying(false);
    } else {
      try {
        await audioRef.current.play();
        setIsPlaying(true);
      } catch (error) {
        console.log('Audio playback failed:', error);
        // Fallback for browsers that block autoplay
      }
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      <Button
        variant="glow"
        size="icon"
        onClick={toggleMusic}
        className="rounded-full shadow-glow hover:shadow-pink-glow"
        title={isPlaying ? 'Pause music' : 'Play background music'}
      >
        {isPlaying ? (
          <Volume2 className="w-5 h-5" />
        ) : (
          <VolumeX className="w-5 h-5" />
        )}
      </Button>
      
      {/* Volume Control (appears on hover) */}
      {isPlaying && (
        <div className="absolute bottom-16 right-0 bg-card/90 backdrop-blur-sm rounded-lg p-3 opacity-0 hover:opacity-100 transition-opacity">
          <input
            type="range"
            min="0"
            max="1"
            step="0.1"
            value={volume}
            onChange={(e) => {
              const newVolume = parseFloat(e.target.value);
              setVolume(newVolume);
              if (audioRef.current) {
                audioRef.current.volume = newVolume;
              }
            }}
            className="w-20 accent-primary"
          />
        </div>
      )}
    </div>
  );
};

export default MusicToggle;