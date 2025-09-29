import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Gamepad2, Globe, Users, Zap } from 'lucide-react';

const MinecraftSection = () => {
  const copyServerIP = () => {
    navigator.clipboard.writeText('play.confessionmc.fun');
    // You could add a toast notification here
  };

  return (
    <section className="py-20 px-4 relative">
      <div className="max-w-4xl mx-auto">
        {/* Section Header */}
        <div className="text-center mb-12 fade-in-section">
          <h2 className="text-3xl md:text-4xl font-bold mb-4 bg-gradient-gaming bg-clip-text text-transparent">
            🎮 Thriving Minecraft Community
          </h2>
          <p className="text-xl text-muted-foreground">
            Join our amazing Minecraft server and build, explore, and survive with friends!
          </p>
        </div>

        {/* Server Card */}
        <Card className="bg-gradient-to-br from-minecraft/20 to-accent/20 border-minecraft/30 shadow-glow fade-in-section">
          <CardContent className="p-8">
            <div className="grid md:grid-cols-2 gap-8 items-center">
              {/* Server Info */}
              <div className="space-y-6">
                <div className="space-y-2">
                  <h3 className="text-2xl font-bold text-minecraft">ConfessionMC Server</h3>
                  <p className="text-lg text-muted-foreground">
                    A community-driven survival server with amazing features and friendly players
                  </p>
                </div>

                {/* Server IP */}
                <div className="bg-card/50 rounded-lg p-4 border border-minecraft/30">
                  <div className="flex items-center justify-between">
                    <div>
                      <span className="text-sm text-muted-foreground">Server IP:</span>
                      <p className="text-xl font-mono font-bold text-minecraft">
                        play.confessionmc.fun
                      </p>
                    </div>
                    <Button 
                      variant="minecraft" 
                      size="sm"
                      onClick={copyServerIP}
                    >
                      Copy IP
                    </Button>
                  </div>
                </div>

                {/* Features */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="flex items-center gap-2">
                    <Users className="w-5 h-5 text-minecraft" />
                    <span className="text-sm">Active Community</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Globe className="w-5 h-5 text-minecraft" />
                    <span className="text-sm">Survival Mode</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Zap className="w-5 h-5 text-minecraft" />
                    <span className="text-sm">24/7 Uptime</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Gamepad2 className="w-5 h-5 text-minecraft" />
                    <span className="text-sm">Events & Competitions</span>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="space-y-4">
                <Button variant="minecraft" size="xl" className="w-full glow-effect">
                  <Gamepad2 className="w-5 h-5 mr-2" />
                  Join Minecraft Server
                </Button>
                
                <a 
                  href="https://discord.gg/baatein" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="block"
                >
                  <Button variant="outline" size="lg" className="w-full">
                    Get Help in Discord
                  </Button>
                </a>

                <p className="text-sm text-muted-foreground text-center">
                  Need help connecting? Ask in our Discord server for assistance!
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </section>
  );
};

export default MinecraftSection;