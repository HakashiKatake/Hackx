// src/app/page.tsx
'use client';

import React from 'react';
import HeroGeometric from '@/components/HeroGeometric';
import FeaturesSection from '@/components/FeaturesSection';
import ClothReviewSection from '@/components/ClothReviewSection';
import GridMotion from '@/background/GridMotion/GridMotion';
import SplashCursor from '@/animations/SplashCursor/SplashCursor';

export default function LandingPage() {
  return (
    <>
      
      <HeroGeometric 
        badge="Featured" 
        title1="Elevate Your" 
        title2="Fashion Sense" 
      />
      <FeaturesSection />
      <GridMotion />
      
      
      {/* <ClothReviewSection />
      You can add additional sections here */}
      
    </>
  );
}
