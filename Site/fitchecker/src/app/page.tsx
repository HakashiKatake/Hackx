import React from 'react';
import HeroGeometric from '@/components/HeroGeometric';
import FeaturesSection from '@/components/FeaturesSection';
import CheckClothes3DSection from '@/components/CheckClothes3DSection';
import AboutSection from '@/components/AboutSection';
import FAQSection from '@/components/FAQSection';
import TryOnARSection from '@/components/TryOnARSection';
import Link from 'next/link';

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
      <AboutSection />
      <FAQSection />

      {/* Floating Chat with AI Button at Right Corner */}
      <div className="fixed bottom-6 right-6 z-50">
        <Link href="/help" legacyBehavior>
          <a className="w-20 h-20 bg-blue-500 rounded-full flex items-center justify-center shadow-lg cursor-pointer transform transition hover:scale-110">
            <span className="text-white text-xs md:text-sm font-bold text-center">
              Chat with AI
            </span>
          </a>
        </Link>
      </div>
    </>
  );
}
