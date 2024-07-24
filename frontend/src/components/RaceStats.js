import React, { useEffect, useState } from 'react';
import Header from './Header.js';
import Footer from './Footer.js';
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
    const [qualifyingTable, setQualifyingTable] = useState([]);
    const [raceTable, setRaceTable] = useState([]);
    const [sprintTable, setSprintTable] = useState([]);
    const [selectedTable, setSelectedTable] = useState('qualifying'); // 'qualifying', 'race', 'sprint'
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

    const fetchQualifyingTable = async (raceId) => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/racestats/qualifying/${raceId}`);
            const data = await response.json();
            setQualifyingTable(data);
        } catch (error) {
            console.error('Error fetching qualifying table', error);
        }
    };

    const fetchRaceTable = async (raceId) => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/racestats/race/${raceId}`);
            const data = await response.json();
            setRaceTable(data);
        } catch (error) {
            console.error('Error fetching race table', error);
        }
    };

    const fetchSprintTable = async (raceId) => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/racestats/sprint/${raceId}`);
            const data = await response.json();
            setSprintTable(data);
        } catch (error) {
            console.error('Error fetching sprint table', error);
        }
    };

    useEffect(() => {
        if (raceData) {
            const currentTime = new Date().getTime();
            const raceTime = new Date(raceData.race.date + 'T' + raceData.race.time + 'Z').getTime();
            
            if (raceTime > currentTime) {
                return;
            } else {
                fetchQualifyingTable(raceData.race.raceId);
                fetchRaceTable(raceData.race.raceId);
                if (raceData.sprint_weekend === 'true') {
                    fetchSprintTable(raceData.race.raceId);
                }
            }
        }
    }, [raceData]);

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

    const renderQualiTable = (raceName, table, tableName) => {
        if (table.length === 0) {
            return (
                <div className='countdown-container'>
                    <div className="countdown">No results are currently available for {raceName} - {tableName} Session</div>
                </div>
            )
        } else {
            return (
                <div className="quali-table">
                    <h3 className='quali-table_header'>{raceName} - Qualifying Result</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Driver</th>
                                <th>Team</th>
                                <th>Time</th>
                            </tr>
                        </thead>
                        <tbody>
                            {table.map((row, index) => (
                                <tr key={index}>
                                    <td className='quali-table_pos'>
                                        <div className='quali-table_pos_container'>
                                            <div className='quali-table_pos_color' style={{ backgroundColor: row.team_color }}></div>
                                            <span className='quali-table_pos_text'>{row.position}</span>
                                        </div>
                                    </td>
                                    <td className='quali-table_driver'>
                                        <div className='quali-table_driver_img'>
                                            <img className='quali-table_driver_img_profile' src={`/pro_pic/${row.driver_pic}`} alt={`${row.driver_name} pro pic`}></img>
                                            <img className='quali-table_driver_img_nationality' src={`/flags/${row.driver_nat_flag}`} alt={`${row.driver_name} nationality`}></img>
                                        </div>
                                        <div className='quali-table_driver_name'>{row.driver_name}</div>
                                    </td>
                                    <td className='quali-table_team'>{row.team_name}</td>
                                    <td className='quali-table_time'>{row.time}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )
        }
    };

    const renderRaceTable = (raceName, table, tableName) => {
        if (table.length === 0) {
            return (
                <div className='countdown-container'>
                    <div className="countdown">No results are currently available for {raceName} - {tableName} Session</div>
                </div>
            )
        } else {
            return(
                <div className="race-table">
                    <h3 className='race-table_header'>{raceName} - {tableName} Result</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Driver</th>
                                <th>Team</th>
                                <th>Time</th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                            table.map((row, index) => (
                                <tr key={index}>
                                    <td className='race-table_pos'>
                                        <div className='race-table_pos_container'>
                                            <div className='race-table_pos_color' style={{ backgroundColor: row.team_color }}></div>
                                            <span className='race-table_pos_text'>{row.position}</span>
                                        </div>
                                    </td>
                                    <td className='race-table_driver'>
                                        <div className='race-table_driver_img'>
                                            <img className='race-table_driver_img_profile' src={`/pro_pic/${row.driver_pic}`} alt={`${row.driver_name} pro pic`}></img>
                                            <img className='race-table_driver_img_nationality' src={`/flags/${row.driver_nat_flag}`} alt={`${row.driver_name} nationality`}></img>
                                        </div>
                                        <div className='race-table_driver_name'>{row.driver_name}</div>
                                        {row.fastest_lap && (
                                            <span className="fastest-lap-tooltip">
                                                <img className='tooltip-icon' src="/fastest-lap.png" alt="Fastest Lap" />
                                                <span className="tooltip-text">{row.fastest_lap}</span>
                                            </span>
                                        )}
                                    </td>
                                    <td className='race-table_team'>{row.team_name}</td>
                                    <td className='race-table_time'>{row.time}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )
        }
    };

    return (
        <>
        <Header/>
        <div className='main-container'>
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
                <div>
                    <div className='circuit-card-container'>
                        <div className='circuit-name-container'>
                            <h2 className='circuit-name'>{raceData.circuit.name}</h2>
                        </div>
                        <div className="circuit-card">
                            <img
                                src={raceData.additional_info.img_src}
                                alt={raceData.circuit.name}
                                className="circuit-image"
                            />
                            <div className="circuit-info">
                                <div className='circuit-info-heading'>Location
                                    <div className='circuit-info-data'>{raceData.circuit.location}, {raceData.circuit.country}</div>
                                </div>
                                <div className='circuit-info-heading'>First Grand Prix
                                    <div className='circuit-info-data'>{raceData.additional_info.first_gp}</div>
                                </div>
                                <div className='circuit-info-heading'>Number of Laps
                                    <div className='circuit-info-data'>{raceData.additional_info.laps}</div>
                                </div>
                                <div className='circuit-info-heading'>Circuit Length
                                    <div className='circuit-info-data'>{raceData.additional_info.length}
                                        <div className='circuit-info-unit'>km</div>
                                    </div>
                                </div>
                                <div className='circuit-info-heading'>Race Distance
                                    <div className='circuit-info-data'>{raceData.additional_info.race_distance}
                                        <div className='circuit-info-unit'>km</div>
                                    </div>
                                </div>
                                <div className='circuit-info-heading'>Lap Record
                                    <div className='circuit-info-data'>{raceData.additional_info.lap_record}
                                        <div className='circuit-info-unit'>{raceData.additional_info.record_holder}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div className="toggle-switch">
                        {raceData && raceData.sprint_weekend === 'true' ? (
                            <div className="three-way-toggle">
                                <label
                                    className={selectedTable === 'qualifying' ? 'toggle-on' : 'toggle-off'}
                                >
                                    <input
                                        type="radio"
                                        value="qualifying"
                                        checked={selectedTable === 'qualifying'}
                                        onChange={() => setSelectedTable('qualifying')}
                                    />
                                    Qualifying
                                </label>
                                <label
                                    className={selectedTable === 'sprint' ? 'toggle-on' : 'toggle-off'}
                                >
                                    <input
                                        type="radio"
                                        value="sprint"
                                        checked={selectedTable === 'sprint'}
                                        onChange={() => setSelectedTable('sprint')}
                                    />
                                    Sprint
                                </label>
                                <label
                                    className={selectedTable === 'race' ? 'toggle-on' : 'toggle-off'}
                                >
                                    <input
                                        type="radio"
                                        value="race"
                                        checked={selectedTable === 'race'}
                                        onChange={() => setSelectedTable('race')}
                                    />
                                    Race
                                </label>
                            </div>
                        ) : (
                            <div className="two-way-toggle">
                                <label
                                    className={selectedTable === 'qualifying' ? 'toggle-on' : 'toggle-off'}
                                >
                                    <input
                                        type="radio"
                                        value="qualifying"
                                        checked={selectedTable === 'qualifying'}
                                        onChange={() => setSelectedTable('qualifying')}
                                    />
                                    Qualifying
                                </label>
                                <label
                                    className={selectedTable === 'race' ? 'toggle-on' : 'toggle-off'}
                                >
                                    <input
                                        type="radio"
                                        value="race"
                                        checked={selectedTable === 'race'}
                                        onChange={() => setSelectedTable('race')}
                                    />
                                    Race
                                </label>
                            </div>
                        )}
                    </div>
                    {selectedTable === 'qualifying' && renderQualiTable(raceData.race.name, qualifyingTable, "Qualifying")}
                    {selectedTable === 'race' && renderRaceTable(raceData.race.name, raceTable, "Race")}
                    {selectedTable === 'sprint' && renderRaceTable(raceData.race.name, sprintTable, "Sprint Race")}
                </div>
            )}
        </div>
        <Footer/>
        </>
    );
};

export default RaceStats;
