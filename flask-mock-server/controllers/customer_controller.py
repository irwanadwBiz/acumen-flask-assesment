from flask import Blueprint, request, jsonify
from services.customer_service import CustomerService
from repositories.customer_repository import CustomerRepository

customer_repo = CustomerRepository()
customer_service = CustomerService(customer_repo)

customer_bp = Blueprint('customer_bp', __name__)

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

@customer_bp.route('/api/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """
    Get Customer by ID
    ---
    parameters:
      - name: customer_id
        in: path
        type: integer
        required: true
        description: The ID of the customer
    responses:
      200:
        description: Customer details
      404:
        description: Customer not found
    """
    customer = customer_service.get_customer_by_id(customer_id)
    
    if customer:
        return jsonify(customer), 200
    else:
        return jsonify({"error": "Customer not found"}), 404
