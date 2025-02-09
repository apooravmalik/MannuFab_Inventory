from datetime import datetime
from config import supabase

class StockManager:
    @staticmethod
    def validate_stock_data(data, required_fields):
        """Validate if all required fields are present in the data"""
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
        return True

    @staticmethod
    def calculate_margin(selling_price, cost_price):
        """Calculate margin from selling price and cost price"""
        return selling_price - cost_price

    def create_stock_item(self, data):
        """Create a new stock item."""
        try:
            required_fields = ['vendor_id', 'selling_price', 'cost_price', 
                            'item_name', 'quantity', 'size']
            
            self.validate_stock_data(data, required_fields)
            
            # Remove margin from the payload if present
            data.pop('margin', None)

            # Set default values
            data['order_date'] = data.get('order_date', datetime.now().isoformat())
            data['sold'] = data.get('sold', False)

            result = supabase.table('stock').insert(data).execute()
            return result.data[0]
        except Exception as e:
            raise Exception(f"Error creating stock item: {str(e)}")

    def get_all_stock(self):
        """Retrieve all stock items"""
        try:
            result = supabase.table('stock').select('*').execute()
            return result.data
        except Exception as e:
            raise Exception(f"Error retrieving stock items: {str(e)}")

    def get_stock_by_id(self, item_id):
        """Retrieve a specific stock item by ID"""
        try:
            result = supabase.table('stock').select('*').eq('item_id', item_id).execute()
            if not result.data:
                raise ValueError(f"Stock item with ID {item_id} not found")
            return result.data[0]
        except Exception as e:
            raise Exception(f"Error retrieving stock item: {str(e)}")

    def update_stock_item(self, item_id, data):
        """Update an existing stock item"""
        try:
            # Verify item exists
            existing_item = self.get_stock_by_id(item_id)
            
            # Update margin if price fields are modified
            if 'selling_price' in data or 'cost_price' in data:
                selling_price = data.get('selling_price', existing_item['selling_price'])
                cost_price = data.get('cost_price', existing_item['cost_price'])
                # data['margin'] = self.calculate_margin(selling_price, cost_price)
            
            result = supabase.table('stock').update(data).eq('item_id', item_id).execute()
            return result.data[0]
            
        except Exception as e:
            raise Exception(f"Error updating stock item: {str(e)}")

    def delete_stock_item(self, item_id):
        """Delete a stock item"""
        try:
            # Verify item exists
            self.get_stock_by_id(item_id)  # Will raise ValueError if not found
            
            result = supabase.table('stock').delete().eq('item_id', item_id).execute()
            return result.data[0]
            
        except Exception as e:
            raise Exception(f"Error deleting stock item: {str(e)}")