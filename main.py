import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class MeanReversionStrategy:
    def __init__(self, data, initial_balance=1000, entry_threshold=0.04, stoploss_threshold=0.02, take_profit_threshold=0.03, mean_period_in_hour=4, timeframe_in_minute=5):
        self.data = data
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.position = 0 # represents the amount of the asset (e.g. Ethereum) held at a given moment
        self.entry_price = 0
        self.stoploss = 0
        self.take_profit = 0
        self.trade_history = []
        self.entry_threshold = entry_threshold
        self.stoploss_threshold = stoploss_threshold
        self.take_profit_threshold = take_profit_threshold
        self.mean_period_in_hour = mean_period_in_hour
        self.timeframe_in_minute = timeframe_in_minute

    def calculate_mean(self):
        periods = int((self.mean_period_in_hour * 60) / self.timeframe_in_minute)  # Convert hours to the number of periods based on the timeframe

        '''
          Do you wanna periods+1? it doesn't change the result, but start 03:55:00 
        '''
        self.data['mean'] = self.data['close'].rolling(window=periods).mean()

    def execute_trades(self):
        for index, row in self.data.iterrows():
            current_price = row['close']
            mean_price = row['mean']

            # Check if there's an open position
            if self.position == 0:
                # Calculate the entry threshold based on the mean price
                entry_threshold_price = mean_price * (1 - self.entry_threshold)

                # Check if the current price is below the entry threshold price
                if current_price <= entry_threshold_price:
                    # Open a long position
                    self.position = self.balance / current_price
                    self.entry_price = current_price
                    self.stoploss = current_price * (1 - self.stoploss_threshold)
                    self.take_profit = current_price * (1 + self.take_profit_threshold)

                    '''
                      Feel like balance should be 0 if you mean the €account balance 
                      Share holding can be there, current self.position
                    '''
                    # Record the buy trade
                    self.trade_history.append({
                        'timestamp': index,
                        'action': 'buy',
                        'price': current_price,
                        'balance': self.balance,
                    })

            # Check if there's an open position to manage
            elif self.position > 0:
                # Check if the current price has reached the stoploss or take_profit levels
                if current_price <= self.stoploss or current_price >= self.take_profit:
                    # Close the position
                    self.balance = self.position * current_price
                    self.position = 0

                    # Record the sell trade
                    self.trade_history.append({
                        'timestamp': index,
                        'action': 'sell',
                        'price': current_price,
                        'balance': self.balance,
                    })


    def analyze_performance(self):
        final_balance = self.balance
        profit = final_balance - self.initial_balance
        percentage_profit = (profit / self.initial_balance) * 100

        return final_balance, profit, percentage_profit

    def plot_performance(self):
        fig, (ax1, ax2) = plt.subplots(2, figsize=(24, 8))
        ax1.plot(self.data.index, self.data['close'], label='Close Price')
        ax1.plot(self.data.index, self.data['mean'], label=f'{self.mean_period_in_hour}-Hour Mean')

        buy_legend_added = False
        sell_legend_added = False

        for trade in self.trade_history:
            if trade['action'] == 'buy':
                label = 'Buy' if not buy_legend_added else None
                ax1.scatter(trade['timestamp'], trade['price'], marker='^', color='g', label=label)
                buy_legend_added = True
            elif trade['action'] == 'sell':
                label = 'Sell' if not sell_legend_added else None
                ax1.scatter(trade['timestamp'], trade['price'], marker='v', color='r', label=label)
                sell_legend_added = True

        ax1.set_title('Close Price & Mean Reversion Trading Signals')
        ax1.legend()

        equity_df = self.build_equity_dataframe()
        ax2.plot(equity_df['timestamp'], equity_df['equity'])
        ax2.set_title('Equity Curve')
        plt.show()


    def build_equity_dataframe(self):
        # Create an initial DataFrame with only the timestamp column from the original data
        equity_df = pd.DataFrame(self.data.index, columns=['timestamp'])

        # Iterate through the trade history and set the equity (balance) at each trade timestamp
        for trade in self.trade_history:
            timestamp = trade['timestamp']
            equity_df.loc[equity_df['timestamp'] == timestamp, 'equity'] = trade['balance']

        # Forward-fill the missing equity values (NaN) with the previous equity value
        equity_df['equity'].fillna(method='ffill', inplace=True)

        # Fill any remaining missing values (at the beginning) with the initial balance
        equity_df['equity'].fillna(self.initial_balance, inplace=True)

        return equity_df

def load_data(file_path):
    data = pd.read_csv(file_path, index_col='timestamp', parse_dates=True)
    data.index = pd.to_datetime(data.index, unit='ms')
    return data

def main():
    file_path = 'ohlc.csv'
    data = load_data(file_path)
    strategy = MeanReversionStrategy(data)
    strategy.calculate_mean()
    strategy.execute_trades()
    final_balance, profit, percentage_profit = strategy.analyze_performance()

    print(f"Initial balance: ${strategy.initial_balance:.2f}")
    print(f"Final balance: ${final_balance:.2f}")
    print(f"Profit: ${profit:.2f}")
    print(f"Percentage profit: {percentage_profit:.2f}%")

    strategy.plot_performance()

if __name__ == '__main__':
    main()