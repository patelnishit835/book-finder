import React, { useState } from 'react';
import { Link } from 'react-router-dom';

function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [category, setCategory] = useState('');
  const [author, setAuthor] = useState('');
  const [year, setYear] = useState('');

  const handleSearch = async () => {
    let url = '';
    if (query) {
      url = `/search?q=${encodeURIComponent(query)}`;
    } else {
      const params = new URLSearchParams();
      if (category) params.append('category', category);
      if (author) params.append('author', author);
      if (year) params.append('year', year);
      url = `/filter?${params.toString()}`;
    }

    const response = await fetch(url);
    const data = await response.json();
    setResults(data);
  };

  return (
    <>
      <header className="app-header">
        <h1>📚 Book Explorer</h1>
      </header>
      
      <div className="search-page">
        <div className="search-inputs">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search for books..."
          />
          <button onClick={handleSearch}>Search</button>
        </div>

        <div className="filter-section">
          <h2>Advanced Filters</h2>
          <div className="filter-inputs">
            <input
              type="text"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              placeholder="Category (e.g., Fiction)"
            />
            <input
              type="text"
              value={author}
              onChange={(e) => setAuthor(e.target.value)}
              placeholder="Author name"
            />
            <input
              type="number"
              value={year}
              onChange={(e) => setYear(e.target.value)}
              placeholder="Publication year"
            />
          </div>
        </div>

        <div className="results-section">
          <h2>Search Results</h2>
          <ul className="results-list">
            {results.map((book) => (
              <li key={book.id} className="book-card">
                <Link to={`/book/${book.isbn13 || book.isbn10}`}>
                  <h3>{book.title}</h3>
                  <p>by {book.authors}</p>
                  {book.categories && <p className="categories">{book.categories}</p>}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </>
  );
}

export default SearchPage;