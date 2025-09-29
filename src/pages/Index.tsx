import CustomCursor from '@/components/CustomCursor';
import FloatingHearts from '@/components/FloatingHearts';
import HeroSection from '@/components/HeroSection';
import FeaturesSection from '@/components/FeaturesSection';
import MinecraftSection from '@/components/MinecraftSection';
import TestimonialsSection from '@/components/TestimonialsSection';
import MusicToggle from '@/components/MusicToggle';
import Footer from '@/components/Footer';

const Index = () => {
  return (
    <div className="min-h-screen bg-background relative">
      {/* Background Effects */}
      <FloatingHearts />
      <CustomCursor />
      
      {/* Main Content */}
      <main className="relative z-10">
        <HeroSection />
        <FeaturesSection />
        <MinecraftSection />
        <TestimonialsSection />
      </main>
      
      {/* Footer */}
      <Footer />
      
      {/* Music Toggle */}
      <MusicToggle />
    </div>
  );
};

export default Index;
