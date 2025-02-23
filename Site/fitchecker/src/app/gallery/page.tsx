// src/app/gallery/page.tsx
'use client';

import React from 'react';
import CircularGallery from '@/components/CircularGallery/CircularGallery';

export type GalleryItem = {
  id: number;
  bgColor: string;
  icon: React.ReactNode;
  title: string;
  desc: string;
};

// Sample data array that satisfies the CircularGalleryProps type.
const galleryData: GalleryItem[] = [
  {
    id: 1,
    bgColor: "#F54748",
    icon: <span>📷</span>,
    title: "Item 1",
    desc: "Lorem Ipsum is simply dummy text.",
  },
  {
    id: 2,
    bgColor: "#7952B3",
    icon: <span>🍹</span>,
    title: "Item 2",
    desc: "Lorem Ipsum has been the industry's standard.",
  },
  {
    id: 3,
    bgColor: "#1597BB",
    icon: <span>🐉</span>,
    title: "Item 3",
    desc: "Lorem Ipsum is simply dummy text.",
  },
  {
    id: 4,
    bgColor: "#185ADB",
    icon: <span>⚽</span>,
    title: "Item 4",
    desc: "Lorem Ipsum has been the industry's standard.",
  },
  {
    id: 5,
    bgColor: "#FF616D",
    icon: <span>🚁</span>,
    title: "Item 5",
    desc: "Lorem Ipsum is simply dummy text.",
  },
];

export default function GalleryPage() {
  return (
    <div className="min-h-screen bg-gray-900 flex flex-col items-center justify-center p-8">
      <h1 className="text-4xl font-bold text-white mb-8">Circular Gallery</h1>
      <div className="w-full max-w-3xl">
        <CircularGallery data={galleryData} activeSlide={0} />
      </div>
    </div>
  );
}
