import React, { useEffect, useState } from 'react';
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

    return (
        <div>
            <h1>Team Section</h1>
            <div className="team-buttons">
                {teams.map(team => (
                    <button
                        key={team.constructorId}
                        className={team.constructorId === selectedTeam ? 'team-button selected' : 'team-button'}
                        onClick={() => setSelectedTeam(team.constructorId)}
                    >
                        {team.name}
                    </button>
                ))}
            </div>

            {teamStats && (
                <div className="team-card">
                    <h2>{teamStats.name}</h2>
                    <p>Points: {teamStats.points}</p>
                    <p>Wins: {teamStats.wins}</p>
                    <p>Podiums: {teamStats.podiums}</p>
                    <p>Sprint Wins: {teamStats.sprint_wins}</p>
                    <p>Sprint Podiums: {teamStats.sprint_podiums}</p>
                </div>
            )}

            <div className="drivers-container">
                {driverStats.map(driver => (
                    <div key={driver.driverId} className="driver-card">
                        <h3>{driver.forename} {driver.surname}</h3>
                        <p>Nationality: {driver.nationality}</p>
                        <p>Points: {driver.points}</p>
                        <p>Wins: {driver.wins}</p>
                        <p>Podiums: {driver.podiums}</p>
                        <p>Sprint Wins: {driver.sprint_wins}</p>
                        <p>Sprint Podiums: {driver.sprint_podiums}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default TeamSection;
