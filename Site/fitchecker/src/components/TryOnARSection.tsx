// src/components/TryOnARSection.tsx
'use client';

import React from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';

export default function TryOnARSection() {
  return (
    <section className="py-20 bg-[#030303] text-white">
      <div className="container mx-auto px-4 text-center">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
          className="text-4xl md:text-5xl font-bold mb-6"
        >
          Try the Clothes on You with AR!
        </motion.h2>
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: 'easeOut', delay: 0.2 }}
          className="mb-8 text-lg max-w-2xl mx-auto"
        >
          Experience our augmented reality feature and see how our clothes look on you in real time. Click the button below to begin your AR journey.
        </motion.p>
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.4 }}
        >
          <Link href="/ar-preview">
            <button className="px-6 py-3 bg-gradient-to-r from-indigo-500 to-rose-500 text-white rounded-lg shadow-lg hover:opacity-90 transition">
              Try AR Now
            </button>
          </Link>
        </motion.div>
      </div>
    </section>
  );
}
