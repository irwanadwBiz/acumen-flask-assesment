from flask import Flask, jsonify
from flasgger import Swagger
from controllers.customer_controller import customer_bp

app = Flask(__name__)
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
