import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Header from './Header.js';
import Footer from './Footer.js';
import '../styles/Calendar.css';

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
    const startMonth = startDate.toLocaleString('en-EN', { month: 'short' });
    const endDay = endDate.getDate();
    const endMonth = endDate.toLocaleString('en-EN', { month: 'short' });

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
    <Header /> {}
    <div className="cal-calendar-container">
      <img src={`${process.env.PUBLIC_URL}/calendar/calendar_logo.png`} alt="Calendar Logo" className="cal-calendar-logo"/>
      <div className="cal-calendar-grid">
        {calendar.map((race, index) => (
          <Link to={`/racestats/${race.year}/${race.round}`} className="cal-calendar-item" key={index}>
            <div className={`cal-round ${isRacePast(race.date) ? 'past' : ''}`}>R{index + 1}</div>
            <div className="cal-race-info">
              <div className="cal-race-flag">
                <img src={race.flag} alt={`${race.location} flag`} />
              </div>
              <div className="cal-race-name">{race.name}</div>
              <div className="cal-race-location">{race.location}</div>
              <div className="cal-race-date">{formatDate(race.date)}</div>
            </div>
          </Link>
        ))}
      </div>
    </div>
    <Footer /> {}
    </>
  );
};

export default Calendar;
