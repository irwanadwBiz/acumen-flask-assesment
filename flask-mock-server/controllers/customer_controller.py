from flask import Blueprint, request, jsonify
from services.customer_service import CustomerService
from repositories.customer_repository import CustomerRepository
from repositories.json_customer_repository import JsonCustomerRepository
from models.customer import Customer
from database import db
import uuid
from datetime import datetime

# Setup Repositories and Services
json_repo = JsonCustomerRepository()

customer_service = CustomerService(json_repo)
customer_bp = Blueprint('customer_bp', __name__)

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

    new_customer_data = {
        "customer_id": str(uuid.uuid4())[:8],
        "first_name": data.get('first_name'),
        "last_name": data.get('last_name'),
        "email": data.get('email'),
        "phone": data.get('phone'),
        "address": data.get('address'),
        "account_balance": data.get('account_balance', 0.0),
        "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    
    if data.get('date_of_birth'):
        new_customer_data["date_of_birth"] = data.get('date_of_birth')

    customer_service.create_customer(new_customer_data)

    return jsonify({"message": "Customer created successfully", "customer_id": new_customer_data["customer_id"]}), 201

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
