// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Other Next.js config options...
  eslint: {
    // Warning: This allows production builds to successfully complete even if there are ESLint errors.
    ignoreDuringBuilds: true,
  },
};

module.exports = nextConfig;
