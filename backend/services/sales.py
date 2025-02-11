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
        """Create a new sale entry with stitching reference if required."""
        try:
            required_fields = ['item_name', 'cost_price', 'selling_price', 'mode', 'cust_name', 'order_date']
            self.validate_sales_data(data, required_fields)

            # Insert sale record first
            result = supabase.table('sales').insert(data).execute()
            sale_record = result.data[0]

            # Handle stitching reference creation only after successful sale
            if data.get('stitching', False):
                stitching_data = {
                    "item_id": sale_record["item_id"],
                    "stitching_preference": "TBD",
                    "tailor_price": 0,
                    "selling_price": 0,
                    "item_name": data['item_name'],
                    "cust_name": data['cust_name'],
                    "expected_date": data.get('order_date'),
                    "order_date": data.get('order_date', datetime.now().isoformat())
                }
                supabase.table('stitching').insert(stitching_data).execute()

            return sale_record

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
