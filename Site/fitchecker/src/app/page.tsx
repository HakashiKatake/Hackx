// src/app/page.tsx
'use client';

import React from 'react';
import HeroGeometric from '@/components/HeroGeometric';
import FeaturesSection from '@/components/FeaturesSection';
import CheckClothes3DSection from '@/components/CheckClothes3DSection';
import GridMotion from '@/background/GridMotion/GridMotion';
import AboutSection from '@/components/AboutSection';
import FAQSection from '@/components/FAQSection';
import TryOnARSection from '@/components/TryOnARSection';

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
      
      <GridMotion />
      <AboutSection />
      <FAQSection />
      
      


      
      
      {/* <ClothReviewSection />
      You can add additional sections here */}
      
    </>
  );
}
