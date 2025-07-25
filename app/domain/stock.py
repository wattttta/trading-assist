import yfinance as yf
from domain.constants import RSI_PERIOD, STOCK_PERIOD, MACD_THRESHOLD

class Stock:
    def __init__(self, ticker: str, is_japan: bool):
        if is_japan:
            ticker = f"{ticker}.T"
        else:
            ticker = ticker.upper()
        stock = yf.Ticker(ticker)
        info = stock.info
        self.detail = yf.download(ticker, period=f"{STOCK_PERIOD}d", interval="1d", auto_adjust=True)
        self.ticker: str = ticker
        self.short_name: str = info.get('shortName')
        self.rsi: float = self._get_latest_rsi().values[0].round(2)
        self.sell_signal: bool = self._get_macd_sell_signal()
        self.is_japan: bool = is_japan

    def _get_latest_rsi(self, period=RSI_PERIOD):
        if self.detail.empty or "Close" not in self.detail:
            return None
        close = self.detail["Close"]
        delta = close.diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1] if not rsi.empty else None

    def _get_macd_sell_signal(self, threshold=MACD_THRESHOLD):
        if self.detail.empty or "Close" not in self.detail:
            return None
        
        close = self.detail['Close']
        ema_12 = close.ewm(span=12, adjust=False).mean()
        ema_26 = close.ewm(span=26, adjust=False).mean()
        macd = ema_12 - ema_26
        signal = macd.ewm(span=9, adjust=False).mean()

        macd_today = float(macd.iloc[-1].iloc[0])
        signal_today = float(signal.iloc[-1].iloc[0])
        macd_yesterday = float(macd.iloc[-2].iloc[0])
        signal_yesterday = float(signal.iloc[-2].iloc[0])

        spread_today = macd_today - signal_today
        spread_yesterday = macd_yesterday - signal_yesterday

        if (
            spread_today > 0 and
            spread_today < threshold and
            spread_today < spread_yesterday
        ):
            return True
        return False