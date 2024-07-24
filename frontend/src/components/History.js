import React, { useEffect, useState } from 'react';
import '../styles/History.css';
import Header from './Header.js';
import Footer from './Footer.js';

const History = () => {
  const [driverHistory, setDriverHistory] = useState([]);
  const [activeTable, setActiveTable] = useState(null);
  const [carouselPosition, setCarouselPosition] = useState(0);
  const [additionalCarouselPosition, setAdditionalCarouselPosition] = useState(0);
  const [thirdCarouselPosition, setThirdCarouselPosition] = useState(0);
  const [activeAdditionalTable, setActiveAdditionalTable] = useState(null);
  const [activeThirdTable, setActiveThirdTable] = useState(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/history');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const result = await response.json();
        setDriverHistory(result);
      } catch (error) {
        console.error('Errore nel recupero della storia:', error);
      }
    };

    fetchHistory();
    document.body.style.backgroundColor = 'black';

    return () => {
      document.body.style.backgroundColor = '';
    };
  }, []);

  const carouselImages = [
    { id: 1, src: `${process.env.PUBLIC_URL}/all_time/most_gp.jpg`, alt: 'World Logo', title: 'Most World Drivers’ Championships' },
    { id: 2, src: `${process.env.PUBLIC_URL}/all_time/most_wins.jpg`, alt: 'Wins Logo', title: 'Most Grand Prix Wins' },
    { id: 3, src: `${process.env.PUBLIC_URL}/all_time/most_podiums.jpg`, alt: 'Podiums Logo', title: 'Most Podiums' },
    { id: 4, src: `${process.env.PUBLIC_URL}/all_time/most_points.jpg`, alt: 'Points Logo', title: 'Most Points' },
    { id: 5, src: `${process.env.PUBLIC_URL}/all_time/most_polePositions.jpg`, alt: 'Pole Logo', title: 'Most Pole Positions' },
  ];

  const additionalCarouselImages = [
    { id: 6, src: `${process.env.PUBLIC_URL}/all_time/most_gp_cons.jpg`, alt: 'C World Logo', title: 'Most World Constructors’ Championships' },
    { id: 7, src: `${process.env.PUBLIC_URL}/all_time/most_wins_cons.jpg`, alt: 'C Wins Logo', title: 'Most Grand Prix Wins'},
    { id: 8, src: `${process.env.PUBLIC_URL}/all_time/most_podiums_cons.jpg`, alt: 'C Podiums Logo', title: 'Most Podiums' },
    { id: 9, src: `${process.env.PUBLIC_URL}/all_time/most_starts_cons.png`, alt: 'C Starts Logo', title: 'Most Starts' },
    { id: 10, src: `${process.env.PUBLIC_URL}/all_time/most_fastest_laps_cons.jpg`, alt: 'C Laps Logo', title: 'Most Fastest Laps' },
  ];

  const thirdCarouselImages = [
    { id: 11, src: `${process.env.PUBLIC_URL}/all_time/most_raced_circuits.jpg`, alt: 'Teams Logo', title: 'Most Raced Circuits' },
    { id: 12, src: `${process.env.PUBLIC_URL}/all_time/most_nations_wins.png`, alt: 'Drivers Logo', title: 'Nations With Most GP Wins' },
    { id: 13, src: `${process.env.PUBLIC_URL}/all_time/most_nations_drivers.jpg`, alt: 'Countries Logo', title: 'Nations With Most Drivers' },
  ];

  const handleImageClick = (tableId, isAdditional, isThird) => {
    if (isThird) {
      setActiveThirdTable((prevActiveTable) => (prevActiveTable === tableId ? null : tableId));
    } else if (isAdditional) {
      setActiveAdditionalTable((prevActiveTable) => (prevActiveTable === tableId ? null : tableId));
    } else {
      setActiveTable((prevActiveTable) => (prevActiveTable === tableId ? null : tableId));
    }
  };

  const handlePrevClick = () => {
    setCarouselPosition((prevPosition) => (prevPosition - 1 + carouselImages.length) % carouselImages.length);
  };

  const handleNextClick = () => {
    setCarouselPosition((prevPosition) => (prevPosition + 1) % carouselImages.length);
  };

  const handleAdditionalPrevClick = () => {
    setAdditionalCarouselPosition((prevPosition) => (prevPosition - 1 + additionalCarouselImages.length) % additionalCarouselImages.length);
  };

  const handleAdditionalNextClick = () => {
    setAdditionalCarouselPosition((prevPosition) => (prevPosition + 1) % additionalCarouselImages.length);
  };

  const handleThirdPrevClick = () => {
    setThirdCarouselPosition((prevPosition) => (prevPosition - 1 + thirdCarouselImages.length) % thirdCarouselImages.length);
  };

  const handleThirdNextClick = () => {
    setThirdCarouselPosition((prevPosition) => (prevPosition + 1) % thirdCarouselImages.length);
  };

  return (
    <>
      <Header /> {}
      <div className="hist-main-content"> {}
        <div className="hist-header-image-container">
          <img src={`${process.env.PUBLIC_URL}/all_time/alltimeLogo.png`} alt="All-Time Stats" className="hist-header-image" />
        </div>

        <div className="hist-grid-section">
        <h2 className="hist-grid-title">DRIVER STATS</h2>
          <div className="hist-grid-container">
            <div className="hist-navigation-buttons left">
              <button onClick={handlePrevClick}>{'<'}</button>
            </div>
            {Array.from({ length: 3 }).map((_, index) => {
              const imgIndex = (carouselPosition + index) % carouselImages.length;
              const image = carouselImages[imgIndex];
              return (
                <div className="hist-image-container" key={image.id} onClick={() => handleImageClick(image.id, false, false)}>
                  <img src={image.src} alt={image.alt} className="hist-history-logo" />
                  <p className="hist-image-title">{image.title}</p>
                </div>
              );
            })}
            <div className="hist-navigation-buttons right">
              <button onClick={handleNextClick}>{'>'}</button>
            </div>
          </div>
        </div>

        <div className="hist-table-container">
          {activeTable === 1 && <MostWorldChampionshipsTable driverHistory={driverHistory} />}
          {activeTable === 2 && <MostWinsTable driverHistory={driverHistory} />}
          {activeTable === 3 && <MostPodiumsTable driverHistory={driverHistory} />}
          {activeTable === 4 && <MostPointsTable driverHistory={driverHistory} />}
          {activeTable === 5 && <MostPolePositionsTable driverHistory={driverHistory} />}
        </div>

        <div className="hist-grid-section">
          <h2 className="hist-grid-title">CONSTRUCTORS STATS</h2>
          <div className="hist-grid-container">
            <div className="hist-navigation-buttons left">
              <button onClick={handleAdditionalPrevClick}>{'<'}</button>
            </div>
            {Array.from({ length: 3 }).map((_, index) => {
              const imgIndex = (additionalCarouselPosition + index) % additionalCarouselImages.length;
              const image = additionalCarouselImages[imgIndex];
              return (
                <div className="hist-image-container" key={image.id} onClick={() => handleImageClick(image.id, true, false)}>
                  <img src={image.src} alt={image.alt} className="hist-history-logo" />
                  <p className="hist-image-title">{image.title}</p>
                </div>
              );
            })}
            <div className="hist-navigation-buttons right">
              <button onClick={handleAdditionalNextClick}>{'>'}</button>
            </div>
          </div>
        </div>

        <div className="hist-table-container">
          {activeAdditionalTable === 6 && <MostConstructorsChampionshipsTable driverHistory={driverHistory} />}
          {activeAdditionalTable === 7 && <MostConstructorsWinsTable driverHistory={driverHistory} />}
          {activeAdditionalTable === 8 && <MostConstructorsPodiumsTable driverHistory={driverHistory} />}
          {activeAdditionalTable === 9 && <MostConstructorsStartsTable driverHistory={driverHistory} />}
          {activeAdditionalTable === 10 && <MostConstructorsFastestLapsTable driverHistory={driverHistory} />}
        </div>

        <div className="hist-grid-section">
          <h2 className="hist-grid-title">OTHER STATS</h2>
          <div className="hist-grid-container">
            <div className="hist-navigation-buttons left">
              <button onClick={handleThirdPrevClick}>{'<'}</button>
            </div>
            {Array.from({ length: 3 }).map((_, index) => {
              const imgIndex = (thirdCarouselPosition + index) % thirdCarouselImages.length;
              const image = thirdCarouselImages[imgIndex];
              return (
                <div className="hist-image-container" key={image.id} onClick={() => handleImageClick(image.id, false, true)}>
                  <img src={image.src} alt={image.alt} className="hist-history-logo" />
                  <p className="hist-image-title">{image.title}</p>
                </div>
              );
            })}
            <div className="hist-navigation-buttons right">
              <button onClick={handleThirdNextClick}>{'>'}</button>
            </div>
          </div>
        </div>

        <div className="hist-table-container">
          {activeThirdTable === 11 && <MostCircuitsGPTable driverHistory={driverHistory} />}
          {activeThirdTable === 12 && <MostNationsWinsTable driverHistory={driverHistory} />}
          {activeThirdTable === 13 && <MostNationsDriversTable driverHistory={driverHistory} />}
        </div>
      </div>
      <Footer /> {}
    </>
    
  );
};
/*

  DRIVER STATS

*/
const MostWorldChampionshipsTable = ({ driverHistory }) => {
  return (
    <table className="hist-specific-page-table world-championships-table">
      <thead>
        <tr>
          <th>Position</th>
          <th>First Name</th>
          <th>Last Name</th>
          <th>Championships</th>
        </tr>
      </thead>
      <tbody>
        {driverHistory.mostChampionships?.map((driver, index) => (
          <tr key={index}>
            <td>{index + 1}</td>
            <td>{driver.forename}</td>
            <td>{driver.surname}</td>
            <td>{driver.championshipsWon}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

const MostWinsTable = ({ driverHistory }) => {
  return (
    <table className="hist-specific-page-table wins-table">
      <thead>
        <tr>
          <th>Position</th>
          <th>First Name</th>
          <th>Last Name</th>
          <th>Wins</th>
          <th>First Win</th>
          <th>Last Win</th>
        </tr>
      </thead>
      <tbody>
        {driverHistory.mostWins?.map((driver, index) => (
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
  );
};

const MostPodiumsTable = ({ driverHistory }) => {
  return (
    <table className="hist-specific-page-table podiums-table">
      <thead>
        <tr>
          <th>Position</th>
          <th>First Name</th>
          <th>Last Name</th>
          <th>Podiums</th>
          <th>Podium Percentage</th>
          <th>Team</th>
        </tr>
      </thead>
      <tbody>
        {driverHistory.podiums?.map((driver, index) => (
          <tr key={index}>
            <td>{index + 1}</td>
            <td>{driver.forename}</td>
            <td>{driver.surname}</td>
            <td>{driver.podiums}</td>
            <td>{driver.podiumPercentage}</td>
            <td>{driver.constructors}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

const MostPointsTable = ({ driverHistory }) => {
  return (
    <table className="hist-specific-page-table points-table">
      <thead>
        <tr>
          <th>Position</th>
          <th>First Name</th>
          <th>Last Name</th>
          <th>Points</th>
          <th>Points per GP</th>
        </tr>
      </thead>
      <tbody>
        {driverHistory.mostPoints?.map((driver, index) => (
          <tr key={index}>
            <td>{index + 1}</td>
            <td>{driver.forename}</td>
            <td>{driver.surname}</td>
            <td>{driver.totalPoints}</td>
            <td>{driver.pointsPerGP}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

const MostPolePositionsTable = ({ driverHistory }) => {
  return (
    <table className="hist-specific-page-table pole-positions-table">
      <thead>
        <tr>
          <th>Position</th>
          <th>First Name</th>
          <th>Last Name</th>
          <th>Pole Positions</th>
          <th>Pole Percentage</th>
          <th>Team</th>
        </tr>
      </thead>
      <tbody>
        {driverHistory.polePositions?.map((driver, index) => (
          <tr key={index}>
            <td>{index + 1}</td>
            <td>{driver.forename}</td>
            <td>{driver.surname}</td>
            <td>{driver.polePositions}</td>
            <td>{driver.polePercentage}</td>
            <td>{driver.constructors}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

const MostConstructorsChampionshipsTable = ({ driverHistory }) => {
  return (
    <table className="hist-specific-page-table constructors-championships-table">
      <thead>
        <tr>
          <th>Position</th>
          <th>Team</th>
          <th>Championships</th>
        </tr>
      </thead>
      <tbody>
        {driverHistory.mostConstructorChampionships?.map((driver, index) => (
          <tr key={index}>
            <td>{index + 1}</td>
            <td>{driver.name}</td>
            <td>{driver.championshipsWon}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

const MostConstructorsWinsTable = ({ driverHistory }) => {
  return (
    <table className="hist-specific-page-table constructors-wins-table">
      <thead>
        <tr>
          <th>Position</th>
          <th>Team</th>
          <th>Wins</th>
          <th>First Win</th>
          <th>Last Win</th>
        </tr>
      </thead>
      <tbody>
        {driverHistory.mostConstructorsWins?.map((driver, index) => (
          <tr key={index}>
            <td>{index + 1}</td>
            <td>{driver.name}</td>
            <td>{driver.wins}</td>
            <td>{driver.firstWin}</td>
            <td>{driver.lastWin}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

const MostConstructorsPodiumsTable = ({ driverHistory }) => {
  return (
    <table className="hist-specific-page-table constructors-podiums-table">
      <thead>
        <tr>
          <th>Position</th>
          <th>Team</th>
          <th>Podiums</th>
          <th>Podium Percentage</th>
          <th>Top Driver</th>
        </tr>
      </thead>
      <tbody>
        {driverHistory.mostConstructorsPodiums?.map((driver, index) => (
          <tr key={index}>
            <td>{index + 1}</td>
            <td>{driver.name}</td>
            <td>{driver.podiums}</td>
            <td>{driver.percentage_podiums}</td>
            <td>{driver.best_driver}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

const MostConstructorsStartsTable = ({ driverHistory }) => {
  return (
    <table className="hist-specific-page-table constructors-starts-table">
      <thead>
        <tr>
          <th>Position</th>
          <th>Team</th>
          <th>Starts</th>
          <th>Active Seasons</th>
        </tr>
      </thead>
      <tbody>
        {driverHistory.mostConstructorsStarts?.map((driver, index) => (
          <tr key={index}>
            <td>{index + 1}</td>
            <td>{driver.name}</td>
            <td>{driver.num_participations}</td>
            <td>{driver.active_seasons}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

const MostConstructorsFastestLapsTable = ({ driverHistory }) => {
  return (
    <table className="hist-specific-page-table constructors-fastest-laps-table">
      <thead>
        <tr>
          <th>Position</th>
          <th>Team</th>
          <th>Fastest Laps</th>
          <th>First Fastest Lap</th>
          <th>Last Fastest Lap</th>
        </tr>
      </thead>
      <tbody>
        {driverHistory.mostConstructorsFastLaps?.map((driver, index) => (
          <tr key={index}>
            <td>{index + 1}</td>
            <td>{driver.name}</td>
            <td>{driver.fastest_laps}</td>
            <td>{driver.first_race}</td>
            <td>{driver.last_race}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

const MostCircuitsGPTable = ({ driverHistory }) => {
  return (
    <table className="hist-specific-page-table most-circuits-gp-table">
      <thead>
        <tr>
          <th>Position</th>
          <th>Circuit</th>
          <th>Grand Prix</th>
          <th>First GP</th>
          <th>Last GP</th>
        </tr>
      </thead>
      <tbody>
        {driverHistory.mostCircuitsGP?.map((driver, index) => (
          <tr key={index}>
            <td>{index + 1}</td>
            <td>{driver.name}</td>
            <td>{driver.num_gps}</td>
            <td>{driver.first_gp_year}</td>
            <td>{driver.last_gp_year}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

const MostNationsWinsTable = ({ driverHistory }) => {
  return (
    <table className="hist-specific-page-table most-nations-wins-table">
      <thead>
        <tr>
          <th>Position</th>
          <th>Country</th>
          <th>Wins</th>
          <th>Number of Drivers</th>
          <th>Drivers</th>
        </tr>
      </thead>
      <tbody>
        {driverHistory.mostNationsWins?.map((driver, index) => (
          <tr key={index}>
            <td>{index + 1}</td>
            <td>{driver.country}</td>
            <td>{driver.num_wins}</td>
            <td>{driver.num_drivers}</td>
            <td>{driver.drivers}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

const MostNationsDriversTable = ({ driverHistory }) => {
  return (
    <table className="hist-specific-page-table most-nations-drivers-table">
      <thead>
        <tr>
          <th>Position</th>
          <th>Country</th>
          <th>Drivers</th>
          <th>Wins</th>
          <th>Top Driver</th>
        </tr>
      </thead>
      <tbody>
        {driverHistory.mostNationsDrivers?.map((driver, index) => (
          <tr key={index}>
            <td>{index + 1}</td>
            <td>{driver.nationality}</td>
            <td>{driver.num_drivers}</td>
            <td>{driver.total_wins}</td>
            <td>{driver.best_driver}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default History;