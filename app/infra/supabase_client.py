from supabase import create_client, Client

SUPABASE_URL = "https://jesrylmlprkgcenznnow.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Implc3J5bG1scHJrZ2Nlbnpubm93Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MjI3OTM3MiwiZXhwIjoyMDY3ODU1MzcyfQ.iWWigZjrpfOiIjhKEWFM46Ak11VJELwkKky8C8MOo9Q"

def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_table(table_name):
    supabase = get_supabase_client()
    data = supabase.table(table_name).select("*").execute()
    return data.data