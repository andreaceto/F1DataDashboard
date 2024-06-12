import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Home = () => {
    const [data, setData] = useState(null);

    useEffect(() => {
        axios.get('/')  // Ensure this matches your Flask route
            .then(response => {
                setData(response.data);
            })
            .catch(error => {
                console.error('Error fetching the home data', error);
            });
    }, []);

    if (!data) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1>F1 Data Dashboard</h1>
            <div>
                <h2>F1 Drivers' World Championship</h2>
                <img src={`data:image/png;base64,${data['driver_championship_plot']}`} alt="F1 Drivers' World Championship" />
            </div>
        </div>
    );
};

export default Home;
