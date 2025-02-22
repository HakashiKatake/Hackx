'use client';

import { motion } from "framer-motion";
import React, { JSX } from "react";

// A simple feature card component
interface FeatureCardProps {
  icon: JSX.Element;
  title: string;
  description: string;
  delay: number;
}

function FeatureCard({ icon, title, description, delay }: FeatureCardProps) {
  return (
    <motion.div
      className="p-6 bg-white/[0.05] border border-white/[0.1] rounded-lg shadow-lg backdrop-blur-md"
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay, duration: 0.6 }}
    >
      <div className="flex items-center justify-center h-12 w-12 rounded-full bg-gradient-to-r from-indigo-500 to-rose-500 mb-4">
        {icon}
      </div>
      <h3 className="text-xl font-semibold text-white mb-2">{title}</h3>
      <p className="text-white/60">{description}</p>
    </motion.div>
  );
}

export default function FeaturesSection() {
  return (
    <section className="py-20 bg-[#030303]">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <motion.div
          className="text-center mb-12"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="text-3xl md:text-4xl font-bold text-white">
            Our Features
          </h2>
          <p className="mt-4 text-white/60 max-w-xl mx-auto">
            Explore the cutting-edge features that make our Smart Fit Predictor truly unique.
          </p>
        </motion.div>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <FeatureCard
            icon={
              // Replace the below SVG with your own icon if desired
              <svg
                className="w-6 h-6 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M12 8c-1.657 0-3 1.343-3 3m6 0c0-1.657-1.343-3-3-3m0 0v6m0-6c1.657 0 3 1.343 3 3m-6-3c0 1.657-1.343 3-3 3m6 0v6m0-6c1.657 0 3 1.343 3 3"
                ></path>
              </svg>
            }
            title="3D Virtual Try-On"
            description="Experience your future look with our interactive 3D try-on feature."
            delay={0.2}
          />

          <FeatureCard
            icon={
              <svg
                className="w-6 h-6 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M9 12h6m2 0a2 2 0 110 4H7a2 2 0 110-4m10-4H7a2 2 0 100 4h10a2 2 0 100-4z"
                ></path>
              </svg>
            }
            title="Personalized Sizing"
            description="Receive size recommendations tailored to your unique body measurements."
            delay={0.4}
          />

          <FeatureCard
            icon={
              <svg
                className="w-6 h-6 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M12 8c-1.657 0-3 1.343-3 3m6 0c0-1.657-1.343-3-3-3m0 0v6m0-6c1.657 0 3 1.343 3 3m-6-3c0 1.657-1.343 3-3 3m6 0v6m0-6c1.657 0 3 1.343 3 3"
                ></path>
              </svg>
            }
            title="Custom Fit Options"
            description="Choose from slim, regular, or loose fits to match your style."
            delay={0.6}
          />
        </div>
      </div>
    </section>
  );
}
