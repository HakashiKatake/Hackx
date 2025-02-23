'use client';

import React from 'react';
import Chatbot from '@/components/ChatBot';
import { LiquidChrome } from '@/background/LiquidChrome/LiquidChrome'; // Adjust path if necessary
import Link from 'next/link';

export default function HelpPage() {
  return (
    <div className="relative min-h-screen bg-gray-900">
      {/* LiquidChrome background positioned absolutely */}
      <LiquidChrome className="absolute inset-0 z-0" />

      {/* Go Back to Home Button */}
      <div className="absolute top-6 left-6 z-20">
        <Link href="/" legacyBehavior>
          <a className="px-4 py-2 bg-blue-500 text-white rounded-md shadow-lg hover:bg-blue-600 transition">
            Go Back to Home
          </a>
        </Link>
      </div>

      {/* Content area where the Chatbot is rendered */}
      <div className="relative z-10 flex items-center justify-center p-4">
        <Chatbot />
      </div>
    </div>
  );
}
