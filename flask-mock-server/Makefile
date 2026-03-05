.PHONY: start dev data

start-docker:
	docker run -p 5000:5000 flask-mock-server

start:
	venv/bin/python app.py

dev:
	venv/bin/flask --app app.py run --debug --host=0.0.0.0 --port=5000

data:
	venv/bin/python generate_data.py
