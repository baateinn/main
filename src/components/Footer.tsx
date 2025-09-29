import { Heart, Users, Gamepad2, MessageCircle } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-card/30 backdrop-blur-sm border-t border-border/50 py-12">
      <div className="max-w-6xl mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          {/* Logo and Description */}
          <div className="space-y-4">
            <h3 className="text-2xl font-bold bg-gradient-secondary bg-clip-text text-transparent">
              Baatein♡
            </h3>
            <p className="text-muted-foreground leading-relaxed">
              A warm and welcoming Discord community where friendships bloom, 
              gamers unite, and love stories begin.
            </p>
          </div>

          {/* Quick Links */}
          <div className="space-y-4">
            <h4 className="text-lg font-semibold text-foreground">Quick Links</h4>
            <div className="space-y-2">
              <a 
                href="https://discord.gg/baatein" 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex items-center gap-2 text-muted-foreground hover:text-discord transition-colors"
              >
                <MessageCircle className="w-4 h-4" />
                Join Discord
              </a>
              <a 
                href="#minecraft" 
                className="flex items-center gap-2 text-muted-foreground hover:text-minecraft transition-colors"
              >
                <Gamepad2 className="w-4 h-4" />
                Minecraft Server
              </a>
              <a 
                href="#staff-application" 
                className="flex items-center gap-2 text-muted-foreground hover:text-secondary transition-colors"
              >
                <Users className="w-4 h-4" />
                Staff Application
              </a>
            </div>
          </div>

          {/* Community Stats */}
          <div className="space-y-4">
            <h4 className="text-lg font-semibold text-foreground">Community</h4>
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <Heart className="w-4 h-4 text-heart fill-current" />
                <span className="text-muted-foreground">Social & Dating</span>
              </div>
              <div className="flex items-center gap-2">
                <Gamepad2 className="w-4 h-4 text-minecraft" />
                <span className="text-muted-foreground">Gaming Hub</span>
              </div>
              <div className="flex items-center gap-2">
                <Users className="w-4 h-4 text-accent" />
                <span className="text-muted-foreground">Active Community</span>
              </div>
              <div className="flex items-center gap-2">
                <MessageCircle className="w-4 h-4 text-primary" />
                <span className="text-muted-foreground">24/7 Chat</span>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-border/30 pt-8 text-center">
          <p className="text-muted-foreground">
            © 2025 Baatein♡ | Community • Gaming • Hangout • Dating
          </p>
          <p className="text-sm text-muted-foreground/70 mt-2">
            Made with <Heart className="w-4 h-4 inline text-heart fill-current mx-1" /> for our amazing community
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;