from flask import Flask
from api.api_endpts import stock_bp, sales_bp

app = Flask(__name__)

# Register the Blueprint for stock routes
app.register_blueprint(stock_bp)

# Register the Blueprint for sales routes
app.register_blueprint(sales_bp)

@app.route('/')
def home():
    return {
        "message": "Welcome to the Inventory and Sales Management API"
    }

if __name__ == '__main__':
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
