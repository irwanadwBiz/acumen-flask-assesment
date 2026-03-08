class CustomerService:
    def __init__(self, repository):
        self.repository = repository

    def get_paginated_customers(self, page, limit):
        return self.repository.get_paginated(page, limit)

    def get_customer_by_id(self, customer_id):
        customer = self.repository.get_by_id(customer_id)
        return customer
        
    def create_customer(self, customer_data):
        return self.repository.add_customer(customer_data)
