import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [description, setDescription] = useState('');
  const [suggestions, setSuggestions] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://localhost:5000/predict', { description });
      setSuggestions(response.data);
    } catch (error) {
      console.error("Error fetching suggestions:", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>DesignSense AI</h1>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Enter design description"
          />
          <p></p>
          <button type="submit">Get Suggestions</button>
        </form>
        <p></p>
        {suggestions && (
          <div className="suggestions">
            <h2>Suggestions</h2>
            <p><strong>Font:</strong> {suggestions.font}</p>
            <p><strong>Color Palette:</strong> {suggestions.palette}</p>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;

