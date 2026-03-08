import json
from datetime import datetime, timedelta
from faker import Faker
import random

fake = Faker()

customers = []
for i in range(1, 26):
    customer = {
        "customer_id": str(i),
        "first_name": f"{fake.first_name()}",
        "last_name": f"{fake.last_name()}",
        "email": f"{fake.email()}",
        "phone": f"{fake.phone_number()}",
        "address": f"{fake.address()}",
        "date_of_birth": (datetime.now() - timedelta(days=random.randint(7000, 20000))).strftime("%Y-%m-%d"),
        "account_balance": round(random.uniform(100.0, 5000.0), 2),
        "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    customers.append(customer)

with open("data/customers.json", "w") as f:
    json.dump(customers, f, indent=4)

print("Generated 25 customers in data/customers.json")  