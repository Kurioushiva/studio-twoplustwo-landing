import React from 'react';
import { Mail, Phone } from 'lucide-react';

const ContactPreviewSection = () => {
  return (
    <section className="py-20 md:py-24 px-8 md:px-16 lg:px-24 bg-stone-50">
      <div className="max-w-2xl mx-auto text-center">
        <div className="space-y-8">
          <p className="text-lg font-light text-stone-700">
            Or reach us directly at:
          </p>
          
          <div className="flex flex-col md:flex-row justify-center items-center space-y-4 md:space-y-0 md:space-x-12">
            <a 
              href="mailto:hello@studioname.com" 
              className="flex items-center space-x-3 text-stone-700 hover:text-sage-600 transition-colors duration-300 group"
            >
              <Mail className="w-5 h-5 group-hover:scale-110 transition-transform duration-300" />
              <span className="font-light">hello@studioname.com</span>
            </a>
            
            <a 
              href="tel:+919876543210" 
              className="flex items-center space-x-3 text-stone-700 hover:text-sage-600 transition-colors duration-300 group"
            >
              <Phone className="w-5 h-5 group-hover:scale-110 transition-transform duration-300" />
              <span className="font-light">+91 98765 43210</span>
            </a>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ContactPreviewSection;