import httpx
import dlt
from dlt.destinations import postgres
from fastapi import HTTPException
import os
import datetime
from pipeline_database import DATABASE_URL

class PipelineIngestionService:
    async def ingest(self):
        mock_url = os.environ.get('MOCK_SERVER_URL', 'http://mock-server:5000/api/customers')
        
        all_customers = []
        page = 1
        limit = 100
        
        async with httpx.AsyncClient() as client:
            while True:
                try:
                    response = await client.get(f"{mock_url}?page={page}&limit={limit}")
                    response.raise_for_status()
                except httpx.RequestError as exc:
                    raise HTTPException(status_code=500, detail=f"Request to mock server failed: {str(exc)}")
                except httpx.HTTPStatusError as exc:
                    raise HTTPException(status_code=500, detail=f"Mock server returned error: {exc.response.status_code}")
                    
                data = response.json()
                customers = data.get("data", [])
                if not customers:
                    break
                    
                all_customers.extend(customers)
                
                if len(customers) < limit:
                    break
                page += 1
                
        if not all_customers:
            return {"status": "success", "records_processed": 0}

        @dlt.resource(name="customers", write_disposition="replace", primary_key="customer_id")
        def customer_resource():
            for customer in all_customers:
                if isinstance(customer.get("date_of_birth"), str) and customer.get("date_of_birth"):
                    try:
                        customer["date_of_birth"] = datetime.datetime.strptime(customer["date_of_birth"], "%Y-%m-%d")
                    except ValueError:
                        customer["date_of_birth"] = None
                else:
                    customer["date_of_birth"] = None
                        
                if isinstance(customer.get("created_at"), str) and customer.get("created_at"):
                    try:
                        customer["created_at"] = datetime.datetime.strptime(customer["created_at"], "%Y-%m-%dT%H:%M:%SZ")
                    except ValueError:
                        customer["created_at"] = None
                else:
                    customer["created_at"] = None
                    
                yield customer
                
        # Explicitly hint the types to avoid inference problems
        customer_resource.apply_hints(columns={
            "date_of_birth": {"data_type": "date"},
            "created_at": {"data_type": "timestamp"},
            "phone": {"data_type": "text"}
        })
                
        # Upsert using dlt
        pipeline = dlt.pipeline(
            pipeline_name="customer_pipeline",
            destination=postgres(credentials=DATABASE_URL),
            dataset_name="public",
        )
        
        load_info = pipeline.run(customer_resource)
        
        return {"status": "success", "records_processed": len(all_customers)}
