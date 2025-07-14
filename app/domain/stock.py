import yfinance as yf
from domain.constants import RSI_PERIOD

class Stock:
    def __init__(self, ticker: str, is_japan: bool):
        if is_japan:
            ticker = f"{ticker}.T"
        else:
            ticker = ticker.upper()
        stock = yf.Ticker(ticker)
        info = stock.info

        self.ticker: str = ticker
        self.short_name: str = info.get('shortName')
        self.rsi: float = self._get_latest_rsi().values[0].round(2)
        self.is_japan = is_japan

    def _get_latest_rsi(self, period=RSI_PERIOD):
        df = yf.download(self.ticker, period=f"{period+1}d", interval="1d", auto_adjust=True)
        if df.empty or "Close" not in df:
            return None
        close = df["Close"]
        delta = close.diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1] if not rsi.empty else None