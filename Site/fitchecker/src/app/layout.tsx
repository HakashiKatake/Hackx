// src/app/layout.tsx
import "./globals.css";
import { Inter } from "next/font/google";
import React from "react";
import SplashCursor from "@/animations/SplashCursor/SplashCursor"; // Adjust path if necessary
import DockWrapper from "@/components/DockWrapper"; // New client component

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "My App",
  description: "My app description",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`${inter.className} relative`}>
        {/* Render the SplashCursor on every page */}
        <SplashCursor />
        {children}
        {/* Render the Dock via the client component */}
        <DockWrapper />
      </body>
    </html>
  );
}
