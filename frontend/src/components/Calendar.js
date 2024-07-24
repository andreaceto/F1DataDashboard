import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/Calendar.css';
import React, { useEffect, useState } from 'react';
import Header from './Header.js';
import Footer from './Footer.js';

const Calendar = () => {
  const [calendar, setCalendar] = useState([]);

  useEffect(() => {
    const fetchCalendar = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/calendar');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const result = await response.json();
        setCalendar(result);
      } catch (error) {
        console.error('Errore nel recupero del calendario:', error);
      }
    };

    fetchCalendar();

    // Cambia il colore di sfondo del body quando il componente è montato
    document.body.style.backgroundColor = '#00010c';

    // Pulisci l'effetto quando il componente viene smontato
    return () => {
      document.body.style.backgroundColor = '';
    };
  }, []); // Dipendenza vuota per eseguire solo una volta all'avvio

  const formatDate = (dateString) => {
    const [start, end] = dateString.split(' - ');
    const startDate = new Date(start);
    const endDate = new Date(end);
    const startDay = startDate.getDate();
    const startMonth = startDate.toLocaleString('en-EN', { month: 'long' });
    const endDay = endDate.getDate();
    const endMonth = endDate.toLocaleString('en-EN', { month: 'long' });

    const capitalizeFirstLetter = (string) => {
      return string.charAt(0).toUpperCase() + string.slice(1);
    };

    if (startMonth === endMonth) {
      return `${startDay} - ${endDay} ${capitalizeFirstLetter(startMonth)}`;
    } else {
      return `${startDay} ${capitalizeFirstLetter(startMonth)} - ${endDay} ${capitalizeFirstLetter(endMonth)}`;
    }
  };

  const isRacePast = (dateString) => {
    const endDate = new Date(dateString.split(' - ')[1]);
    const today = new Date();
    return endDate < today;
  };

  return (
    <>
    <Header /> {/* Importa ed usa il componente Header */}
    <div className="calendar-container">
      <img src={`${process.env.PUBLIC_URL}/calendar/calendar_logo.png`} alt="Calendar Logo" className="calendar-logo"/>
      <div className="calendar-grid">
        {calendar.map((race, index) => (
          <Link to={`/racestats/${race.year}/${race.round}`} className="calendar-item" key={index}>
            <div className={`round ${isRacePast(race.date) ? 'past' : ''}`}>R{index + 1}</div>
            <div className="race-info">
              <div className="race-flag">
                <img src={race.flag} alt={`${race.location} flag`} />
              </div>
              <div className="cal-race-location">{race.location}</div>
              <div className="cal-race-name">{race.name}</div>
              <div className="cal-race-date">{formatDate(race.date)}</div>
            </div>
          </Link>
        ))}
      </div>
    </div>
    <Footer /> {/* Importa ed usa il componente Footer */}
    </>
  );
};

export default Calendar;
