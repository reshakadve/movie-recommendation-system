import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function MovieRecommendation() {
  const [movieName, setMovieName] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [movieNotFound, setMovieNotFound] = useState(false);  

  const handleInputChange = (e) => {
    setMovieName(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!movieName) return;

    setLoading(true);
    setError('');
    setMovieNotFound(false);  
    try {
      const response = await axios.get(`http://localhost:5000/recommend?movie_name=${movieName}`);
      if (response.data.error) {
        setMovieNotFound(true); 
        setRecommendations([]);
      } else {
        setRecommendations(response.data);
      }
    } catch (err) {
      setError('Error fetching recommendations');
    }

    setLoading(false);
  };

  return (
    <div className="movie-recommendation-container">
      <h1>Movie Recommendation System</h1>
      <form className="movie-form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter movie name"
          value={movieName}
          onChange={handleInputChange}
          className="movie-input"
        />
        <button type="submit" className="submit-button">Get Recommendations</button>
      </form>

      {loading && <p className="loading-text">Loading...</p>}
      {error && <p className="error-text">{error}</p>}
      {movieNotFound && <p className="error-text">Movie not found in the database.</p>} {/* Show message if movie not found */}

      <div className="recommendations-list">
        <h3>Recommended Movies:</h3>
        <ul>
          {recommendations.length > 0 ? (
            recommendations.map((movie, index) => (
              <li key={index}>
                <span className="movie-title">{movie}</span>
              </li>
            ))
          ) : (
            // No message unless movie not found
            <></>
          )}
        </ul>
      </div>
    </div>
  );
}

export default MovieRecommendation;
