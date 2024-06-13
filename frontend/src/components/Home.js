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
                <h2>F1 Drivers' World Championship</h2>
                <img src={data.driver_championship_plot_path} alt="F1 Drivers' World Championship" width="800" height="600"/>
            </div>
        </div>
    );
};

export default Home;
