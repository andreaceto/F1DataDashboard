import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import RaceStats from './components/RaceStats';
import TeamSection from './components/TeamSection';
import Calendar from './components/Calendar';
import History from './components/History';

function App() {
    return (
        <Router>
            <div className="App">
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/racestats" element={<RaceStats />} />
                    <Route path="/teams" element={<TeamSection />} />
                    <Route path="/calendar" element={<Calendar />} />
                    <Route path="/history" element={<History />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;

