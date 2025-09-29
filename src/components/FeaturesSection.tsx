import { Card, CardContent } from '@/components/ui/card';
import { Heart, Users, Headphones, Crown, MessageCircle, Shield } from 'lucide-react';

const features = [
  {
    icon: Users,
    title: "Friendly & Active Members",
    description: "Join thousands of welcoming members from around the world",
    color: "text-heart",
  },
  {
    icon: Shield,
    title: "24/7 Responsive Staff", 
    description: "Our dedicated team ensures a safe and fun environment",
    color: "text-accent",
  },
  {
    icon: Crown,
    title: "Staff Applications Open",
    description: "Want to help our community grow? Apply to join our team!",
    color: "text-secondary",
  },
  {
    icon: MessageCircle,
    title: "Late-Night Conversations",
    description: "Deep talks, gaming sessions, and memorable moments",
    color: "text-primary",
  },
  {
    icon: Heart,
    title: "Love Stories Begin",
    description: "Many relationships have blossomed in our community",
    color: "text-heart",
  },
  {
    icon: Headphones,
    title: "Gaming Community",
    description: "Connect with fellow gamers and join epic gaming sessions",
    color: "text-minecraft",
  },
];

const FeaturesSection = () => {
  return (
    <section className="py-20 px-4 relative">
      <div className="max-w-6xl mx-auto">
        {/* Section Header */}
        <div className="text-center mb-16 fade-in-section">
          <h2 className="text-3xl md:text-4xl font-bold mb-4 bg-gradient-secondary bg-clip-text text-transparent">
            Why Choose Baatein♡?
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Discover what makes our community special and why thousands of members call Baatein♡ home
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <Card 
              key={index} 
              className="bg-card/50 backdrop-blur-sm border-border/50 hover:shadow-glow transition-all duration-300 hover:scale-105 fade-in-section"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <CardContent className="p-6 text-center">
                <div className="flex justify-center mb-4">
                  <feature.icon className={`w-12 h-12 ${feature.color}`} />
                </div>
                <h3 className="text-xl font-semibold mb-3 text-foreground">
                  {feature.title}
                </h3>
                <p className="text-muted-foreground leading-relaxed">
                  {feature.description}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;