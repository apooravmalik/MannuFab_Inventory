from flask import Blueprint, request, jsonify
from config import supabase
from services.stock import StockManager
from services.sales import SalesManager
from services.stitching import StitchingManager
from services.billing import BillingManager
from services.home import HomeAnalytics
from flask_cors import cross_origin

# Create Blueprint
stock_bp = Blueprint('stock', __name__)
sales_bp = Blueprint('sales', __name__)
stitching_bp = Blueprint('stitching', __name__)
billing_bp = Blueprint('billing', __name__)
home_bp = Blueprint('home', __name__)
auth_bp = Blueprint('auth', __name__)

# Initialize Services
stock_manager = StockManager()
sales_manager = SalesManager()
stitching_manager = StitchingManager()
billing_manager = BillingManager()
home_analytics = HomeAnalytics()

""" 
    ALL THESE API ENDPOINTS DONT REQUIRE BASE URL ------- THEY JUST REQUIRE PARAMETERS ,i.e ID
    BASE URL IS DEFINED IN main.py
    """

# Create Stock Item
@stock_bp.route('/', methods=['POST'])
def create_stock():
    try:
        data = request.get_json()
        result = stock_manager.create_stock_item(data)
        
        return jsonify({
            'message': 'Stock item created successfully',
            'data': result
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get All Stock Items
@stock_bp.route('/', methods=['GET'])
def get_all_stock():
    try:
        result = stock_manager.get_all_stock()
        return jsonify({
            'message': 'Stock items retrieved successfully',
            'data': result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get Stock Item by ID
@stock_bp.route('/<item_id>', methods=['GET'])
def get_stock_by_id(item_id):
    try:
        result = stock_manager.get_stock_by_id(item_id)
        return jsonify({
            'message': 'Stock item retrieved successfully',
            'data': result
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update Stock Item
@stock_bp.route('/<item_id>', methods=['PUT'])
def update_stock(item_id):
    try:
        data = request.get_json()
        result = stock_manager.update_stock_item(item_id, data)
        
        return jsonify({
            'message': 'Stock item updated successfully',
            'data': result
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete Stock Item
@stock_bp.route('/<item_id>', methods=['DELETE'])
def delete_stock(item_id):
    try:
        result = stock_manager.delete_stock_item(item_id)
        
        return jsonify({
            'message': 'Stock item deleted successfully',
            'data': result
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# Sales Endpoints    
@sales_bp.route('/', methods=['OPTIONS'])
@cross_origin(origin="http://localhost:5173", supports_credentials=True)
def handle_sales_options():
    return '', 204  # Return 204 No Content (Preflight Passed)
    
    # Create Sale
@sales_bp.route('', methods=['POST'])
def create_sale():
    try:
        data = request.get_json()
        result = sales_manager.create_sale(data)
        return jsonify({
            'message': 'Sale created successfully',
            'data': result
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get All Sales
@sales_bp.route('', methods=['GET'])
def get_all_sales():
    try:
        result = sales_manager.get_all_sales()
        return jsonify({
            'message': 'Sales records retrieved successfully',
            'data': result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get Sale by ID
@sales_bp.route('<sale_id>', methods=['GET'])
def get_sale_by_id(sale_id):
    try:
        result = sales_manager.get_sale_by_id(sale_id)
        return jsonify({
            'message': 'Sale record retrieved successfully',
            'data': result
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update Sale
@sales_bp.route('<sale_id>', methods=['PUT'])
def update_sale(sale_id):
    try:
        print(f"Updating sale with ID: {sale_id} (type: {type(sale_id)})")
        data = request.get_json()
        print(f"Data received: {data}")
        
        # Try converting the ID to an integer if needed
        # Some databases require numeric IDs
        try:
            numeric_id = int(sale_id)
            result = sales_manager.update_sale(numeric_id, data)
        except ValueError:
            # If conversion fails, use the original ID
            result = sales_manager.update_sale(sale_id, data)
            
        return jsonify({
            'message': 'Sale record updated successfully',
            'data': result
        }), 200
    except ValueError as e:
        print(f"ValueError: {str(e)}")
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        print(f"Exception: {str(e)}")
        import traceback
        traceback.print_exc()  # Print full stack trace
        return jsonify({'error': str(e)}), 500

# Delete Sale
@sales_bp.route('<sale_id>', methods=['DELETE'])
def delete_sale(sale_id):
    try:
        result = sales_manager.delete_sale(sale_id)
        return jsonify({
            'message': 'Sale record deleted successfully',
            'data': result
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Stitching APIs

@stitching_bp.route('/', methods=['OPTIONS'])
def handle_stitching_options():
    return '', 204  # Return 204 No Content (Preflight Passed

# Create Stitching Record
@stitching_bp.route('', methods=['POST'])
def create_stitching():
    try:
        data = request.get_json()
        result = stitching_manager.create_stitching_record(data)
        return jsonify({
            'message': 'Stitching record created successfully',
            'data': result
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get All Stitching Records
@stitching_bp.route('/', methods=['GET'])
def get_all_stitching():
    try:
        result = stitching_manager.get_all_stitching_records()
        return jsonify({
            'message': 'Stitching records retrieved successfully',
            'data': result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get Stitching Record by ID
@stitching_bp.route('<stitching_id>', methods=['GET'])
def get_stitching_by_id(stitching_id):
    try:
        result = stitching_manager.get_stitching_record_by_id(stitching_id)
        return jsonify({
            'message': 'Stitching record retrieved successfully',
            'data': result
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update Stitching Record
@stitching_bp.route('<stitching_id>', methods=['PUT'])
def update_stitching(stitching_id):
    try:
        data = request.get_json()
        result = stitching_manager.update_stitching_record(stitching_id, data)
        return jsonify({
            'message': 'Stitching record updated successfully',
            'data': result
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete Stitching Record
@stitching_bp.route('<stitching_id>', methods=['DELETE'])
def delete_stitching(stitching_id):
    try:
        result = stitching_manager.delete_stitching_record(stitching_id)
        return jsonify({
            'message': 'Stitching record deleted successfully',
            'data': result
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Billing APIs

# Create Bill
@billing_bp.route('/', methods=['POST'])
def create_bill():
    try:
        data = request.get_json()
        result = billing_manager.create_bill(data)
        return jsonify({
            'message': 'Bill created successfully',
            'data': result
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get All Bills
@billing_bp.route('/', methods=['GET'])
def get_all_bills():
    try:
        result = billing_manager.get_all_bills()
        return jsonify({
            'message': 'Billing records retrieved successfully',
            'data': result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get Bill by ID
@billing_bp.route('/<bill_id>', methods=['GET'])
def get_bill_by_id(bill_id):
    try:
        result = billing_manager.get_bill_by_id(bill_id)
        return jsonify({
            'message': 'Bill record retrieved successfully',
            'data': result
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete Bill
@billing_bp.route('/<bill_id>', methods=['DELETE'])
def delete_bill(bill_id):
    try:
        result = billing_manager.delete_bill(bill_id)
        return jsonify({
            'message': 'Bill record deleted successfully',
            'data': result
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
# Home Analytics APIs

# Get Pending Orders
@home_bp.route('/pending-orders', methods=['GET'])
def get_pending_orders():
    try:
        result = home_analytics.get_pending_orders()
        return jsonify({
            'message': 'Pending orders retrieved successfully',
            'data': result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get Summary Metrics
@home_bp.route('/summary', methods=['GET'])
def get_summary_metrics():
    try:
        result = home_analytics.get_summary_metrics()
        return jsonify({
            'message': 'Summary metrics retrieved successfully',
            'data': result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get Monthly Sales Data
@home_bp.route('/monthly-sales', methods=['GET'])
def get_monthly_sales():
    try:
        result = home_analytics.get_monthly_sales()
        return jsonify({
            'message': 'Monthly sales data retrieved successfully',
            'data': result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
# login 

@auth_bp.route('/login', methods=['OPTIONS'])
@cross_origin(origin="http://localhost:5173", supports_credentials=True)
def handle_options():
    return '', 204  # Return 204 No Content (Preflight Passed)
@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user with Supabase."""
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        # Authenticate using Supabase
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})

        # Use dot notation to access attributes
        if response.user is None:
            return jsonify({"error": "Invalid credentials"}), 401

        return jsonify({
            "message": "Login successful",
            "session": {
                "access_token": response.session.access_token,
                "refresh_token": response.session.refresh_token
            },
            "user": {
                "id": response.user.id,
                "email": response.user.email
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

