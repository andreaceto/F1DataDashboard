import React, { useEffect, useState } from 'react';
import Header from './Header.js';
import Footer from './Footer.js';
import '../styles/TeamSection.css';

const TeamSection = () => {
    const [teams, setTeams] = useState([]);
    const [selectedTeam, setSelectedTeam] = useState(6);  // Default to Ferrari (constructorId: 6)
    const [teamStats, setTeamStats] = useState(null);
    const [driverStats, setDriverStats] = useState([]);

    useEffect(() => {
        // Fetch the list of teams
        fetch('http://127.0.0.1:5000/teams')
            .then(response => response.json())
            .then(data => setTeams(data))
            .catch(error => console.error('Error fetching teams', error));
    }, []);

    useEffect(() => {
        if (selectedTeam) {
            // Fetch the stats for the selected team
            fetch(`http://127.0.0.1:5000/teams/${selectedTeam}`)
                .then(response => response.json())
                .then(data => {
                    setTeamStats(data.team);
                    setDriverStats(data.drivers);
                })
                .catch(error => console.error('Error fetching team stats', error));
        }
    }, [selectedTeam]);

    const handleNext = () => {
        setSelectedTeam((prevTeam) => {
            const currentIndex = teams.findIndex(team => team.constructorId === prevTeam);
            const nextIndex = (currentIndex + 1) % teams.length;
            return teams[nextIndex].constructorId;
        });
    };

    const handlePrevious = () => {
        setSelectedTeam((prevTeam) => {
            const currentIndex = teams.findIndex(team => team.constructorId === prevTeam);
            const prevIndex = (currentIndex - 1 + teams.length) % teams.length;
            return teams[prevIndex].constructorId;
        });
    };

    const getDisplayedTeams = () => {
        if (teams.length === 0) return [];

        const currentIndex = teams.findIndex(team => team.constructorId === selectedTeam);
        const totalTeams = teams.length;
        const offset = 2;
        const displayedTeams = [];

        for (let i = -offset; i <= offset; i++) {
            const index = (currentIndex + i + totalTeams) % totalTeams;
            displayedTeams.push(teams[index]);
        }

        return displayedTeams;
    };

    return (
        <>
        <Header/>
        <div>
            <div className="ts-team-carousel">
                <button className="ts-carousel-button" onClick={handlePrevious}>&lt;</button>
                <div className="ts-carousel-items">
                    {getDisplayedTeams().map(team => (
                        <div
                            key={team.constructorId}
                            className={`ts-carousel-item ${team.constructorId === selectedTeam ? 'selected' : ''}`}
                            style={team.constructorId === selectedTeam ? { backgroundColor: team.team_color } : {}}
                            onClick={() => setSelectedTeam(team.constructorId)}
                        >
                            <img src={`/team_logos/${team.team_logo}`} alt={`${team.team_logo}`} className="ts-carousel-team-logo" />
                        </div>
                    ))}
                </div>
                <button className="ts-carousel-button" onClick={handleNext}>&gt;</button>
            </div>

            {teamStats && (
                <div className="ts-team-card" style={{ backgroundColor: teamStats.team_color }}>
                    <div className='ts-team-card-bios-container'>
                            <div className='ts-team-name-wrapper'>
                                <div className='ts-team-name'>{teamStats.name}</div>
                            </div>
                            <div className='ts-team-nat-flag-wrapper'>
                                <img className='ts-team-nat-flag' src={`/flags/${teamStats.team_nat_flag}`} alt={`${teamStats.team_nat_flag}`}></img>
                            </div>
                        </div>
                    <div className='ts-team-card-info-container'>
                        <div className='ts-team-stats-container'>
                                <div className='ts-teams-points-wrapper'>
                                    <div className='ts-teams-points' style={{ color: teamStats.team_color }}>{teamStats.points} pts.</div>
                                </div>
                                <div className='ts-team-stats-header' style={{ color: teamStats.team_color }}>Poles:
                                    <div className='ts-team-stats'>
                                        <div className='ts-team-stat-primary'>{teamStats.poles}</div>
                                        <div className='ts-team-stat-secondary'>+{teamStats.sprint_poles}*</div>
                                    </div>
                                </div>
                                <div className='ts-team-stats-header' style={{ color: teamStats.team_color }}>Wins:
                                    <div className='ts-team-stats'>
                                        <div className='ts-team-stat-primary'>{teamStats.wins}</div>
                                        <div className='ts-team-stat-secondary'>+{teamStats.sprint_wins}*</div>
                                    </div>
                                </div>
                                <div className='ts-team-stats-header' style={{ color: teamStats.team_color }}>Podiums:
                                    <div className='ts-team-stats'>
                                        <div className='ts-team-stat-primary'>{teamStats.podiums}</div>
                                        <div className='ts-team-stat-secondary'>+{teamStats.sprint_podiums}*</div>
                                    </div>
                                </div>
                        </div>
                        <div className='ts-team-disclaimer'>* Sprint stats</div>
                    </div>
                    <div className='ts-team-card-content-container'>
                        <div className='ts-team-car-img-wrapper'>
                            <img className='ts-team-car-img' src={`/cars/${teamStats.team_car}`} alt={`${teamStats.team_car}`}></img>
                        </div>
                        <div className='ts-team-car-name-wrapper'>
                            <div className='ts-team-car-name'>{teamStats.car_name}</div>
                        </div>
                        <div className='ts-team-logo-wrapper'>
                            <img className='ts-team-logo' src={`/team_logos/${teamStats.team_logo}`} alt={`${teamStats.team_logo}`}></img>
                        </div>
                    </div>
                </div>
            )}

            <div className="ts-drivers-container">
                {driverStats.map(driver => (
                    <div key={driver.driverId} className="ts-driver-card">
                        <div className='ts-driver-card-content-container'>
                            <div className='ts-driver-img-element' style={{ backgroundColor: teamStats.team_color }}></div>
                            <div className='ts-driver-img-wrapper'>
                                <img className='ts-driver-img' src={`/pro_pic/${driver.driver_pic}`} alt={`${driver.driver_pic}`}></img>
                            </div>
                            <div className='ts-driver-team-logo-wrapper'>
                                <img className='ts-driver-team-logo' src={`/team_logos/${teamStats.team_logo}`} alt={`${teamStats.team_logo}`}></img>
                            </div>
                            <div className='ts-driver-points-wrapper'>
                                <div className='ts-driver-points' style={{ color: teamStats.team_color }}>{driver.points} pts.</div>
                            </div>
                            <div className='ts-driver-stats-container'>
                                <div className='ts-driver-stat-row'>
                                    <div className='ts-driver-stat-header' style={{ color: teamStats.team_color }}>Poles:
                                        <div className='ts-driver-stat-primary'>{driver.poles}</div>
                                        <div className='ts-driver-stat-secondary'>+{driver.sprint_poles}*</div>
                                    </div>
                                </div>
                                <div className='ts-driver-stat-row'>
                                    <div className='ts-driver-stat-header' style={{ color: teamStats.team_color }}>Wins:
                                        <div className='ts-driver-stat-primary'>{driver.wins}</div>
                                        <div className='ts-driver-stat-secondary'>+{driver.sprint_wins}*</div>
                                    </div>
                                </div>
                                <div className='ts-driver-stat-row'>
                                    <div className='ts-driver-stat-header' style={{ color: teamStats.team_color }}>Podiums:
                                        <div className='ts-driver-stat-primary'>{driver.podiums}</div>
                                        <div className='ts-driver-stat-secondary'>+{driver.sprint_podiums}*</div>
                                    </div>
                                </div>
                            </div>
                            <div className='ts-driver-disclaimer'>* Sprint stats</div>
                        </div>
                        <div className='ts-driver-card-info-container'>
                            <div className='ts-driver-card-bios-container'>
                                <div className='ts-driver-nat-flag-wrapper'>
                                    <img className='ts-driver-nat-flag' src={`/flags/${driver.nat_flag}`} alt={`${driver.nat_flag}`}></img>
                                </div>
                                <div className='ts-driver-fullName-container'>
                                    <div className='ts-driver-forename'>{driver.forename}</div>
                                    <div className='ts-driver-surname'>{driver.surname}</div>
                                </div>
                                <div className='ts-driver-dob-container'>
                                    <div className='ts-driver-dob'>{driver.dob}</div>
                                    <div className='ts-driver-age'>({driver.age})</div>
                                </div>
                            </div>
                            <div className='ts-driver-bios-element'>
                                <div className='ts-driver-number' style={{ WebkitTextStrokeColor: teamStats.team_color}}>{driver.number}</div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
        <Footer/>
        </>
    );
};

export default TeamSection;
