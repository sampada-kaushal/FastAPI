# FastAPI Scraping Tool

## Overview
This FastAPI application scrapes product data from a website, caches it in Redis, and saves it in a JSON file. The tool supports authentication, proxy usage, and dynamic page scraping.

---

## Features
- Scrapes product title, price, and image.
- Caches results using Redis to avoid redundant scraping.
- Supports proxy configuration for scraping.
- Includes authentication using a static token.
- Saves product data in a JSON file and downloads product images locally.

---

## Prerequisites
1. **Python**: Version 3.10 or later.
2. **Redis**: Ensure Redis is installed and running locally.

---

## Installation

### 1. Clone the Repository
```bash
git clone <repository_url>
cd FASTAPI
```

### 2. Set Up a Virtual Environment
```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start Redis Server
Ensure Redis is running before using the application:
```bash
redis-server
```

---

## Running the Application

### Start the FastAPI Server
```bash
uvicorn main:app --reload
```

### Access API Documentation
- Open the Swagger UI in your browser: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## API Usage

### Endpoint: `/scrape/`
- **Method**: `GET`
- **Parameters**:
  - `pages` (int): Number of pages to scrape.
  - `proxy` (optional, str): Proxy string for scraping.
  - `token` (str): Authentication token.

### Example cURL Request
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/scrape/?pages=3&token=your_static_token' \
  -H 'accept: application/json'
```

---

## Directory Structure
```
FASTAPI/
├── app/
│   ├── models/
│   │   └── product.py       # Product data model
│   ├── services/
│   │   ├── authentication_service.py  # Authentication logic
│   │   ├── cache_service.py           # Redis caching logic
│   │   ├── data_extraction_service.py # Scraping logic
│   │   ├── file_manager_service.py    # File saving and management
│   │   ├── notification_service.py    # Notification logic
│   │   └── product_service.py         # Product processing logic
│   ├── utils/
│   │   └── hashing.py                 # Utility functions for hashing
├── images/              # Directory for downloaded images
├── venv/                # Virtual environment files
├── products.json        # Scraped product data
├── requirements.txt     # Project dependencies
└── main.py              # Application entry point
```

---

## Output
- **JSON File**: Scraped product data is saved in `products.json`.
- **Images**: Product images are downloaded into the `images/` directory.

---

## Dependencies
Here is a breakdown of the dependencies listed in `requirements.txt`:

- `fastapi`: Web framework for building APIs.
- `requests`: HTTP library for making web requests.
- `beautifulsoup4`: Library for parsing HTML and extracting data.
- `redis`: Python client for Redis.
- `uvicorn`: ASGI server to run the FastAPI application.
- `pydantic` : Library to validate request and response payloads
- `python-dotenv` : Library to manage environment variables or configurations

---

## Notes
- Replace `INITIAL_TOKEN` variable in the code with desired authentication token.
- Ensure the Redis server is running before using the application.
- Modify the base URL in `data_extraction_service.py` if scraping a different website.
- Use `redis-cli` `FLUSHALL` to clear cache