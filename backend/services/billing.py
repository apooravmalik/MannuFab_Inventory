from datetime import datetime
from config import supabase

class BillingManager:
    def create_bill(self, data):
        """Create a new bill by connecting stitching and sales tables."""
        try:
            item_id = data.get('item_id')
            if not item_id:
                raise ValueError("item_id is required for billing")

            # Initialize billing data
            total_amount = 0
            bill_details = {}

            # Fetch stitching data
            stitching_result = supabase.table('stitching').select('*').eq('item_id', item_id).execute()
            if stitching_result.data:
                stitching_data = stitching_result.data[0]
                total_amount += stitching_data['selling_price']
                bill_details.update({
                    "stitching_id": stitching_data['stitching_id'],
                    "stitching_price": stitching_data['selling_price'],
                    "stitching_preference": stitching_data['stitching_preference']
                })

            # Fetch sales data
            sales_result = supabase.table('sales').select('*').eq('item_id', item_id).execute()
            if sales_result.data:
                sales_data = sales_result.data[0]
                total_amount += sales_data['selling_price']
                bill_details.update({
                    "sale_price": sales_data['selling_price'],
                    "customer_name": sales_data['cust_name'],
                    "order_date": sales_data['order_date']
                })

            if not bill_details:
                raise ValueError(f"No related stitching or sales record found for item_id: {item_id}")

            # Insert billing record
            bill_data = {
                "item_id": item_id,
                "total_amount": total_amount,
                "bill_date": datetime.now().strftime('%Y-%m-%d'),
                "stitching_id": bill_details.get("stitching_id")
            }
            result = supabase.table('billing').insert(bill_data).execute()
            bill_details.update(bill_data)

            return bill_details

        except Exception as e:
            raise Exception(f"Error creating bill: {str(e)}")

    def get_all_bills(self):
        """Retrieve all billing records."""
        try:
            result = supabase.table('billing').select('*').execute()
            return result.data
        except Exception as e:
            raise Exception(f"Error retrieving billing records: {str(e)}")

    def get_bill_by_id(self, bill_id):
        """Retrieve a specific bill by ID."""
        try:
            result = supabase.table('billing').select('*').eq('bill_id', bill_id).execute()
            if not result.data:
                raise ValueError(f"Bill record with ID {bill_id} not found")
            return result.data[0]
        except Exception as e:
            raise Exception(f"Error retrieving bill record: {str(e)}")

    def delete_bill(self, bill_id):
        """Delete a bill record."""
        try:
            self.get_bill_by_id(bill_id)  # Ensure it exists
            result = supabase.table('billing').delete().eq('bill_id', bill_id).execute()
            return result.data[0]
        except Exception as e:
            raise Exception(f"Error deleting bill record: {str(e)}")
