import React from 'react';
import HeroGeometric from '@/components/HeroGeometric';
import FeaturesSection from '@/components/FeaturesSection';
import CheckClothes3DSection from '@/components/CheckClothes3DSection';

import SplashCursor from '@/animations/SplashCursor/SplashCursor';
import AboutSection from '@/components/AboutSection';
import FAQSection from '@/components/FAQSection';
import TryOnARSection from '@/components/TryOnARSection';
import RollingGallery from '@/components/RollingGallery/RollingGallery';


export default function LandingPage() {
  return (
    <>
      <HeroGeometric 
        badge="Featured" 
        title1="Elevate Your" 
        title2="Fashion Sense" 
      />
     
      <CheckClothes3DSection />
      
      <TryOnARSection />
      <FeaturesSection />
      <RollingGallery />
     
      <AboutSection />
      <FAQSection />

      {/* Floating Chat with AI Button */}
      
    </>
  );
}
