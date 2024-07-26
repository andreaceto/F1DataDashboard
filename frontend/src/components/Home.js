import React, { useEffect, useState } from 'react';
import Header from './Header.js';
import Footer from './Footer.js';
import '../styles/Home.css';

const Home = () => {
    const [data, setData] = useState(null);
    const [selectedStandings, setSelectedStandings] = useState('Drivers');
    const [showPlot, setShowPlot] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('http://127.0.0.1:5000/');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const result = await response.json();
                setData(result);
            } catch (error) {
                console.error('Error fetching the home data', error);
            }
        };

        fetchData();
    }, []);

    const renderDriverStandingsTable = (table) => {
        if (table.length === 0) {
            return (
                <div className='countdown-container'>
                    <div className="countdown">No results are currently available</div>
                </div>
            )
        } else {
            return(
                <div className="race-table">
                    <div className='standings-table-header'>
                        <h3 className='race-table_header'>2024 Driver Standings Table</h3>
                        <div className="standings-buttons">
                            <button 
                                className={`standings-button ${selectedStandings === 'Drivers' ? 'active' : ''}`} 
                                onClick={() => {
                                    setSelectedStandings('Drivers');
                                    setShowPlot(false);  // Reset plot view when changing standings
                                }}
                            >
                                Drivers
                            </button>
                            <button 
                                className={`standings-button ${selectedStandings === 'Constructors' ? 'active' : ''}`} 
                                onClick={() => {
                                    setSelectedStandings('Constructors');
                                    setShowPlot(false);  // Reset plot view when changing standings
                                }}
                            >
                                Teams
                            </button>
                        </div>
                    </div>
                    <table>
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Driver</th>
                                <th>Team</th>
                                <th>Points</th>
                                <th>Wins</th>
                                <th>Podiums</th>
                                <th>Poles</th>
                                <th className='th-fastest-lap-container'>
                                    <img className='th-fastest-lap' src="/fastest-lap.png" alt="Fastest Lap" />
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                            table.map((row, index) => (
                                <tr key={index}>
                                    <td className='race-table_pos'>
                                        <div className='race-table_pos_container'>
                                            <div className='race-table_pos_color' style={{ backgroundColor: row.TeamC }}></div>
                                            <span className='race-table_pos_text'>{row.Position}</span>
                                        </div>
                                    </td>
                                    <td className='race-table_driver'>
                                        <div className='race-table_driver_img'>
                                            <img className='race-table_driver_img_profile' src={`/pro_pic/${row.ProPic}`} alt={`${row.ProPic}`}></img>
                                            <img className='race-table_driver_img_nationality' src={`/flags/${row.NatFlag}`} alt={`${row.NatFlag}`}></img>
                                        </div>
                                        <div className='race-table_driver_name'>{row.Name} {row.Surname}</div>
                                    </td>
                                    <td className='race-table_team'>
                                    <div className='home-table-team-logo-wrapper'>
                                        <img className='home-table-team-logo' src={`/team_logos/${row.TeamLogo}`} alt={`${row.TeamLogo}`}></img>
                                    </div>
                                    </td>
                                    <td className='home-table-points'>{row.Points}</td>
                                    <td className='home-table-stats'>
                                        <div className='home-table-stats-container'>
                                            <div className='home-table-stats-primary'>{row.Wins}</div>
                                            <div className='home-table-stats-secondary'>+{row.SprintWins}*</div>
                                        </div>
                                    </td>
                                    <td className='home-table-stats'>
                                        <div className='home-table-stats-container'>
                                            <div className='home-table-stats-primary'>{row.Podiums}</div>
                                            <div className='home-table-stats-secondary'>+{row.SprintPodiums}*</div>
                                        </div>
                                    </td>
                                    <td className='home-table-stats'>
                                        <div className='home-table-stats-container'>
                                            <div className='home-table-stats-primary'>{row.Poles}</div>
                                            <div className='home-table-stats-secondary'>+{row.SprintPoles}*</div>
                                        </div>
                                    </td>
                                    <td className='home-table-fastest-laps'>{row.FastestLaps}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    <div className='home-table-disclaimer-wrapper'>
                        <div className='home-table-disclaimer'>* Sprint stats</div>
                        <button 
                        className={`show-plot-button ${showPlot ? 'hide' : 'show'}`} 
                        onClick={() => setShowPlot(!showPlot)}
                        >
                            <img className='show-plot-button-icon' src='/icons8-grafico-96.png' alt='icons8-grafico-96.png'></img>
                        </button>
                    </div>
                </div>
            )
        }
    };

    const renderConstructorStandingsTable = (table) => {
        if (table.length === 0) {
            return (
                <div className='countdown-container'>
                    <div className="countdown">No results are currently available</div>
                </div>
            )
        } else {
            return(
                <div className="race-table">
                    <div className='standings-table-header'>
                        <h3 className='race-table_header'>2024 Constructor Standings Table</h3>
                        <div className="standings-buttons">
                            <button 
                                className={`standings-button ${selectedStandings === 'Drivers' ? 'active' : ''}`} 
                                onClick={() => {
                                    setSelectedStandings('Drivers');
                                    setShowPlot(false);  // Reset plot view when changing standings
                                }}
                            >
                                Drivers
                            </button>
                            <button 
                                className={`standings-button ${selectedStandings === 'Constructors' ? 'active' : ''}`} 
                                onClick={() => {
                                    setSelectedStandings('Constructors');
                                    setShowPlot(false);  // Reset plot view when changing standings
                                }}
                            >
                                Teams
                            </button>
                        </div>
                    </div>
                    <table>
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Team</th>
                                <th>Drivers</th>
                                <th>Points</th>
                                <th>Wins</th>
                                <th>Podiums</th>
                                <th>Poles</th>
                                <th className='th-fastest-lap-container'>
                                    <img className='th-fastest-lap' src="/fastest-lap.png" alt="Fastest Lap" />
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                            table.map((row, index) => (
                                <tr key={index}>
                                    <td className='race-table_pos'>
                                        <div className='race-table_pos_container'>
                                            <div className='race-table_pos_color' style={{ backgroundColor: row.TeamC }}></div>
                                            <span className='race-table_pos_text'>{row.Position}</span>
                                        </div>
                                    </td>
                                    <td className='const-table-team'>
                                        <div className='const-table-car-img-wrapper'>
                                            <img className='const-table-car-img' src={`/cars/${row.Car}`} alt={`${row.Car}`}></img>                                        </div>
                                        <div className='const-table-team-name'>{row.Constructor}</div>
                                    </td>
                                    <td className='const-table-drivers'>
                                    <div className='const-table-driver-names-wrapper'>
                                        <div className='const-table-driver-names'>{row.Drivers.join(', ')}</div>
                                    </div>
                                    </td>
                                    <td className='home-table-points'>{row.Points}</td>
                                    <td className='home-table-stats'>
                                        <div className='home-table-stats-container'>
                                            <div className='home-table-stats-primary'>{row.Wins}</div>
                                            <div className='home-table-stats-secondary'>+{row.SprintWins}*</div>
                                        </div>
                                    </td>
                                    <td className='home-table-stats'>
                                        <div className='home-table-stats-container'>
                                            <div className='home-table-stats-primary'>{row.Podiums}</div>
                                            <div className='home-table-stats-secondary'>+{row.SprintPodiums}*</div>
                                        </div>
                                    </td>
                                    <td className='home-table-stats'>
                                        <div className='home-table-stats-container'>
                                            <div className='home-table-stats-primary'>{row.Poles}</div>
                                            <div className='home-table-stats-secondary'>+{row.SprintPoles}*</div>
                                        </div>
                                    </td>
                                    <td className='home-table-fastest-laps'>{row.FastestLaps}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                        <div className='home-table-disclaimer-wrapper'>
                            <div className='home-table-disclaimer'>* Sprint stats</div>
                            <button 
                            className={`show-plot-button ${showPlot ? 'hide' : 'show'}`} 
                            onClick={() => setShowPlot(!showPlot)}
                            >
                                <img className='show-plot-button-icon' src='/icons8-grafico-96.png' alt='icons8-grafico-96.png'></img>
                            </button>
                        </div>
                    </div>
            )
        }
    };

    const renderPlot = (src, plotType) => {
        return (
            <div className='home-chart-container'>
                <div className='home-chart-header'>2024 {plotType} Evolution Chart</div>
                <img src={src} alt={`${plotType} Evolution Chart`} />
            </div>
        );
    };


    return (
        <>
        <Header/>
        <div className='home-main-container'>
            {selectedStandings === 'Drivers' && data && renderDriverStandingsTable(data.driver_standings_table)}
            {selectedStandings === 'Drivers' && showPlot && renderPlot(data.driver_championship_plot_path, 'Driver Standings')}
            {selectedStandings === 'Constructors' && data && renderConstructorStandingsTable(data.constructor_standings_table)}
            {selectedStandings === 'Constructors' && showPlot && renderPlot(data.constructor_championship_plot_path, 'Constructor Standings')}
        </div>
        <Footer/>
        </>
    );
};

export default Home;
