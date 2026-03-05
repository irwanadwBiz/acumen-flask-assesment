from models.customer import Customer

class CustomerRepository:
    def get_paginated(self, page=1, limit=10):
        # Using pagination directly on SQLAlchemy query
        pagination = Customer.query.paginate(page=page, per_page=limit, error_out=False)
        return {
            "data": [customer.to_dict() for customer in pagination.items],
            "total": pagination.total,
            "page": page,
            "limit": limit
        }

    def get_by_id(self, customer_id):
        # Using SQLAlchemy get
        customer = Customer.query.get(customer_id)
        return customer.to_dict() if customer else None
