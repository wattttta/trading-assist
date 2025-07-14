import infra.line_notify as line_notify
import domain.constants as constants
from domain.stock import Stock

def notify_rsi_signal(stocks: list[Stock], threshold: float):
    jp_stocks = []
    us_stocks = []

    for stock in stocks:
        if stock.rsi > threshold:
            if stock.is_japan:
                jp_stocks.append(stock)
            else:
                us_stocks.append(stock)

    total_count = len(jp_stocks) + len(us_stocks)
    messages = []
    common_msg = f"{total_count}銘柄の最新RSIが{threshold}を超えました。\n"

    if jp_stocks:
        messages.append(
            "\n日本株\n" +
            "\n".join([f"{s.ticker}, {s.short_name}: {s.rsi}" for s in jp_stocks])
        )
    if us_stocks:
        messages.append(
            "\n米国株\n" +
            "\n".join([f"{s.ticker}, {s.short_name}: {s.rsi}" for s in us_stocks])
        )

    if messages:
        line_notify.send_line_message(
            constants.LINE_NOTIFY_API_TOKEN,
            common_msg + "\n\n".join(messages)
        )