from flask import Blueprint, request, jsonify
from services.customer_service import CustomerService
from repositories.customer_repository import CustomerRepository
from repositories.json_customer_repository import JsonCustomerRepository
from services.ingestion_service import IngestionService
from models.customer import Customer
from database import db
import uuid
from datetime import datetime

# Setup Repositories and Services
json_repo = JsonCustomerRepository()
customer_repo = CustomerRepository()

customer_service = CustomerService(customer_repo)
ingestion_service = IngestionService(json_repo)

customer_bp = Blueprint('customer_bp', __name__)

@customer_bp.route('/api/ingest', methods=['POST'])
def ingest_customers():
    """
    Ingest Customers from Mock Source using dlt
    ---
    responses:
      200:
        description: Success message with number of records processed
      500:
        description: Error processing ingestion
    """
    try:
        result = ingestion_service.ingest_data()
        return jsonify({
            "status": "success", 
            "records_processed": result["records_processed"]
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@customer_bp.route('/api/customers', methods=['POST'])
def create_customer():
    """
    Create a new Single Customer
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            first_name:
              type: string
            last_name:
              type: string
            email:
              type: string
            phone:
              type: string
            address:
              type: string
            account_balance:
              type: number
            date_of_birth:
              type: string
              format: date
    responses:
      201:
        description: Customer created successfully
      400:
        description: Invalid input
    """
    data = request.json
    if not data or not data.get('first_name') or not data.get('last_name') or not data.get('email'):
        return jsonify({"error": "first_name, last_name, and email are required"}), 400

    new_customer = Customer(
        customer_id=str(uuid.uuid4())[:8],  # Auto generate an ID for this simple API 
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        phone=data.get('phone'),
        address=data.get('address'),
        account_balance=data.get('account_balance', 0.0)
    )
    
    if data.get('date_of_birth'):
        try:
            new_customer.date_of_birth = datetime.strptime(data.get('date_of_birth'), '%Y-%m-%d').date()
        except ValueError:
            pass # Ignore invalid date formats for now

    db.session.add(new_customer)
    db.session.commit()

    return jsonify({"message": "Customer created successfully", "customer_id": new_customer.customer_id}), 201

@customer_bp.route('/api/customers', methods=['GET'])
def get_customers():
    """
    Get Paginated Customers
    ---
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        default: 1
        description: Page number
      - name: limit
        in: query
        type: integer
        required: false
        default: 10
        description: Items per page
    responses:
      200:
        description: A list of customers
    """
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    result = customer_service.get_paginated_customers(page, limit)
    
    return jsonify(result), 200

@customer_bp.route('/api/customers/<string:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """
    Get Customer by ID
    ---
    parameters:
      - name: customer_id
        in: path
        type: string
        required: true
        description: The ID of the customer
    responses:
      200:
        description: Customer details
      404:
        description: Customer not found
    """
    # Note: Using <string:customer_id> since DB id is VARCHAR(50) now
    customer = customer_service.get_customer_by_id(customer_id)
    
    if customer:
        return jsonify(customer), 200
    else:
        return jsonify({"error": "Customer not found"}), 404
