import React from 'react';

const AboutSection = () => {
  return (
    <section className="py-24 md:py-32 px-8 md:px-16 lg:px-24 bg-white">
      <div className="max-w-4xl mx-auto">
        <div className="space-y-16">
          <h2 className="font-serif text-4xl md:text-5xl font-light text-stone-900 text-center tracking-tight">
            Who We Are
          </h2>
          
          <div className="max-w-2xl mx-auto">
            <p className="text-lg md:text-xl font-light text-stone-700 leading-relaxed text-center">
              We are a contemporary architecture and interior design studio based in Ahmedabad, 
              specializing in thoughtful spaces that blend modern aesthetics with sustainable practices. 
              Our work spans architecture, interior design, master planning, and sustainable design solutions 
              that respond to both human needs and environmental consciousness.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AboutSection;