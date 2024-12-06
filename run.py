from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from config import Config
import os
from utils.es_utils import wait_for_elasticsearch
from elasticsearch import Elasticsearch, NotFoundError
import logging

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure the 'werkzeug' logger to display HTTP requests
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.INFO)

try:
    # Configure Elasticsearch with connection verification
    app.elasticsearch = wait_for_elasticsearch()
except ConnectionError as e:
    logging.error(f"Failed to connect to Elasticsearch: {e}")
    exit(1)

# Index name
INDEX_NAME = "books"

@app.route('/search', methods=['GET'])
def search_books():
    query = request.args.get('q', '')
    logging.info(f"Search request received with query: '{query}'")
    if not query:
        logging.warning("Query parameter 'q' is missing.")
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    # Multi-match query across key fields
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title", "subtitle", "authors", "categories", "description"],
                "fuzziness": "AUTO"
            }
        }
    }
    results = app.elasticsearch.search(index=INDEX_NAME, body=body)

    # Extract relevant data
    books = [{"id": hit["_id"], **hit["_source"]} for hit in results['hits']['hits']]
    return jsonify(books)



@app.route('/filter', methods=['GET'])
def filter_books():
    category = request.args.get('category')
    author = request.args.get('author')
    year = request.args.get('year')
    logging.info(f"Filter request received with parameters: category={category}, author={author}, year={year}")

    # Build filter queries
    filters = []
    if category:
        filters.append({"term": {"categories.keyword": category}})
    if author:
        filters.append({"match": {"authors": author}})
    if year:
        filters.append({"term": {"published_year": int(year)}})

    body = {
        "query": {
            "bool": {
                "must": filters
            }
        }
    }
    results = app.elasticsearch.search(index=INDEX_NAME, body=body)

    # Extract relevant data
    books = [{"id": hit["_id"], **hit["_source"]} for hit in results['hits']['hits']]
    return jsonify(books)


@app.route('/book/<isbn>', methods=['GET'])
def get_book_by_isbn(isbn):
    logging.info(f"Get book request received for ISBN: {isbn}")
    body = {
        "query": {
            "bool": {
                "should": [
                    {"term": {"isbn13.keyword": isbn}},
                    {"term": {"isbn10.keyword": isbn}}
                ]
            }
        }
    }
    results = app.elasticsearch.search(index=INDEX_NAME, body=body)

    # Handle no results
    if not results['hits']['hits']:
        logging.warning(f"Book not found for ISBN: {isbn}")
        return jsonify({"error": "Book not found"}), 404

    # Return the first match
    book = results['hits']['hits'][0]["_source"]
    return jsonify(book)


@app.route('/top-rated', methods=['GET'])
def top_rated_books():
    size = int(request.args.get('size', 10))  
    body = {
        "query": {"match_all": {}},
        "sort": [{"average_rating": "desc"}],
        "size": size
    }
    results = app.elasticsearch.search(index=INDEX_NAME, body=body)

    books = [{"id": hit["_id"], **hit["_source"]} for hit in results['hits']['hits']]
    return jsonify(books)


@app.route('/books-by-year', methods=['GET'])
def books_by_year():
    start_year = request.args.get('start_year')
    end_year = request.args.get('end_year')

    if not start_year or not end_year:
        return jsonify({"error": "Both 'start_year' and 'end_year' are required"}), 400

    body = {
        "query": {
            "range": {
                "published_year": {
                    "gte": int(start_year),
                    "lte": int(end_year)
                }
            }
        }
    }
    results = app.elasticsearch.search(index=INDEX_NAME, body=body)

    books = [{"id": hit["_id"], **hit["_source"]} for hit in results['hits']['hits']]
    return jsonify(books)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    logging.info("Starting Flask application...")
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5001)