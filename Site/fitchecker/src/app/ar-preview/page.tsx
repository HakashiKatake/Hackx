'use client';

import React from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';

export default function ARPreviewPage() {
  return (
    <div className="min-h-screen bg-[#030303] text-white flex flex-col items-center justify-center p-4 space-y-16">
      <h1 className="text-4xl md:text-5xl font-bold mb-8">AR Preview</h1>
      
      {/* Desktop AR Preview Section */}
      <section className="w-full max-w-6xl">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
          className="text-4xl md:text-5xl font-bold mb-6 text-center"
        >
         
        </motion.h2>
        <div className="flex flex-col md:flex-row gap-8 w-full">
          {/* Before Video Container */}
          <motion.div
            className="relative flex-1 aspect-square rounded-lg overflow-hidden shadow-lg"
            initial={{ opacity: 0, scale: 0.8 }}
            whileInView={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
          >
            <video
              src="/before.mp4"
              autoPlay
              loop
              muted
              playsInline
              className="object-cover w-full h-full"
            />
            <div className="absolute top-2 right-2 bg-black bg-opacity-50 px-2 py-1 rounded text-sm font-bold">
              Before
            </div>
          </motion.div>
          {/* After Video Container */}
          <motion.div
            className="relative flex-1 aspect-square rounded-lg overflow-hidden shadow-lg"
            initial={{ opacity: 0, scale: 0.8 }}
            whileInView={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <video
              src="/after.mp4"
              autoPlay
              loop
              muted
              playsInline
              className="object-cover w-full h-full"
            />
            <div className="absolute top-2 right-2 bg-black bg-opacity-50 px-2 py-1 rounded text-sm font-bold">
              After
            </div>
          </motion.div>
        </div>
      </section>
      
      {/* Mobile Preview Section */}
      <section className="w-full max-w-4xl">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
          className="text-4xl md:text-5xl font-bold mb-6 text-center"
        >
          See how it looks in mobile!
        </motion.h2>
        <div className="flex flex-col md:flex-row gap-8 justify-center items-center">
          {/* Before Mobile Preview Container */}
          <motion.div
            className="relative flex-1 md:max-w-[250px] aspect-[9/16] rounded-lg overflow-hidden shadow-lg"
            initial={{ opacity: 0, scale: 0.8 }}
            whileInView={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
          >
            <video
              src="/bmobile.mp4"
              autoPlay
              loop
              muted
              playsInline
              className="object-cover w-full h-full"
            />
            <div className="absolute top-2 right-2 bg-black bg-opacity-50 px-2 py-1 rounded text-sm font-bold">
              Before
            </div>
          </motion.div>
          {/* After Mobile Preview Container */}
          <motion.div
            className="relative flex-1 md:max-w-[250px] aspect-[9/16] rounded-lg overflow-hidden shadow-lg"
            initial={{ opacity: 0, scale: 0.8 }}
            whileInView={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <video
              src="/amobile.mp4"
              autoPlay
              loop
              muted
              playsInline
              className="object-cover w-full h-full"
            />
            <div className="absolute top-2 right-2 bg-black bg-opacity-50 px-2 py-1 rounded text-sm font-bold">
              After
            </div>
          </motion.div>
        </div>
      </section>
      
      <Link href="/" className="mt-8 text-blue-500 hover:underline">
        Back to Home
      </Link>
    </div>
  );
}
