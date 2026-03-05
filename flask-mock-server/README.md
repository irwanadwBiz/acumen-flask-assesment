# Flask Mock Server

This is a Flask mock API server that provides paginated customer data loaded from a JSON file.

## Features

- MVC Architecture
- Swagger UI Documentation
- Makefile for easy running
- Dockerized

## Requirements

- Python 3.12+ (or Docker)

## Setup Locally

1. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Generate the mock data:

   ```bash
   make data
   ```

3. Start the server:
   ```bash
   make start
   ```

The application runs on `http://localhost:5000`.

## API Documentation (Swagger)

You can view and test the API endpoints using **Swagger UI**.
After starting the server, open your browser and go to:
[http://localhost:5000/apidocs/](http://localhost:5000/apidocs/)

## Running With Docker

If you have Docker running (the Docker daemon must be active):

```bash
docker build -t flask-mock-server .
docker run -p 5000:5000 flask-mock-server
```

Then visit `http://localhost:5000/apidocs/`.
