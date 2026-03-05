class CustomerService:
    def __init__(self, repository):
        self.repository = repository

    def get_paginated_customers(self, page, limit):
        all_customers = self.repository.get_all()
        
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        
        paginated_data = all_customers[start_idx:end_idx]
        
        return {
            "data": paginated_data,
            "total": len(all_customers),
            "page": page,
            "limit": limit
        }

    def get_customer_by_id(self, customer_id):
        customer = self.repository.get_by_id(customer_id)
        return customer
