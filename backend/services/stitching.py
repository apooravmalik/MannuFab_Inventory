from datetime import datetime
from config import supabase

class StitchingManager:
    @staticmethod
    def validate_stitching_data(data, required_fields):
        """Validate if all required fields are present in the data."""
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
        return True

    def create_stitching_record(self, data):
        """Create a new stitching record."""
        try:
            # Validate required fields
            required_fields = ['stitching_preference', 'tailor_price', 'selling_price', 'expected_date', 'cust_name']
            self.validate_stitching_data(data, required_fields)

            # Check for item_id only if linked to sales
            if 'item_id' in data and data['item_id']:
                sale_check = supabase.table('sales').select('item_id').eq('item_id', data['item_id']).execute()
                if not sale_check.data:
                    raise ValueError(f"Invalid item_id: {data['item_id']} - No matching sale found.")

            result = supabase.table('stitching').insert(data).execute()
            return result.data[0]
        except Exception as e:
            raise Exception(f"Error creating stitching record: {str(e)}")


    def get_all_stitching_records(self):
        """Retrieve all stitching records."""
        try:
            result = supabase.table('stitching').select('*').execute()
            return result.data
        except Exception as e:
            raise Exception(f"Error retrieving stitching records: {str(e)}")

    def get_stitching_record_by_id(self, stitching_id):
        """Retrieve a specific stitching record by ID."""
        try:
            result = supabase.table('stitching').select('*').eq('stitching_id', stitching_id).execute()
            if not result.data:
                raise ValueError(f"Stitching record with ID {stitching_id} not found")
            return result.data[0]
        except Exception as e:
            raise Exception(f"Error retrieving stitching record: {str(e)}")

    def update_stitching_record(self, stitching_id, data):
        """Update an existing stitching record."""
        try:
            # Verify item exists
            self.get_stitching_record_by_id(stitching_id)
            result = supabase.table('stitching').update(data).eq('stitching_id', stitching_id).execute()
            return result.data[0]
        except Exception as e:
            raise Exception(f"Error updating stitching record: {str(e)}")

    def delete_stitching_record(self, stitching_id):
        """Delete a stitching record."""
        try:
            self.get_stitching_record_by_id(stitching_id)  # Will raise ValueError if not found
            result = supabase.table('stitching').delete().eq('stitching_id', stitching_id).execute()
            return result.data[0]
        except Exception as e:
            raise Exception(f"Error deleting stitching record: {str(e)}")
