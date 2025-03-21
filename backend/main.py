from flask import Flask
from api.api_endpts import stock_bp, sales_bp, stitching_bp, billing_bp, home_bp, auth_bp
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {
    "origins": "http://localhost:5173",
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}}, supports_credentials=True)

# Register the Blueprint for stock routes
app.register_blueprint(stock_bp, url_prefix='/api/stock')

# Register the Blueprint for sales routes
app.register_blueprint(sales_bp, url_prefix='/api/sales')

# Register the Blueprint for stitching routes
app.register_blueprint(stitching_bp, url_prefix='/api/stitching')

# Register the Blueprint for stitching routes
app.register_blueprint(billing_bp, url_prefix='/api/billing')

# Register the Blueprint for anaylytics routes
app.register_blueprint(home_bp, url_prefix='/api/analytics')

# Register the Blueprint for authentication routes
app.register_blueprint(auth_bp, url_prefix='/api/auth')

@app.route('/')
def home():
    return {
        "message": "Welcome to the Inventory and Sales Management API"
    }

if __name__ == '__main__':
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
