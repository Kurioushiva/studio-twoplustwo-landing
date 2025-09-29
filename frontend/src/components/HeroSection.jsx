import React from 'react';

const HeroSection = () => {
  return (
    <section className="relative min-h-screen flex items-center justify-center bg-stone-50 px-8 md:px-16 lg:px-24">
      {/* Background placeholder - can be replaced with actual image */}
      <div className="absolute inset-0 bg-gradient-to-br from-stone-100 to-stone-200 opacity-30"></div>
      
      <div className="relative z-10 max-w-4xl mx-auto text-center space-y-12">
        <h1 className="font-serif text-5xl md:text-7xl lg:text-8xl font-light text-stone-900 leading-[1.1] tracking-tight">
          Something Extraordinary
          <br />
          <span className="text-sage-600">is Coming</span>
        </h1>
        
        <div className="space-y-8">
          <p className="text-xl md:text-2xl font-light text-stone-700 leading-relaxed max-w-2xl mx-auto">
            We're crafting a new digital home for our
            <br className="hidden md:block" />
            architecture and interior design practice
          </p>
          
          <div className="inline-block">
            <div className="bg-white/80 backdrop-blur-sm px-8 py-4 rounded-sm border border-stone-200">
              <p className="text-base text-stone-600 font-medium tracking-wide">
                Launching post-Diwali 2025
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;