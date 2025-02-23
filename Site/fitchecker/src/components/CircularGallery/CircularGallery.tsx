// src/components/CircularGallery/CircularGallery.tsx
import React, { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faChevronRight, faChevronLeft } from "@fortawesome/free-solid-svg-icons";

export type GalleryItem = {
  id: number;
  bgColor: string;
  icon: React.ReactNode;
  title: string;
  desc: string;
};

export type CircularGalleryProps = {
  data: GalleryItem[];
  activeSlide?: number;
};

const CircularGallery = (props: CircularGalleryProps) => {
  const { data, activeSlide: initialSlide = 0 } = props;
  const [activeSlide, setActiveSlide] = useState<number>(initialSlide);

  const next = () => {
    if (activeSlide < data.length - 1) setActiveSlide(activeSlide + 1);
  };

  const prev = () => {
    if (activeSlide > 0) setActiveSlide(activeSlide - 1);
  };

  const getStyles = (index: number) => {
    if (activeSlide === index)
      return {
        opacity: 1,
        transform: "translateX(0px) translateZ(0px) rotateY(0deg)",
        zIndex: 10,
      };
    else if (activeSlide - 1 === index)
      return {
        opacity: 1,
        transform: "translateX(-240px) translateZ(-400px) rotateY(35deg)",
        zIndex: 9,
      };
    else if (activeSlide + 1 === index)
      return {
        opacity: 1,
        transform: "translateX(240px) translateZ(-400px) rotateY(-35deg)",
        zIndex: 9,
      };
    else if (activeSlide - 2 === index)
      return {
        opacity: 1,
        transform: "translateX(-480px) translateZ(-500px) rotateY(35deg)",
        zIndex: 8,
      };
    else if (activeSlide + 2 === index)
      return {
        opacity: 1,
        transform: "translateX(480px) translateZ(-500px) rotateY(-35deg)",
        zIndex: 8,
      };
    else if (index < activeSlide - 2)
      return {
        opacity: 0,
        transform: "translateX(-480px) translateZ(-500px) rotateY(35deg)",
        zIndex: 7,
      };
    else if (index > activeSlide + 2)
      return {
        opacity: 0,
        transform: "translateX(480px) translateZ(-500px) rotateY(-35deg)",
        zIndex: 7,
      };
    return {};
  };

  return (
    <>
      {/* Carousel Container */}
      <div
        className="relative mx-auto"
        style={{
          perspective: "1000px",
          transformStyle: "preserve-3d",
          width: "362px",
          height: "272px",
        }}
      >
        {data.map((item, i) => (
          <React.Fragment key={item.id}>
            {/* Slide */}
            <div
              className="w-[362px] h-[272px] absolute top-0 rounded-[12px] flex items-center justify-center transition-all duration-500 ease-out"
              style={{
                background: item.bgColor,
                boxShadow: `0 5px 20px ${item.bgColor}30`,
                ...getStyles(i),
              }}
            >
              <SliderContent {...item} />
            </div>
            {/* Reflection */}
            <div
              className="absolute w-full h-[60px] bottom-[-60px] rounded-[12px] transition-all duration-500 ease-out"
              style={{
                background: `linear-gradient(to bottom, ${item.bgColor}40, transparent)`,
                ...getStyles(i),
              }}
            />
          </React.Fragment>
        ))}
      </div>
      {/* Navigation Buttons */}
      <div className="pt-[100px] flex justify-center">
        <FontAwesomeIcon
          className="cursor-pointer"
          onClick={prev}
          icon={faChevronLeft}
          color="#fff"
          size="2x"
        />
        <FontAwesomeIcon
          className="cursor-pointer ml-[40px]"
          onClick={next}
          icon={faChevronRight}
          color="#fff"
          size="2x"
        />
      </div>
    </>
  );
};

const SliderContent = (props: GalleryItem) => {
  return (
    <div
      className="flex flex-col text-white p-[30px] items-start"
      style={{
        fontFamily:
          '"Lucida Sans", "Lucida Sans Regular", "Lucida Grande", "Lucida Sans Unicode", Geneva, Verdana, sans-serif',
      }}
    >
      {props.icon}
      <h2 className="my-4">{props.title}</h2>
      <p className="mb-4">{props.desc}</p>
    </div>
  );
};

export default CircularGallery;
