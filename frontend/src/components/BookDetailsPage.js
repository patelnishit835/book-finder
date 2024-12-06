import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';

function BookDetailsPage() {
  const { isbn } = useParams();
  const [book, setBook] = useState(null);

  useEffect(() => {
    const fetchBookDetails = async () => {
      const response = await fetch(`/book/${isbn}`);
      const data = await response.json();
      setBook(data);
    };
    fetchBookDetails();
  }, [isbn]);

  if (!book) return (
    <div className="loading">
      <div className="loader"></div>
      <p>Loading book details...</p>
    </div>
  );

  return (
    <>
      <header className="app-header">
        <h1>📚 Book Details</h1>
      </header>
      
      <div className="book-details">
        <Link to="/" className="back-button">← Back to Search</Link>
        <h1>{book.title}</h1>
        {book.subtitle && <h2>{book.subtitle}</h2>}
        
        <div className="book-info">
          <div className="info-item">
            <strong>Author(s):</strong>
            <p>{book.authors}</p>
          </div>
          <div className="info-item">
            <strong>Categories:</strong>
            <p>{book.categories}</p>
          </div>
          <div className="info-item">
            <strong>Published:</strong>
            <p>{book.published_year}</p>
          </div>
          {book.average_rating && (
            <div className="info-item">
              <strong>Rating:</strong>
              <p>⭐ {book.average_rating}/5</p>
            </div>
          )}
        </div>

        <div className="book-description">
          <h3>Description</h3>
          <p>{book.description}</p>
        </div>
      </div>
    </>
  );
}

export default BookDetailsPage;