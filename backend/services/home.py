from config import supabase
from datetime import date

class HomeAnalytics:
    def get_summary_metrics(self):
        """Fetch key metrics for the dashboard."""
        try:
            # Total Sales Count
            total_sales = supabase.table('sales').select('item_id', count='exact').execute().count
            
            # Total Stitching Orders
            total_stitching_orders = supabase.table('stitching').select('stitching_id', count='exact').execute().count
            
            # Total Revenue (Sales + Stitching)
            sales_revenue = supabase.table('sales').select('selling_price').execute()
            stitching_revenue = supabase.table('stitching').select('selling_price').execute()
            total_revenue = sum(item['selling_price'] for item in sales_revenue.data) + sum(item['selling_price'] for item in stitching_revenue.data)
            
            return {
                "total_sales": total_sales,
                "total_stitching_orders": total_stitching_orders,
                "total_revenue": total_revenue
            }
        except Exception as e:
            raise Exception(f"Error fetching summary metrics: {str(e)}")

    def get_monthly_sales(self):
        """Fetch monthly sales data."""
        try:
            result = supabase.table('monthly_sales').select('*').execute()
            return result.data
        except Exception as e:
            raise Exception(f"Error fetching monthly sales data: {str(e)}")
    
    def get_pending_orders(self):
        """Fetch all pending and working orders based on expected date."""
        try:
            today = date.today().isoformat()
            
            # Fetch pending sales (expected_date has passed)
            pending_sales = supabase.table('sales').select('*').lt('expected_date', today).execute()
            
            # Fetch working sales (between order_date and expected_date)
            working_sales = supabase.table('sales').select('*').gte('expected_date', today).execute()
            
            # Fetch pending stitching (expected_date has passed)
            pending_stitching = supabase.table('stitching').select('*').lt('expected_date', today).execute()
            
            # Fetch working stitching (between order_date and expected_date)
            working_stitching = supabase.table('stitching').select('*').gte('expected_date', today).execute()
            
            return {
                "pending_sales": pending_sales.data,
                "working_sales": working_sales.data,
                "pending_stitching": pending_stitching.data,
                "working_stitching": working_stitching.data
            }
        except Exception as e:
            raise Exception(f"Error fetching pending orders: {str(e)}")
