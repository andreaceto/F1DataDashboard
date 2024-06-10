import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Home = () => {
    const [plot, setPlot] = useState(null);

    useEffect(() => {
        axios.get('/api/home')  // Ensure this matches your Flask route
            .then(response => {
                setPlot(response.data.plot);
            })
            .catch(error => {
                console.error('Error fetching the plot data', error);
            });
    }, []);

    return (
        <div>
            <h1>F1 Data Dashboard</h1>
            {plot ? <img src={`data:image/png;base64,${plot}`} alt="Driver Points Over Time" /> : 'Loading...'}
        </div>
    );
};

export default Home;
