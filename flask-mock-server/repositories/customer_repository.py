import json
import os

class CustomerRepository:
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

    def get_by_id(self, customer_id):
        return next((c for c in self._customers if c['customer_id'] == customer_id), None)
