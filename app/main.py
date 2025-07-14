from domain.constants import RSI_THRESHOLD
from application.rsi_notify_service import notify_rsi_signal
from application.get_stocks_service import get_stocks

# DBから株の情報を取得する
stocks = get_stocks()

# RSIの閾値を超えた株の情報を通知する
notify_rsi_signal(stocks, RSI_THRESHOLD)