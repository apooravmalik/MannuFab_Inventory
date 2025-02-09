from flask import Blueprint, request, jsonify
from services.stock import StockManager

# Create Blueprint
stock_bp = Blueprint('stock', __name__)
stock_manager = StockManager()

# Create Stock Item
@stock_bp.route('/api/stock', methods=['POST'])
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
@stock_bp.route('/api/stock', methods=['GET'])
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
@stock_bp.route('/api/stock/<item_id>', methods=['GET'])
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
@stock_bp.route('/api/stock/<item_id>', methods=['PUT'])
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
@stock_bp.route('/api/stock/<item_id>', methods=['DELETE'])
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