import React, { useEffect, useState } from 'react';

const Home = () => {
    const [data, setData] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('http://127.0.0.1:5000//');
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

    if (!data) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1>F1 Data Dashboard</h1>
            <div>
                <h2>Drivers' Standings</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Position</th>
                            <th>Driver</th>
                            <th>Nationality</th>
                            <th>Team</th>
                            <th>Points</th>
                            <th>Wins</th>
                            <th>Sprint Wins</th>
                            <th>Podiums</th>
                            <th>Sprint Podiums</th>
                        </tr>
                    </thead>
                    <tbody>
                        {data.drivers_standings_table.map((driver, index) => (
                            <tr key={index}>
                                <td>{driver.Position}</td>
                                <td>{driver.Driver}</td>
                                <td>{driver.Nationality}</td>
                                <td>{driver.Team}</td>
                                <td>{driver.Points}</td>
                                <td>{driver.Wins}</td>
                                <td>{driver.SprintWins}</td>
                                <td>{driver.Podiums}</td>
                                <td>{driver.SprintPodiums}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            <div>
                <h2>F1 Drivers' World Championship</h2>
                <img src={data.driver_championship_plot_path} alt="F1 Drivers' World Championship" />
            </div>
        </div>
    );
};

export default Home;
