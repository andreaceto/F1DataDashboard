import React, { useEffect, useState } from 'react';
import '../styles/RaceStats.css';

const raceFlags = {
    'Bahrain Grand Prix': 'bahrain.png',
    'Saudi Arabian Grand Prix': 'saudiarabia.png',
    'Australian Grand Prix': 'australia.png',
    'Japanese Grand Prix': 'japan.png',
    'Chinese Grand Prix': 'china.png',
    'Miami Grand Prix': 'usa.png',
    'Emilia Romagna Grand Prix': 'italy.png',
    'Monaco Grand Prix': 'monaco.png',
    'Canadian Grand Prix': 'canada.png',
    'Spanish Grand Prix': 'spain.png',
    'Austrian Grand Prix': 'austria.png',
    'British Grand Prix': 'uk.png',
    'Hungarian Grand Prix': 'hungary.png',
    'Belgian Grand Prix': 'belgium.png',
    'Dutch Grand Prix': 'netherlands.png',
    'Italian Grand Prix': 'italy.png',
    'Azerbaijan Grand Prix': 'azerbaijan.png',
    'Singapore Grand Prix': 'singapore.png',
    'United States Grand Prix': 'usa.png',
    'Mexico City Grand Prix': 'mexico.png',
    'São Paulo Grand Prix': 'brazil.png',
    'Las Vegas Grand Prix': 'usa.png',
    'Qatar Grand Prix': 'qatar.png',
    'Abu Dhabi Grand Prix': 'abudhabi.png'
};

const RaceStats = () => {
    const [calendar, setCalendar] = useState([]);
    const [selectedRound, setSelectedRound] = useState(1);
    const [raceData, setRaceData] = useState(null);
    const [year] = useState(new Date().getFullYear());

    useEffect(() => {
        const fetchCalendar = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:5000/racestats/calendar/${year}`);
                const data = await response.json();
                setCalendar(data);
            } catch (error) {
                console.error('Error fetching calendar', error);
            }
        };

        fetchCalendar();
    }, [year]);

    useEffect(() => {
        const fetchRaceData = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:5000/racestats/race/${year}/${selectedRound}`);
                const data = await response.json();
                setRaceData(data);
            } catch (error) {
                console.error('Error fetching race data', error);
            }
        };

        if (selectedRound) {
            fetchRaceData();
        }
    }, [selectedRound, year]);

    const handleNext = () => {
        setSelectedRound((prevRound) => (prevRound % calendar.length) + 1);
    };

    const handlePrevious = () => {
        setSelectedRound((prevRound) => (prevRound - 2 + calendar.length) % calendar.length + 1);
    };

    const formatEventPeriod = (fp1Date, raceDate) => {
        const start = new Date(fp1Date);
        const end = new Date(raceDate);

        const options = { day: 'numeric', month: 'short' };
        const formattedStart = start.toLocaleDateString('en-GB', options).toUpperCase().replace('.', '');
        const formattedEnd = end.toLocaleDateString('en-GB', options).toUpperCase().replace('.', '');

        return `${formattedStart} - ${formattedEnd}`;
    };

    const formatSessionDetails = (session) => {
        const date = new Date(session.date);
        const time = new Date(`1970-01-01T${session.time}Z`); // Assuming time is in UTC

        const dateOptions = { day: 'numeric', month: 'short', year: 'numeric' };
        const timeOptions = { hour: '2-digit', minute: '2-digit', hour12: false, timeZoneName: 'short' };
        const formattedDate = date.toLocaleDateString('en-GB', dateOptions).toUpperCase().replace('.', '');
        const formattedTime = time.toLocaleTimeString('en-GB', timeOptions);

        return { formattedDate, formattedTime };
    };

    const formatRaceName = (name, isSelected) => {
        if (isSelected) {
            return name.replace('Grand Prix', 'GP');
        } else {
            if (name.includes('United States') || name.includes('Paulo') || name.includes('Las Vegas') || name.includes('Abu Dhabi')) {
                return name.split(' ').slice(0, 2).join(' ');
            }
            return name.split(' ')[0];
        }
    };

    const getDisplayedRaces = () => {
        if (calendar.length === 0) return [];

        const totalRaces = calendar.length;
        const offset = 2;
        const races = [];

        for (let i = -offset; i <= offset; i++) {
            const index = (selectedRound - 1 + i + totalRaces) % totalRaces;
            races.push(calendar[index]);
        }

        return races;
    };

    const prevRaceIndex = (selectedRound - 2 + calendar.length) % calendar.length;
    const nextRaceIndex = selectedRound % calendar.length;

    return (
        <div className='main-container'>
            <h1>Race Stats</h1>
            <div className="race-selection">
                <div className="race-bar">
                    {getDisplayedRaces().map((race, index) => (
                        <div
                            key={race.round}
                            className={`race-item ${race.round === selectedRound ? 'selected' : ''}`}
                            onClick={() => setSelectedRound(race.round)}
                        >
                            <img src={`/flags/${raceFlags[race.name]}`} alt={`${race.name} flag`} className="race-flag" />
                            <div className="race-info">
                                <div className="race-name">{formatRaceName(race.name, race.round === selectedRound)}</div>
                                {race.round === selectedRound ? (
                                    <div className="session-details">
                                        {race.sessions.map((session, index) => {
                                            const { formattedDate, formattedTime } = formatSessionDetails(session);
                                            return (
                                                <div key={index} className="event">
                                                    <div className="event-type">{session.type}</div>
                                                    <div className="event-date">{formattedDate}</div>
                                                    <div className="event-time">{formattedTime}</div>
                                                </div>
                                            );
                                        })}
                                    </div>
                                ) : (
                                    <div className="race-date">{formatEventPeriod(race.fp1_date, race.date)}</div>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
                {calendar.length > 0 && (
                    <div className="navigation-buttons">
                        <button onClick={handlePrevious}>
                            &lt;
                            <img src={`/flags/${raceFlags[calendar[prevRaceIndex].name]}`} alt="Previous race" className="nav-flag" />
                        </button>
                        <button onClick={handleNext}>
                            <img src={`/flags/${raceFlags[calendar[nextRaceIndex].name]}`} alt="Next race" className="nav-flag" />
                            &gt;
                        </button>
                    </div>
                )}
            </div>

            {raceData && (
                <div className="race-card">
                    <img
                        src={raceData.additional_info.img_src}
                        alt={raceData.circuit.name}
                        className="circuit-image"
                    />
                    <div className="circuit-info">
                        <h2>{raceData.circuit.name}</h2>
                        <p className='circuit-info-heading'>Location</p>
                        <p className='circuit-info-data'>{raceData.circuit.location}, {raceData.circuit.country}</p>
                        <p className='circuit-info-heading'>First Grand Prix</p>
                        <p className='circuit-info-data'>{raceData.additional_info.first_gp}</p>
                        <p className='circuit-info-heading'>Number of Laps</p>
                        <p className='circuit-info-data'>{raceData.additional_info.laps}</p>
                        <p className='circuit-info-heading'>Circuit Length</p>
                        <p className='circuit-info-data'>{raceData.additional_info.length} <p className='circuit-info-unit'>km</p></p>
                        <p className='circuit-info-heading'>Race Distance</p>
                        <p className='circuit-info-data'>{raceData.additional_info.race_distance} <p className='circuit-info-unit'>km</p></p>
                        <p className='circuit-info-heading'>Lap Record</p>
                        <p className='circuit-info-data'>{raceData.additional_info.lap_record} <p className='circuit-info-unit'>{raceData.additional_info.record_holder}</p></p>
                    </div>
                </div>
            )}
        </div>
    );
};

export default RaceStats;
