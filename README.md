# 📚 Book Finder

Welcome to **Book Finder**, a comprehensive application to search and filter books using Elasticsearch and a React frontend. Follow the steps below to set up and run the project.

## Prerequisites

Ensure you have the following installed:
- Python 3.9+
- Node.js 14+
- Elasticsearch 7.x

## Setup Instructions

### 1. Populate the Database

First, you need to populate the Elasticsearch database with book data.

1. Navigate to the project directory:
    ```sh
    cd /path/to/project
    ```

2. Run the `populate_data.py` script:
    ```sh
    python populate_data.py
    ```

### 2. Run the Backend Application

Next, start the Flask backend application.

1. Navigate to the project directory (if not already there):
    ```sh
    cd /path/to/project
    ```

2. Run the `run.py` script:
    ```sh
    python run.py
    ```

The backend server should now be running on `http://localhost:5001`.

### 3. Run the React Application

Finally, start the React frontend application.

1. Navigate to the `frontend` directory:
    ```sh
    cd frontend
    ```

2. Install the dependencies:
    ```sh
    npm install
    ```

3. Start the React application:
    ```sh
    npm start
    ```

The frontend application should now be running on `http://localhost:3000`.

## Usage

- **Search Books**: Use the search bar to find books by title, author, or category.
- **Filter Books**: Use the advanced filters to narrow down your search by category, author, or publication year.
- **Book Details**: Click on a book to view detailed information.

## License

This project is licensed under the MIT License.

---

Happy Reading! 📖