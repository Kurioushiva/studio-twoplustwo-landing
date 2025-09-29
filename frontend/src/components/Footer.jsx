import React from 'react';
import { Instagram, Facebook, Linkedin, MapPin, Clock, Mail, Phone } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-stone-900 text-stone-300">
      {/* Main Footer Content */}
      <div className="px-8 md:px-16 lg:px-24 py-16 md:py-20">
        <div className="max-w-6xl mx-auto">
          {/* Studio Name & Tagline */}
          <div className="text-center mb-16">
            <h3 className="font-serif text-3xl md:text-4xl font-light text-white mb-4">
              [Studio Name]
            </h3>
            <p className="text-lg font-light text-stone-400">
              Crafting spaces that inspire and endure
            </p>
          </div>

          {/* Three Column Layout */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12 md:gap-8">
            {/* Column 1 - Contact Information */}
            <div className="space-y-6">
              <h4 className="font-medium text-white text-lg mb-6">Contact Information</h4>
              
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <Phone className="w-5 h-5 text-sage-400 flex-shrink-0" />
                  <a href="tel:+919876543210" className="font-light hover:text-white transition-colors duration-300">
                    +91 98765 43210
                  </a>
                </div>
                
                <div className="flex items-center space-x-3">
                  <Mail className="w-5 h-5 text-sage-400 flex-shrink-0" />
                  <a href="mailto:hello@studioname.com" className="font-light hover:text-white transition-colors duration-300">
                    hello@studioname.com
                  </a>
                </div>
                
                <div className="flex items-center space-x-3">
                  <Clock className="w-5 h-5 text-sage-400 flex-shrink-0" />
                  <span className="font-light">
                    Mon - Sat: 9:00 AM - 6:00 PM
                  </span>
                </div>
              </div>
            </div>

            {/* Column 2 - Address */}
            <div className="space-y-6">
              <h4 className="font-medium text-white text-lg mb-6">Our Studio</h4>
              
              <div className="space-y-3">
                <div className="flex items-start space-x-3">
                  <MapPin className="w-5 h-5 text-sage-400 flex-shrink-0 mt-1" />
                  <div className="font-light leading-relaxed">
                    <p>123 Design District,</p>
                    <p>Vastrapur, Ahmedabad,</p>
                    <p>Gujarat 380015</p>
                  </div>
                </div>
                
                <a 
                  href="#" 
                  className="inline-flex items-center text-sage-400 hover:text-sage-300 transition-colors duration-300 font-light ml-8"
                >
                  Get Directions →
                </a>
              </div>
            </div>

            {/* Column 3 - Connect */}
            <div className="space-y-6">
              <h4 className="font-medium text-white text-lg mb-6">Connect</h4>
              
              <div className="space-y-4">
                <p className="font-light text-stone-400 mb-6">Follow our journey</p>
                
                <div className="flex space-x-4">
                  <a 
                    href="#" 
                    className="w-10 h-10 bg-stone-800 rounded-sm flex items-center justify-center hover:bg-sage-600 transition-colors duration-300 group"
                  >
                    <Instagram className="w-5 h-5 group-hover:scale-110 transition-transform duration-300" />
                  </a>
                  <a 
                    href="#" 
                    className="w-10 h-10 bg-stone-800 rounded-sm flex items-center justify-center hover:bg-sage-600 transition-colors duration-300 group"
                  >
                    <Facebook className="w-5 h-5 group-hover:scale-110 transition-transform duration-300" />
                  </a>
                  <a 
                    href="#" 
                    className="w-10 h-10 bg-stone-800 rounded-sm flex items-center justify-center hover:bg-sage-600 transition-colors duration-300 group"
                  >
                    <Linkedin className="w-5 h-5 group-hover:scale-110 transition-transform duration-300" />
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-stone-800 px-8 md:px-16 lg:px-24 py-6">
        <div className="max-w-6xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <div className="flex flex-col md:flex-row items-center space-y-2 md:space-y-0 md:space-x-6">
              <p className="font-light text-stone-400">
                © 2025 [Studio Name]. All rights reserved.
              </p>
              <p className="font-light text-stone-500">
                Designed with passion in Ahmedabad
              </p>
            </div>
            
            <div className="flex space-x-6">
              <a href="#" className="font-light text-stone-400 hover:text-white transition-colors duration-300">
                Privacy Policy
              </a>
              <a href="#" className="font-light text-stone-400 hover:text-white transition-colors duration-300">
                Terms of Service
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;