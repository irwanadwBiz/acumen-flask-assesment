.PHONY: start dev data start-docker start-local

start-docker:
	docker-compose up -d --build

start-local:
	DATABASE_URL=postgresql://postgres:password@localhost:5433/customer_db venv/bin/python app.py

start:
	venv/bin/python app.py

dev:
	venv/bin/flask --app app.py run --debug --host=0.0.0.0 --port=5000

data:
	venv/bin/python generate_data.py
