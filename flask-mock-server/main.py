from fastapi import FastAPI
from controllers.pipeline_customer_controller import router as customer_router
import os
from pipeline_database import engine, Base

app = FastAPI()

# Make sure tables are created 
Base.metadata.create_all(bind=engine)

app.include_router(customer_router)
