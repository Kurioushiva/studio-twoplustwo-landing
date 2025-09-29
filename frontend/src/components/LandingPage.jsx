import React from 'react';
import HeroSection from './HeroSection';
import AboutSection from './AboutSection';
import SocialMediaSection from './SocialMediaSection';
import WhatToExpectSection from './WhatToExpectSection';
import ContactPreviewSection from './ContactPreviewSection';
import Footer from './Footer';

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-stone-50">
      <HeroSection />
      <AboutSection />
      <SocialMediaSection />
      <WhatToExpectSection />
      <ContactPreviewSection />
      <Footer />
    </div>
  );
};

export default LandingPage;