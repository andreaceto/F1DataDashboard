import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
    const [data, setData] = useState(null);

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
            <div>
                <h2>Constructors' Standings</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Position</th>
                            <th>Constructor</th>
                            <th>Points</th>
                            <th>Wins</th>
                            <th>Podiums</th>
                            <th>Sprint Wins</th>
                            <th>Sprint Podiums</th>
                            <th>Drivers</th>
                        </tr>
                    </thead>
                    <tbody>
                        {data.constructors_standings_table.map((constructor, index) => (
                            <tr key={index}>
                                <td>{constructor.Position}</td>
                                <td>{constructor.Constructor}</td>
                                <td>{constructor.Points}</td>
                                <td>{constructor.Wins}</td>
                                <td>{constructor.Podiums}</td>
                                <td>{constructor.SprintWins}</td>
                                <td>{constructor.SprintPodiums}</td>
                                <td>{constructor.Drivers.join(', ')}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            <div>
                <h2>F1 Constructors' World Championship</h2>
                <img src={data.constructor_championship_plot_path} alt="F1 Constructors' World Championship" />
            </div>
            <div>
                <Link to="/teams">
                    <button>Teams</button>
                </Link>
                <Link to="/calendar">
                    <button>Calendar</button>
                </Link>
                <Link to="/history">
                    <button>History</button>
                </Link>
            </div>
        </div>
    );
};

export default Home;
