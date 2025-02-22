// src/app/page.tsx
'use client';

import React, { JSX } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, useGLTF } from '@react-three/drei';
import * as THREE from 'three';

// Component to load and display the jacket model
function JacketModel(props: JSX.IntrinsicElements['group']) {
  // Ensure the GLTF and textures are placed in public/Jacket/
  const { scene } = useGLTF('/Jacket/Jacket.gltf');
  return <primitive object={scene} {...props} />;
}

export default function LandingPage() {
  return (
    <div className="relative h-screen w-screen bg-gray-100 overflow-hidden">
      {/* Header */}
      <header className="absolute top-0 w-full p-4 text-center z-10">
        <h1 className="text-4xl font-bold text-gray-800">
          Welcome to Smart Fit Predictor
        </h1>
      </header>

      {/* Three.js Canvas fills the entire viewport */}
      <div className="w-full h-full">
        <Canvas camera={{ position: [0, 2, 5], fov: 50 }}>
          <ambientLight intensity={0.5} />
          <directionalLight intensity={0.8} position={[5, 5, 5]} />
          <JacketModel position={[0, -1, 0]} scale={[1.2, 1.2, 1.2]} />
          <OrbitControls
            enablePan={true}
            enableZoom={true}
            enableRotate={true}
            rotateSpeed={1.0}
            zoomSpeed={1.2}
            panSpeed={0.5}
            mouseButtons={{
              LEFT: THREE.MOUSE.ROTATE,
              MIDDLE: THREE.MOUSE.DOLLY,
              RIGHT: THREE.MOUSE.PAN,
            }}
          />
        </Canvas>
      </div>

      {/* Call-to-Action Button */}
      <div className="absolute bottom-10 w-full flex justify-center z-10">
        <button className="px-6 py-3 bg-blue-600 text-white rounded-lg shadow-lg hover:bg-blue-700 transition">
          Get Started
        </button>
      </div>
    </div>
  );
}
