// src/components/CheckClothes3DSection.tsx
'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ClothReviewSection from './ClothReviewSection';

export default function CheckClothes3DSection() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <section className="py-20 bg-[#030303] text-white">
      <div className="container mx-auto px-4 text-center">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
          className="text-4xl md:text-5xl font-bold mb-6"
        >
          Check the Clothes in 3D!
        </motion.h2>
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: 'easeOut', delay: 0.2 }}
          className="mb-8 text-lg max-w-2xl mx-auto"
        >
          Interact with our 3D models to see every detail and experience the quality up close.
        </motion.p>
        <button
          onClick={() => setIsOpen(true)}
          className="px-6 py-3 bg-gradient-to-r from-indigo-500 to-rose-500 text-white rounded-lg shadow-lg hover:opacity-90 transition"
        >
          View in 3D
        </button>
      </div>

      {/* Modal */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="fixed inset-0 z-50 flex items-center justify-center"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            {/* Overlay */}
            <motion.div
              className="absolute inset-0 bg-black opacity-70"
              onClick={() => setIsOpen(false)}
            />

            {/* Modal Content */}
            <motion.div
              className="relative bg-[#030303] rounded-xl shadow-xl p-6 max-w-4xl w-full mx-4"
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.8, opacity: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-2xl font-bold">3D Cloth Viewer</h3>
                <button
                  className="text-white text-2xl leading-none"
                  onClick={() => setIsOpen(false)}
                >
                  &times;
                </button>
              </div>
              <div className="w-full h-[500px]">
                <ClothReviewSection />
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </section>
  );
}
