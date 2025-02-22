// src/components/ClothReviewSection.tsx
'use client';

import React, { JSX, useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, useGLTF } from '@react-three/drei';
import * as THREE from 'three';

function ClothModel(props: JSX.IntrinsicElements['group']) {
  // Ensure that your model and its textures are in public/Cloth/
  const { scene } = useGLTF('/Jacket/Jacket.gltf');
  return <primitive object={scene} {...props} />;
}

export default function ClothReviewSection() {
  const [active, setActive] = useState(false);

  return (
    <section
      className="relative w-full h-screen"
      // When the mouse enters this section, enable pointer events (for 3D interaction)
      onMouseEnter={() => setActive(true)}
      // When the mouse leaves, disable pointer events so that scrolling works
      onMouseLeave={() => setActive(false)}
    >
      <div className={`absolute inset-0 ${active ? 'pointer-events-auto' : 'pointer-events-none'}`}>
        <Canvas camera={{ position: [0, 2, 5], fov: 50 }}>
          <ambientLight intensity={0.5} />
          <directionalLight intensity={0.8} position={[5, 5, 5]} />
          <ClothModel position={[0, -1, 0]} scale={[1.2, 1.2, 1.2]} />
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
    </section>
  );
}
