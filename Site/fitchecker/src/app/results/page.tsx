import React from 'react';

const Page = () => {
  return (
    <>
      <nav className="h-[100px] w-full bg-[3f3f46] text-white flex items-center justify-between px-6 shadow-lg">
        <h1 className="text-2xl font-bold">Get Your Size</h1>
        <ul className="flex space-x-6">
          <li className="hover:text-gray-400 cursor-pointer"><a href="https://rohanvashisht-hackx.hf.space/">Open in Tab</a></li>
        </ul>
      </nav>
      <embed className="w-screen h-[calc(100vh-100px)]" src="https://rohanvashisht-hackx.hf.space/"></embed>
    </>
  );
};

export default Page;