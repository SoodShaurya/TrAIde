import yfinance as yf
import datetime

class Simulator:
    def __init__(self, initial_balance=10000):
        self.balance = initial_balance
        self.portfolio = {}
        self.transaction_history = []
        self.start_date = (datetime.datetime.now() - datetime.timedelta(days=180)).strftime('%Y-%m-%d')
        self.end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.current_date = self.start_date

    def get_stock_price(self, ticker):
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(start=self.start_date, end=self.end_date)
            if self.current_date in data.index:
                return round(data.loc[self.current_date]['Close'], 2)
            return None
        except Exception as e:
            print(f"Error fetching stock price: {e}")
            return None

    def buy_stock(self, ticker, quantity):
        price = self.get_stock_price(ticker)
        if price is None:
            print("Unable to fetch stock price. Try again.")
            return

        total_cost = price * quantity
        if total_cost > self.balance:
            print("Insufficient balance to complete this transaction.")
            return

        self.balance -= total_cost
        if ticker in self.portfolio:
            self.portfolio[ticker]['quantity'] += quantity
            self.portfolio[ticker]['avg_price'] = (
                (self.portfolio[ticker]['avg_price'] * self.portfolio[ticker]['quantity'] + total_cost) /
                (self.portfolio[ticker]['quantity'] + quantity)
            )
        else:
            self.portfolio[ticker] = {'quantity': quantity, 'avg_price': price}

        self.transaction_history.append(
            {'type': 'buy', 'ticker': ticker, 'quantity': quantity, 'price': price, 'date': self.current_date})
        print(f"Bought {quantity} shares of {ticker} at ${price:.2f} each. Remaining balance: ${self.balance:.2f}")

    def sell_stock(self, ticker, quantity):
        if ticker not in self.portfolio or self.portfolio[ticker]['quantity'] < quantity:
            print("You do not have enough shares to sell.")
            return

        price = self.get_stock_price(ticker)
        if price is None:
            print("Unable to fetch stock price. Try again.")
            return

        total_revenue = price * quantity
        self.balance += total_revenue
        self.portfolio[ticker]['quantity'] -= quantity

        if self.portfolio[ticker]['quantity'] == 0:
            del self.portfolio[ticker]

        self.transaction_history.append(
            {'type': 'sell', 'ticker': ticker, 'quantity': quantity, 'price': price, 'date': self.current_date})
        print(f"Sold {quantity} shares of {ticker} at ${price:.2f} each. New balance: ${self.balance:.2f}")

    def advance_date(self):
        self.current_date = (datetime.datetime.strptime(self.current_date, '%Y-%m-%d') + datetime.timedelta(days=1)).strftime('%Y-%m-%d')