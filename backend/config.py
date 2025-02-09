import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

def get_supabase_client():
    """Create and return a Supabase client."""
    print("Testing Supabase connection...")
    try:
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        # Test query to verify the connection
        response = client.table('sales').select('*').limit(1).execute()
        print("Supabase connection successful. Test response:", response.data)
        return client
    except Exception as e:
        print(f"Supabase connection error: {e}")
        return None

supabase = get_supabase_client()
