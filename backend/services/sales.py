from datetime import datetime
from config import supabase

class SalesManager:
    @staticmethod
    def validate_sales_data(data, required_fields):
        """Validate if all required fields are present in the data."""
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
        return True

    def create_sale(self, data):
        """Create a new sale entry."""
        try:
            required_fields = ['mode', 'selling_price', 'cost_price', 'item_name', 'cust_name', 'order_date']
            
            self.validate_sales_data(data, required_fields)

            # Set default values
            data['order_date'] = data.get('order_date', datetime.now().isoformat())
            data['stitching'] = data.get('stitching', False)

            result = supabase.table('sales').insert(data).execute()
            return result.data[0]
            
        except Exception as e:
            raise Exception(f"Error creating sale: {str(e)}")

    def get_all_sales(self):
        """Retrieve all sales records."""
        try:
            result = supabase.table('sales').select('*').execute()
            return result.data
        except Exception as e:
            raise Exception(f"Error retrieving sales records: {str(e)}")

    def get_sale_by_id(self, sale_id):
        """Retrieve a specific sale by ID."""
        try:
            result = supabase.table('sales').select('*').eq('item_id', sale_id).execute()
            if not result.data:
                raise ValueError(f"Sale record with ID {sale_id} not found")
            return result.data[0]
        except Exception as e:
            raise Exception(f"Error retrieving sale record: {str(e)}")

    def update_sale(self, sale_id, data):
        """Update an existing sale."""
        try:
            # Verify item exists
            existing_sale = self.get_sale_by_id(sale_id)

            result = supabase.table('sales').update(data).eq('item_id', sale_id).execute()
            return result.data[0]
        
        except Exception as e:
            raise Exception(f"Error updating sale record: {str(e)}")

    def delete_sale(self, sale_id):
        """Delete a sale record."""
        try:
            # Verify item exists
            self.get_sale_by_id(sale_id)

            result = supabase.table('sales').delete().eq('item_id', sale_id).execute()
            return result.data[0]
        
        except Exception as e:
            raise Exception(f"Error deleting sale record: {str(e)}")
