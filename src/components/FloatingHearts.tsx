import { Heart } from 'lucide-react';
import { useEffect, useState } from 'react';

interface FloatingHeart {
  id: number;
  x: number;
  y: number;
  size: number;
  delay: number;
}

const FloatingHearts = () => {
  const [hearts, setHearts] = useState<FloatingHeart[]>([]);

  useEffect(() => {
    const heartCount = 15;
    const newHearts: FloatingHeart[] = [];

    for (let i = 0; i < heartCount; i++) {
      newHearts.push({
        id: i,
        x: Math.random() * 100,
        y: Math.random() * 100,
        size: Math.random() * 20 + 15,
        delay: Math.random() * 3,
      });
    }

    setHearts(newHearts);
  }, []);

  return (
    <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden">
      {hearts.map((heart) => (
        <Heart
          key={heart.id}
          className="absolute text-heart-glow opacity-20 floating-hearts"
          style={{
            left: `${heart.x}%`,
            top: `${heart.y}%`,
            fontSize: `${heart.size}px`,
            animationDelay: `${heart.delay}s`,
          }}
          fill="currentColor"
        />
      ))}
    </div>
  );
};

export default FloatingHearts;