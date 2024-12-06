import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SearchPage from './components/SearchPage';
import BookDetailsPage from './components/BookDetailsPage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<SearchPage />} />
          <Route path="/book/:isbn" element={<BookDetailsPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;