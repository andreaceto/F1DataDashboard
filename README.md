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
