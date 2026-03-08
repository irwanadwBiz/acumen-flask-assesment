from sqlalchemy import Column, String, Text, Date, Numeric, DateTime
from pipeline_database import Base, engine

class CustomerModel(Base):
    __tablename__ = "customers"
    customer_id = Column(String(50), primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50))
    address = Column(Text)
    date_of_birth = Column(Date)
    account_balance = Column(Numeric(15, 2))
    created_at = Column(DateTime)

# Create tables
Base.metadata.create_all(bind=engine)
