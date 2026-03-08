from models.pipeline_customer_model import CustomerModel
from pipeline_database import SessionLocal

class PipelineCustomerRepository:
    def get_paginated(self, page: int, limit: int):
        db = SessionLocal()
        try:
            total = db.query(CustomerModel).count()
            offset = (page - 1) * limit
            customers = db.query(CustomerModel).offset(offset).limit(limit).all()
            return customers, total
        finally:
            db.close()

    def get_by_id(self, customer_id: str):
        db = SessionLocal()
        try:
            return db.query(CustomerModel).filter(CustomerModel.customer_id == customer_id).first()
        finally:
            db.close()
