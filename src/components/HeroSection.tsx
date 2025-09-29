import { Button } from '@/components/ui/button';
import { Heart, Users, Gamepad2, Crown } from 'lucide-react';
import bannerImage from '@/assets/banner.webp';
import logoImage from '@/assets/logo.png';

const HeroSection = () => {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0 bg-gradient-hero opacity-20"></div>
      
      {/* Banner Background */}
      <div 
        className="absolute inset-0 bg-cover bg-center opacity-30"
        style={{ 
          backgroundImage: `url(${bannerImage})`,
          filter: 'blur(2px)',
        }}
      ></div>

      {/* Content */}
      <div className="relative z-10 text-center space-y-8 px-4 max-w-4xl mx-auto fade-in-section">
        {/* Logo */}
        <div className="flex justify-center mb-6">
          <img 
            src={logoImage} 
            alt="Baatein♡ Logo" 
            className="w-24 h-24 md:w-32 md:h-32 rounded-full shadow-glow animate-bounce-gentle"
          />
        </div>

        {/* Title */}
        <div className="space-y-4">
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold bg-gradient-hero bg-clip-text text-transparent">
            Baatein♡
          </h1>
          <p className="text-xl md:text-2xl text-muted-foreground font-medium">
            Social • Gaming • Dating • Hangout • Community
          </p>
        </div>

        {/* Description */}
        <p className="text-lg md:text-xl text-foreground/90 max-w-3xl mx-auto leading-relaxed">
          Welcome to Baatein♡ — a warm and welcoming Discord community where friendships bloom, 
          gamers unite, and love stories begin. Join us for late-night talks, gaming sessions, 
          and unforgettable moments!
        </p>

        {/* Community Stats */}
        <div className="flex flex-wrap justify-center gap-6 my-8">
          <div className="flex items-center gap-2 text-heart">
            <Heart className="w-5 h-5" fill="currentColor" />
            <span className="font-semibold">Friendly Community</span>
          </div>
          <div className="flex items-center gap-2 text-accent">
            <Users className="w-5 h-5" />
            <span className="font-semibold">Active Members</span>
          </div>
          <div className="flex items-center gap-2 text-minecraft">
            <Gamepad2 className="w-5 h-5" />
            <span className="font-semibold">Gaming Hub</span>
          </div>
          <div className="flex items-center gap-2 text-secondary">
            <Crown className="w-5 h-5" />
            <span className="font-semibold">24/7 Staff</span>
          </div>
        </div>

        {/* Call to Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <a 
            href="https://discord.gg/baatein" 
            target="_blank" 
            rel="noopener noreferrer"
          >
            <Button variant="discord" size="xl" className="glow-effect">
              <Heart className="w-5 h-5 mr-2" fill="currentColor" />
              Join Our Discord
            </Button>
          </a>
          
          <Button variant="gaming" size="xl">
            <Gamepad2 className="w-5 h-5 mr-2" />
            Explore Community
          </Button>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;