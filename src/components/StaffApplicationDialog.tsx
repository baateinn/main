import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
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

const StaffApplicationDialog = () => {
  const { toast } = useToast();
  const [formData, setFormData] = useState<FormData>({
    age: '',
    experience: '',
    whyStaff: '',
    howHelp: '',
    discordUsername: '',
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

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
        
        // Reset form and close dialog
        setFormData({
          age: '',
          experience: '',
          whyStaff: '',
          howHelp: '',
          discordUsername: '',
        });
        setIsOpen(false);
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
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <Button variant="heart" size="lg" className="glow-effect">
          <Crown className="w-5 h-5 mr-2" />
          Staff Application
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto bg-card/50 backdrop-blur-sm border-border/50">
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold flex items-center gap-2 bg-gradient-secondary bg-clip-text text-transparent">
            <Crown className="w-6 h-6 text-secondary" />
            Staff Application
          </DialogTitle>
        </DialogHeader>
        
        <form onSubmit={handleSubmit} className="space-y-4">
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
              placeholder="Tell us about your previous experience as staff/moderator..."
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
              placeholder="What motivates you to join our staff team?"
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
              placeholder="What skills or contributions can you bring?"
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
      </DialogContent>
    </Dialog>
  );
};

export default StaffApplicationDialog;