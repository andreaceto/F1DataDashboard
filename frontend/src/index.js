import React from 'react';
import { createRoot } from 'react-dom/client';
import './styles/index.css';
import App from './App';
import reportWebVitals from './reportWebVitals'; // Ensure you have this file or remove this line if not needed

const container = document.getElementById('root');
const root = createRoot(container);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Call reportWebVitals if you need it
reportWebVitals(console.log); // You can customize this line if needed

