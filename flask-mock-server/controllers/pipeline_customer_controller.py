from fastapi import APIRouter, HTTPException, Query
from services.pipeline_ingestion_service import PipelineIngestionService
from repositories.pipeline_customer_repository import PipelineCustomerRepository

router = APIRouter(prefix="/api")

ingestion_service = PipelineIngestionService()
repository = PipelineCustomerRepository()

@router.post(
    "/ingest",
    summary="Ingest Customers",
    description="Fetches mock customer data from the Flask API and upserts it into the PostGIS database using dlt.",
    responses={
        200: {
            "description": "Ingestion successful",
            "content": {
                "application/json": {
                    "example": {"status": "success", "records_processed": 25}
                }
            }
        },
        500: {"description": "Internal Server Error during ingestion"}
    }
)
async def ingest_data():
    """
    Trigger the DLT pipeline to extract data from the Mock Server
    and load it into the PostgreSQL database.
    """
    return await ingestion_service.ingest()

@router.get("/customers")
def get_customers(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    customers, total = repository.get_paginated(page, limit)
    
    data = []
    for c in customers:
        data.append({
            "customer_id": c.customer_id,
            "first_name": c.first_name,
            "last_name": c.last_name,
            "email": c.email,
            "phone": c.phone,
            "address": c.address,
            "date_of_birth": c.date_of_birth.isoformat() if c.date_of_birth else None,
            "account_balance": float(c.account_balance) if c.account_balance else None,
            "created_at": c.created_at.isoformat() if c.created_at else None
        })
        
    return {
        "data": data,
        "total": total,
        "page": page,
        "limit": limit
    }

@router.get("/customers/{customer_id}")
def get_customer(customer_id: str):
    c = repository.get_by_id(customer_id)
    if not c:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return {
        "customer_id": c.customer_id,
        "first_name": c.first_name,
        "last_name": c.last_name,
        "email": c.email,
        "phone": c.phone,
        "address": c.address,
        "date_of_birth": c.date_of_birth.isoformat() if c.date_of_birth else None,
        "account_balance": float(c.account_balance) if c.account_balance else None,
        "created_at": c.created_at.isoformat() if c.created_at else None
    }
