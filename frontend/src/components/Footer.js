import React from 'react';
import '../styles/Footer.css'; // Make sure to create the corresponding CSS file

const Footer = () => {
  return (
    <footer className="footer">
      <div className="logoFooter">
        <img src={`${process.env.PUBLIC_URL}/F1_logo.png`} alt="F1-Logo" />
      </div>
      <div className="socialMedia">
        <a href="https://www.facebook.com/Formula1/" target="_blank" rel="noopener noreferrer">
          <img src={`${process.env.PUBLIC_URL}/footer/facebook.png`} alt="Facebook" />
        </a>
        <a href="https://x.com/f1" target="_blank" rel="noopener noreferrer">
          <img src={`${process.env.PUBLIC_URL}/footer/x.png`} alt="Twitter" />
        </a>
        <a href="https://www.instagram.com/f1/" target="_blank" rel="noopener noreferrer">
          <img src={`${process.env.PUBLIC_URL}/footer/instagram.png`} alt="Instagram" />
        </a>
        <a href="https://www.snapchat.com/p/f28863e5-1b20-4a6a-99a8-49d6aaf45680/1866141108289536?sender_web_id=f913c270-5a0e-4f49-95b1-6ce9f1ce9160&device_type=desktop&is_copy_url=true" target="_blank" rel="noopener noreferrer" className='snapchat'>
          <img src={`${process.env.PUBLIC_URL}/footer/snapchat.png`} alt="Snapchat" />
        </a>
        <a href="https://www.tiktok.com/@f1" target="_blank" rel="noopener noreferrer" className='tiktok'>
          <img src={`${process.env.PUBLIC_URL}/footer/tiktok.png`} alt="Tik Tok" />
        </a>
        
      </div>
      <div className="copyright">
        © 2024 Formula One World Championship Limited
      </div>
    </footer>
  );
};

export default Footer;
