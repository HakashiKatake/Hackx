// src/components/AboutSection.tsx
'use client';

import { motion } from 'framer-motion';

export default function AboutSection() {
  const fadeInVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: (custom: number) => ({
      opacity: 1,
      y: 0,
      transition: { delay: 0.3 + custom * 0.2, duration: 0.8, ease: 'easeOut' },
    }),
  };

  return (
    <section className="py-20 bg-[#030303] text-white">
      <div className="container mx-auto px-4 text-center">
        <motion.h2
          custom={0}
          variants={fadeInVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          className="text-4xl md:text-5xl font-bold mb-6"
        >
          About Us
        </motion.h2>
        <motion.p
          custom={1}
          variants={fadeInVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          className="max-w-2xl mx-auto text-lg leading-relaxed"
        >
          We are a cutting-edge fashion tech company committed to redefining how you experience personalized style. Our passion for innovative design and advanced AI fuels bespoke recommendations and immersive digital experiences that elevate your wardrobe.
        </motion.p>
      </div>
    </section>
  );
}
