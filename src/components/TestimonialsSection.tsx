import { Card, CardContent } from '@/components/ui/card';
import { Heart, Star } from 'lucide-react';

const testimonials = [
  {
    name: "Alex",
    text: "I found my best friends in Baatein♡! The community is so welcoming and the late-night gaming sessions are legendary.",
    rating: 5,
  },
  {
    name: "Sarah & Mike",
    text: "We met in this Discord and now we're getting married! Thank you Baatein♡ for bringing us together! 💕",
    rating: 5,
  },
  {
    name: "GameMaster_Pro",
    text: "The Minecraft server is amazing! Great builds, friendly players, and the staff are always helpful. 10/10!",
    rating: 5,
  },
  {
    name: "Luna",
    text: "As someone shy, I was nervous to join. But everyone was so kind and patient. Now I can't imagine life without this community!",
    rating: 5,
  },
];

const TestimonialsSection = () => {
  return (
    <section className="py-20 px-4 relative">
      <div className="max-w-6xl mx-auto">
        {/* Section Header */}
        <div className="text-center mb-16 fade-in-section">
          <h2 className="text-3xl md:text-4xl font-bold mb-4 bg-gradient-primary bg-clip-text text-transparent">
            💕 What Our Members Say
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Real stories from real members who found their place in Baatein♡
          </p>
        </div>

        {/* Testimonials Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {testimonials.map((testimonial, index) => (
            <Card 
              key={index} 
              className="bg-card/50 backdrop-blur-sm border-border/50 hover:shadow-pink-glow transition-all duration-300 hover:scale-105 fade-in-section"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <CardContent className="p-6">
                {/* Rating Stars */}
                <div className="flex items-center gap-1 mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="w-5 h-5 text-secondary fill-current" />
                  ))}
                </div>

                {/* Testimonial Text */}
                <p className="text-foreground/90 leading-relaxed mb-4 italic">
                  "{testimonial.text}"
                </p>

                {/* Author */}
                <div className="flex items-center gap-2">
                  <Heart className="w-4 h-4 text-heart fill-current" />
                  <span className="font-semibold text-heart">
                    {testimonial.name}
                  </span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Call to Action */}
        <div className="text-center mt-12 fade-in-section">
          <p className="text-lg text-muted-foreground mb-6">
            Ready to create your own story?
          </p>
          <a 
            href="https://discord.gg/baatein" 
            target="_blank" 
            rel="noopener noreferrer"
          >
            <button className="bg-gradient-secondary text-secondary-foreground px-8 py-3 rounded-lg font-semibold shadow-pink-glow hover:shadow-glow transition-all duration-300 hover:scale-105">
              <Heart className="w-5 h-5 mr-2 inline" fill="currentColor" />
              Join Our Family Today
            </button>
          </a>
        </div>
      </div>
    </section>
  );
};

export default TestimonialsSection;