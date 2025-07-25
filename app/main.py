from domain.constants import RSI_THRESHOLD
from application.rsi_notify_service import notify_rsi_signal
from application.get_stocks_service import get_stocks
from application.macd_sell_notify_service import macd_sell_notify

def main(request):
    # DBから株の情報を取得する
    stocks = get_stocks()

    # RSIの閾値を超えた株の情報を通知する
    notify_rsi_signal(stocks, RSI_THRESHOLD)

    # MACDの売りシグナルを発信する
    macd_sell_notify(stocks)    

    return "Done"

# Development -----------------------------------------------------------------
# stocks = get_stocks()
# macd_sell_notify(stocks)    
# print(stocks)