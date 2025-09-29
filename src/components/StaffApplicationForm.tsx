import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Crown, Send } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

interface FormData {
  age: string;
  experience: string;
  whyStaff: string;
  howHelp: string;
  discordUsername: string;
}

const StaffApplicationForm = () => {
  const { toast } = useToast();
  const [formData, setFormData] = useState<FormData>({
    age: '',
    experience: '',
    whyStaff: '',
    howHelp: '',
    discordUsername: '',
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleInputChange = (field: keyof FormData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      // Validate form
      if (!formData.age || !formData.experience || !formData.whyStaff || !formData.howHelp || !formData.discordUsername) {
        toast({
          title: "Missing Information",
          description: "Please fill in all required fields.",
          variant: "destructive",
        });
        return;
      }

      // Create Discord embed payload
      const embed = {
        title: "🌟 New Staff Application",
        color: 0xDD69C7, // Pink color
        fields: [
          {
            name: "👤 Age",
            value: formData.age,
            inline: true,
          },
          {
            name: "📚 Previous Experience",
            value: formData.experience,
            inline: false,
          },
          {
            name: "💭 Why do you want to be staff?",
            value: formData.whyStaff,
            inline: false,
          },
          {
            name: "🤝 How can you help us?",
            value: formData.howHelp,
            inline: false,
          },
          {
            name: "🎮 Discord Username/ID",
            value: formData.discordUsername,
            inline: true,
          },
        ],
        timestamp: new Date().toISOString(),
        footer: {
          text: "Baatein♡ Staff Application",
        },
      };

      // Send to Discord webhook
      const response = await fetch('https://discord.com/api/webhooks/1422126079702859879/MwS0XUbRO3njuhpJ36ZMAXGvELLdwzURxCto_beEPnd6b1TxD532emqpAPqyERYlq8Ma', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          embeds: [embed],
        }),
      });

      if (response.ok) {
        toast({
          title: "Application Submitted! ✨",
          description: "Thank you for your interest! We'll review your application soon.",
        });
        
        // Reset form
        setFormData({
          age: '',
          experience: '',
          whyStaff: '',
          howHelp: '',
          discordUsername: '',
        });
      } else {
        throw new Error('Failed to submit application');
      }
    } catch (error) {
      toast({
        title: "Submission Failed",
        description: "There was an error submitting your application. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section className="py-20 px-4 relative">
      <div className="max-w-2xl mx-auto">
        <Card className="bg-card/50 backdrop-blur-sm border-border/50 shadow-glow fade-in-section">
          <CardHeader className="text-center">
            <CardTitle className="text-3xl font-bold flex items-center justify-center gap-2 bg-gradient-secondary bg-clip-text text-transparent">
              <Crown className="w-8 h-8 text-secondary" />
              Staff Application
            </CardTitle>
            <p className="text-muted-foreground">
              Want to join our amazing staff team? Fill out this application and we'll get back to you!
            </p>
          </CardHeader>
          
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="age">Age *</Label>
                <Input
                  id="age"
                  type="number"
                  min="13"
                  max="100"
                  value={formData.age}
                  onChange={(e) => handleInputChange('age', e.target.value)}
                  placeholder="Your age"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="experience">Previous Staff/Moderation Experience *</Label>
                <Textarea
                  id="experience"
                  value={formData.experience}
                  onChange={(e) => handleInputChange('experience', e.target.value)}
                  placeholder="Tell us about your previous experience as staff/moderator on Discord servers, forums, or other platforms..."
                  rows={3}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="whyStaff">Why do you want to be staff here? *</Label>
                <Textarea
                  id="whyStaff"
                  value={formData.whyStaff}
                  onChange={(e) => handleInputChange('whyStaff', e.target.value)}
                  placeholder="What motivates you to join our staff team? What do you love about our community?"
                  rows={3}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="howHelp">How can you help us? *</Label>
                <Textarea
                  id="howHelp"
                  value={formData.howHelp}
                  onChange={(e) => handleInputChange('howHelp', e.target.value)}
                  placeholder="What skills, ideas, or contributions can you bring to improve our community?"
                  rows={3}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="discordUsername">Discord Username or User ID *</Label>
                <Input
                  id="discordUsername"
                  value={formData.discordUsername}
                  onChange={(e) => handleInputChange('discordUsername', e.target.value)}
                  placeholder="your_username#1234 or 123456789012345678"
                  required
                />
              </div>

              <Button 
                type="submit" 
                variant="heart" 
                size="lg" 
                className="w-full glow-effect" 
                disabled={isSubmitting}
              >
                {isSubmitting ? (
                  "Submitting..."
                ) : (
                  <>
                    <Send className="w-5 h-5 mr-2" />
                    Submit Application
                  </>
                )}
              </Button>

              <p className="text-sm text-muted-foreground text-center">
                * All fields are required. We'll review your application and get back to you soon!
              </p>
            </form>
          </CardContent>
        </Card>
      </div>
    </section>
  );
};

export default StaffApplicationForm;