# Full Stack Data Pipeline Assessment

This project implements a data ingestion pipeline using Docker, Flask, FastAPI, PostgreSQL, and DLT.
The system consists of three isolated Docker services mapping to a realistic ETL (Extract, Transform, Load) architectural pattern.

## Architecture

1. **Mock Server (`Flask`) - Port 5000**
   - Serves as the simulated external data source fetching dummy customer records from a local JSON file.
   - Handles data generation, read requests, and mock creation without interacting with the primary database.

2. **Pipeline Service (`FastAPI`) - Port 8000**
   - Serves as the primary ingestor and query API.
   - Uses the `dlt` (Data Load Tool) Python library to extract from the external Mock Server, transform types, and load the data into the Database.

3. **Database (`PostgreSQL`) - Port 5432**
   - Stores the persistent relational data for the Pipeline Service.

---

## 🚀 Getting Started

Ensure you have Docker and Docker Compose installed.

1. **Start the Environment**

```bash
docker-compose up -d --build
```

This will spin up all three services.

2. **Verify Health**
   You can check if the mock server is running natively:

```bash
curl http://localhost:5000/api/health
```

---

## 📖 API Documentation

The architecture utilizes two distinct APIs. The primary interface for users is the **FastAPI Pipeline Service**. The **Flask Mock Server** serves only as an external data simulation layer.

### 🌟 FastAPI Pipeline Service (Port 8000)

FastAPI automatically generates comprehensive Swagger documentation. You can view the fully interactive UI in your browser at:
**[http://localhost:8000/docs](http://localhost:8000/docs)**

#### `POST /api/ingest`

Triggers the ETL pipeline. It paginates through the Flask mock server, pulls all JSON customers, transforms the string dates into native date objects, and conditionally upserts them into Postgres.

```bash
curl -X POST http://localhost:8000/api/ingest
```

**Response**: `{"status":"success","records_processed":25}`

#### `GET /api/customers`

Retrieves paginated customers directly from the PostgreSQL instance using SQLAlchemy.

> **Parameters**:
>
> - `page` (int, default=1): Page number
> - `limit` (int, default=10, max=100): Results per page

```bash
curl "http://localhost:8000/api/customers?page=1&limit=5"
```

#### `GET /api/customers/{customer_id}`

Retrieves a single customer natively from the Postgres instance.

```bash
curl "http://localhost:8000/api/customers/1"
```

---

### 🧪 Flask Mock Server (Port 5000)

The native source truth simulation.

#### `GET /api/customers`

Returns a paginated list of customers directly from the local JSON memory bank.

> **Parameters**: `page`, `limit`

```bash
curl "http://localhost:5000/api/customers?page=1&limit=2"
```

#### `GET /api/customers/{id}`

Returns a single mock customer by their string ID from the JSON data.

```bash
curl "http://localhost:5000/api/customers/1"
```

#### `POST /api/customers`

Appends a new customer record directly into the JSON simulation file natively (used for testing).

```bash
curl -X POST "http://localhost:5000/api/customers" \
     -H "Content-Type: application/json" \
     -d '{
           "first_name": "Test",
           "last_name": "User",
           "email": "test@example.com",
           "phone": "123-456-7890",
           "date_of_birth": "1990-01-01"
         }'
```

#### `GET /api/health`

Health check endpoint.

```bash
curl http://localhost:5000/api/health
```
