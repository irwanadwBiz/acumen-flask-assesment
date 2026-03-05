from flask import Flask, jsonify
from flasgger import Swagger
import os
from database import db
from controllers.customer_controller import customer_bp

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 
    'sqlite:///customers.db' # Fallback for local testing
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables based on models
with app.app_context():
    import models.customer
    # db.create_all() # Let dlt handle schema creation for better compatibility

swagger = Swagger(app)

# Register the blueprint from our controller
app.register_blueprint(customer_bp)

# Health Check Endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health Check Endpoint
    ---
    responses:
      200:
        description: API is healthy
    """
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    # Run server on port 5000 
    app.run(host='0.0.0.0', port=5000)
