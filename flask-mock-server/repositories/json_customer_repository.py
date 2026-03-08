import json
import os

class JsonCustomerRepository:
    def __init__(self, data_file='data/customers.json'):
        self.data_file = data_file
        self._customers = self._load_data()

    def _load_data(self):
        if not os.path.exists(self.data_file):
            return []
        with open(self.data_file, 'r') as f:
            return json.load(f)

    def get_all(self):
        return self._customers

    def get_paginated(self, page=1, limit=10):
        start = (page - 1) * limit
        end = start + limit
        paginated_data = self._customers[start:end]
        return {
            "data": paginated_data,
            "total": len(self._customers),
            "page": page,
            "limit": limit
        }

    def get_by_id(self, customer_id):
        return next((cust for cust in self._customers if str(cust["customer_id"]) == str(customer_id)), None)

    def add_customer(self, customer_data):
        self._customers.append(customer_data)
        self._save_data()
        return customer_data
        
    def _save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self._customers, f, indent=4)
