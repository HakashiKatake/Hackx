// src/components/FAQSection.tsx
'use client';

import { motion } from 'framer-motion';
import { useState } from 'react';

interface FAQItem {
  question: string;
  answer: string;
}

const faqs: FAQItem[] = [
  {
    question: 'How does Smart Fit Predictor work?',
    answer:
      'Our AI-driven technology calculates your body measurements and matches them to brand-specific size charts to recommend the perfect fit.',
  },
  {
    question: 'Can I customize my fit preference?',
    answer:
      'Absolutely! Choose between slim, regular, or loose fits to match your unique style.',
  },
  {
    question: 'Is my data secure?',
    answer:
      'We take data privacy seriously. All personal data is securely processed and never shared with third parties.',
  },
];

export default function FAQSection() {
  const fadeInVariants = {
    hidden: { opacity: 0, y: 10 },
    visible: (custom: number) => ({
      opacity: 1,
      y: 0,
      transition: { delay: 0.2 * custom, duration: 0.5, ease: 'easeOut' },
    }),
  };

  const [openIndex, setOpenIndex] = useState<number | null>(null);

  return (
    <section className="py-20 bg-[#030303] text-white">
      <div className="container mx-auto px-4">
        <motion.h2
          custom={0}
          variants={fadeInVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          className="text-4xl md:text-5xl font-bold mb-10 text-center"
        >
          Frequently Asked Questions
        </motion.h2>
        <div className="space-y-4 max-w-3xl mx-auto">
          {faqs.map((faq, index) => (
            <motion.div
              key={index}
              custom={index + 1}
              variants={fadeInVariants}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true }}
              className="border border-white/[0.15] rounded-lg p-4 cursor-pointer"
              onClick={() => setOpenIndex(openIndex === index ? null : index)}
            >
              <div className="flex justify-between items-center">
                <h3 className="text-xl font-semibold">{faq.question}</h3>
                <span className="text-2xl">{openIndex === index ? '-' : '+'}</span>
              </div>
              {openIndex === index && (
                <motion.p
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.3 }}
                  className="mt-2 text-base text-white/70"
                >
                  {faq.answer}
                </motion.p>
              )}
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
