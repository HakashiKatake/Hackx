'use client';

import React from 'react';
import HeroGeometric from '@/components/HeroGeometric';
import CheckClothes3DSection from '@/components/CheckClothes3DSection';
import TryOnARSection from '@/components/TryOnARSection';
import FeaturesSection from '@/components/FeaturesSection';
import AboutSection from '@/components/AboutSection';
import FAQSection from '@/components/FAQSection';
import CircularGallery, { GalleryItem } from '@/components/CircularGallery/CircularGallery';
import Link from 'next/link';
import { motion } from 'framer-motion';

// Sample data for the gallery with an image property added.
const galleryData: GalleryItem[] = [
  {
    id: 1,
    bgColor: "#F54748",
    icon: <span role="img" aria-label="camera">📷</span>,
    title: "Winter item",
    desc: "From the wardrobe of Zara",
    image: "/img2.jpeg",
  },
  {
    id: 2,
    bgColor: "#7952B3",
    icon: <span role="img" aria-label="cocktail">🍹</span>,
    title: "Summer item",
    desc: "From Gucci",
    image: "/img3.jpeg",
  },
  {
    id: 3,
    bgColor: "#1597BB",
    icon: <span role="img" aria-label="dragon">🐉</span>,
    title: "Summer item",
    desc: "From H&M",
    image: "/img1.jpeg",
  },
  {
    id: 4,
    bgColor: "#185ADB",
    icon: <span role="img" aria-label="soccer">⚽</span>,
    title: "Moonsoon item",
    desc: "From Zara",
    image: "/img4.jpeg",
  },
  {
    id: 5,
    bgColor: "#FF616D",
    icon: <span role="img" aria-label="helicopter">🚁</span>,
    title: "Winter item",
    desc: "From H&M",
    image: "/img5.jpeg",
  },
];

export default function LandingPage() {
  return (
    <>
      <HeroGeometric 
        badge="Swagger" 
        title1="Elevate Your" 
        title2="Fashion Sense" 
      />
      
      {/* Gallery Section with updated data */}
      <section className="py-20 bg-[#030303] text-white">
        <div className="container mx-auto px-4 text-center">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: 'easeOut' }}
            className="text-4xl md:text-5xl font-bold mb-8"
          >
            Gallery
          </motion.h2>
          <div className="w-full max-w-3xl mx-auto">
            <CircularGallery data={galleryData} activeSlide={0} />
          </div>
        </div>
      </section>

      <CheckClothes3DSection />
      <TryOnARSection />
      <FeaturesSection />
      <AboutSection />
      <FAQSection />

      
    </>
  );
}
