from flask import Blueprint, request, jsonify
from services.stock import StockManager
from services.sales import SalesManager

# Create Blueprint
stock_bp = Blueprint('stock', __name__)
sales_bp = Blueprint('sales', __name__)
stock_manager = StockManager()
sales_manager = SalesManager()

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
    
    # Create Sale
@sales_bp.route('/', methods=['POST'])
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
@sales_bp.route('/', methods=['GET'])
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
@sales_bp.route('/<sale_id>', methods=['GET'])
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
@sales_bp.route('/<sale_id>', methods=['PUT'])
def update_sale(sale_id):
    try:
        data = request.get_json()
        result = sales_manager.update_sale(sale_id, data)
        return jsonify({
            'message': 'Sale record updated successfully',
            'data': result
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete Sale
@sales_bp.route('/<sale_id>', methods=['DELETE'])
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

