from infra.supabase_client import fetch_table
from domain.stock import Stock

def get_stocks() -> list[Stock]:
    stocks_data = fetch_table("stocks")
    return list(map(lambda data: Stock(data["ticker"], data["type"] == "Japan"), stocks_data))