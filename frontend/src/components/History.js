import React, { useEffect, useState } from 'react';
import '../styles/History.css';
import historyLogo from './history_logo.png';
import winsLogo from './most_wins.jpg';

const History = () => {
  const [history, setHistory] = useState([]);
  const [showTable1, setShowTable1] = useState(false);
  const [showTable2, setShowTable2] = useState(false);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/history');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const result = await response.json();
        setHistory(result);
      } catch (error) {
        console.error('Errore nel recupero della storia:', error);
      }
    };

    fetchHistory();
  }, []);

  const toggleTable1 = () => {
    setShowTable1(!showTable1);
  };

  const toggleTable2 = () => {
    setShowTable2(!showTable2);
  };

  return (
    <div className="history-container">
      <h1>All-Time Stats</h1>
      
      {/* Primo contenitore */}
      <div className="chart-container">
        <img src={winsLogo} alt="History Logo" className="history-logo" onClick={toggleTable1} />
        {showTable1 && (
          <div className="table-container">
            <h3>Grand Prix Wins Details</h3>
            <table>
              <thead>
                <tr>
                  <th>Posizione</th>
                  <th>Nome</th>
                  <th>Cognome</th>
                  <th>Vittorie</th>
                  <th>Prima Vittoria</th>
                  <th>Ultima Vittoria</th>
                </tr>
              </thead>
              <tbody>
                {history && history.map((driver, index) => (
                  <tr key={index}>
                    <td>{index + 1}</td>
                    <td>{driver.forename}</td>
                    <td>{driver.surname}</td>
                    <td>{driver.gpWins}</td>
                    <td>{driver.firstWin}</td>
                    <td>{driver.lastWin}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Secondo contenitore */}
      <div className="chart-container">
        <img src={historyLogo} alt="History Logo" className="history-logo" onClick={toggleTable2} />
        {showTable2 && (
          <div className="table-container">
            <h3>Grand Prix Wins Details</h3>
            <table>
              <thead>
                <tr>
                  <th>Posizione</th>
                  <th>Nome</th>
                  <th>Cognome</th>
                  <th>Vittorie</th>
                  <th>Prima Vittoria</th>
                  <th>Ultima Vittoria</th>
                </tr>
              </thead>
              <tbody>
                {history && history.map((driver, index) => (
                  <tr key={index}>
                    <td>{index + 1}</td>
                    <td>{driver.forename}</td>
                    <td>{driver.surname}</td>
                    <td>{driver.gpWins}</td>
                    <td>{driver.firstWin}</td>
                    <td>{driver.lastWin}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default History;
