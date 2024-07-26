import React from 'react';
import { Link } from 'react-router-dom'; // Importa Link da react-router-dom
import '../styles/Header.css'; // Assicurati di creare il file CSS corrispondente

const Header = () => {
  return (
    <header className="header">
      <div className="logo">
        <Link to="/">
          <img src={`${process.env.PUBLIC_URL}/F1_logo.png`} alt="F1-Logo" />
        </Link>
      </div>
      <nav className="nav">
        <ul>
          <li><Link to="/racestats/2024/1">RACES</Link></li>
          <li><Link to="/teams">TEAMS</Link></li>
          <li><Link to="/calendar">CALENDAR</Link></li>
          <li><Link to="/history">HISTORY</Link></li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
