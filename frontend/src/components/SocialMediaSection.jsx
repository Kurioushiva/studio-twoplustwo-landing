import React from 'react';
import { Instagram, Facebook, Linkedin } from 'lucide-react';
import { mockInstagramPosts } from '../data/mock';

const SocialMediaSection = () => {
  return (
    <section className="py-24 md:py-32 px-8 md:px-16 lg:px-24 bg-stone-50">
      <div className="max-w-6xl mx-auto">
        <div className="space-y-20">
          {/* Header */}
          <div className="text-center space-y-6">
            <h2 className="font-serif text-4xl md:text-5xl font-light text-stone-900 tracking-tight">
              Meanwhile, Find Us Here
            </h2>
            <p className="text-lg text-stone-600 font-light max-w-xl mx-auto">
              Stay connected with our latest projects and design inspiration
            </p>
          </div>

          {/* Instagram Grid */}
          <div className="space-y-12">
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 md:gap-6">
              {mockInstagramPosts.map((post, index) => (
                <div 
                  key={index}
                  className="aspect-square bg-stone-200 rounded-sm overflow-hidden hover:scale-[1.02] transition-transform duration-300 cursor-pointer group"
                >
                  <div className="w-full h-full bg-gradient-to-br from-stone-300 to-stone-400 flex items-center justify-center relative">
                    <div className="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-colors duration-300"></div>
                    <span className="text-stone-600 font-light text-sm opacity-60">
                      {post.type}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Social Links */}
          <div className="flex justify-center space-x-8">
            <a 
              href="#" 
              className="flex items-center space-x-3 text-stone-700 hover:text-sage-600 transition-colors duration-300 group"
            >
              <Instagram className="w-6 h-6 group-hover:scale-110 transition-transform duration-300" />
              <span className="font-light">Instagram</span>
            </a>
            <a 
              href="#" 
              className="flex items-center space-x-3 text-stone-700 hover:text-sage-600 transition-colors duration-300 group"
            >
              <Facebook className="w-6 h-6 group-hover:scale-110 transition-transform duration-300" />
              <span className="font-light">Facebook</span>
            </a>
            <a 
              href="#" 
              className="flex items-center space-x-3 text-stone-700 hover:text-sage-600 transition-colors duration-300 group"
            >
              <Linkedin className="w-6 h-6 group-hover:scale-110 transition-transform duration-300" />
              <span className="font-light">LinkedIn</span>
            </a>
          </div>
        </div>
      </div>
    </section>
  );
};

export default SocialMediaSection;