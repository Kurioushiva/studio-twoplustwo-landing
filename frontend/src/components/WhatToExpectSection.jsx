import React from 'react';
import { ArrowRight } from 'lucide-react';

const WhatToExpectSection = () => {
  const expectations = [
    'Portfolio of completed projects',
    'Our design philosophy and approach',
    'Services we offer',
    'Ways to connect with us'
  ];

  return (
    <section className="py-24 md:py-32 px-8 md:px-16 lg:px-24 bg-white">
      <div className="max-w-4xl mx-auto">
        <div className="space-y-16">
          <h2 className="font-serif text-4xl md:text-5xl font-light text-stone-900 text-center tracking-tight">
            What's Coming
          </h2>
          
          <div className="max-w-2xl mx-auto">
            <ul className="space-y-6">
              {expectations.map((item, index) => (
                <li key={index} className="flex items-center space-x-4 group">
                  <ArrowRight className="w-5 h-5 text-sage-600 flex-shrink-0 group-hover:translate-x-1 transition-transform duration-300" />
                  <span className="text-lg font-light text-stone-700">{item}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
};

export default WhatToExpectSection;