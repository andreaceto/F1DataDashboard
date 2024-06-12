# F1DataDashboard

## Description
F1DataDashboard is a web application designed for Formula 1 enthusiasts to explore, analyze, and visualize detailed information about the current racing season. The platform provides race-by-race data on driver performances, race statistics, championship standings, and much more. The goal is to deliver a clear and comprehensive overview of every aspect of the races and performances.

## Main Features
- **Homepage**: Displays general standings for drivers and constructors, accompanied by charts showing their performance trends over time.
- **Race-by-Race Statistics**: Allows users to select a specific race to view detailed statistics, such as lap times, final positions, pit stop strategies, and other relevant data for an in-depth analysis of each event.
- **Team Section**: Each team has its own dedicated page, including driver cards, team and car information, historical details, and a palmarès of the team's best achievements.
- **Calendar**: Shows all the race dates for the current season, including practice and qualifying sessions, with detailed information about times, locations, and circuit specifications.
- **F1 History**: Dedicated to the history of Formula 1, with rankings and charts on the most successful drivers and teams of all time, as well as useful statistics covering various historical aspects of the championship.

## Technologies Used
- **Non-relational Database**: MongoDB
- **Back-end**: Flask (Python)
- **Interface with MongoDB**: PyMongo
- **Front-end**: React.js, HTML, CSS, JavaScript

## Project Structure
The project is divided into two main components: backend and frontend. The directory structure is organized as follows:

    F1DataDashboard/
    │
    ├── backend/ # All backend logic and data management
    │ ├── app.py # Entry point for the Flask application
    │ ├── config.py # Server and database configurations
    │ ├── api/
    │ │ ├── init.py # API module initialization
    │ │ └── utils.py # Utility functions for APIs
    │ ├── routes/ # Directory for route definitions
    │ │ ├── init.py # Initializes and registers all routes
    │ │ ├── home_route.py # Route for the homepage and general information
    │ │ ├── raceStats_route.py # Route for race statistics
    │ │ ├── teamSection_route.py # Route for team information
    │ │ ├── calendar_route.py # Route for the race calendar
    │ │ └── history_route.py # Route for historical data
    │ ├── data/
    │ │ ├── init.py # Database connection and operations management
    │ │ ├── model.py # MongoDB data models
    │ │ └── data_handler.py # Script for data handling (import/export)
    │ └── services/
    │ ├── init.py # Service module initialization
    │ ├── query_service.py # Services for specific queries
    │ └── calc_service.py # Services for calculations and aggregations
    │
    ├── frontend/ # Source code for the frontend
    │ ├── public/ # Static files such as index.html and manifest.json
    │ ├── src/
    │ │ ├── components/ # React components
    │ │ │ ├── Home.js
    │ │ │ ├── RaceStats.js
    │ │ │ ├── TeamSection.js
    │ │ │ ├── Calendar.js
    │ │ │ └── History.js
    │ │ ├── App.js # Main component of the app
    │ │ ├── index.js # JS entry point
    │ │ └── styles/ # Directory for CSS and other styles
    │ │ ├── App.css
    │ │ └── index.css
    │ └── package.json # NPM dependencies and scripts
    │
    ├── scripts/ # Useful scripts such as deployment scripts
    │ └── deploy.sh
    │
    ├── .gitignore # Files and directories to ignore in Git
    ├── README.md # Project guide and documentation
    └── requirements.txt # Necessary Python dependencies


## Installation Instructions
Follow these steps to set up the project locally.

### Backend Setup
1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd F1DataDashboard/backend

2. **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt

4. **Start the Flask application:**
    ```bash
    python app.py

### Frontend Setup
1. **Navigate to the frontend directory:**
   ```bash
   cd F1DataDashboard/frontend

2. **Install the required NPM packages:**
    ```bash
    npm install

3. **Start the React application:**
    ```bash
    npm start


## Usage
Access the application via a web browser at http://localhost:3000 (default port for React development server) or http://localhost:5000 if accessing backend directly.