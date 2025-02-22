// src/app/layout.tsx
import './globals.css';
import { Inter } from 'next/font/google';
import SplashCursor from '@/animations/SplashCursor/SplashCursor'; // Adjust the import if necessary

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'My App',
  description: 'My app description',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className + " relative"}>
        {/* Render the splash cursor on every page */}
        <SplashCursor />
        {children}
      </body>
    </html>
  );
}
