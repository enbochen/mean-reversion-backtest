import pandas as pd
import plotly.graph_objs as go


class MeanReversionStrategy:
    def __init__(self, data, initial_balance=1000, entry_threshold=0.04, stoploss_threshold=0.02, take_profit_threshold=0.03, mean_period_in_hour=4, timeframe_in_minute=5):
        """
        Initialize the Mean Reversion Strategy class with given parameters.

        :param data: DataFrame containing the historical price data.
        :param initial_balance: The initial balance of the trading account.
        :param entry_threshold: The entry threshold percentage below the mean price for trade execution.
        :param stoploss_threshold: The stoploss threshold percentage below the entry price.
        :param take_profit_threshold: The take profit threshold percentage above the entry price.
        :param mean_period_in_hour: The period for calculating the mean price, in hours.
        :param timeframe_in_minute: The timeframe of the historical data, in minutes.
        """
        self.data = data
        self.initial_balance = initial_balance
        self.balance = initial_balance
        # represents the amount of the asset (e.g. Ethereum) held at a given moment
        self.position = 0
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
        """
        Calculate the rolling mean price for the historical data.
        """
        periods = int((self.mean_period_in_hour * 60) /
                      self.timeframe_in_minute) + 1  # The +1 is to ensure that the first calculated mean value is not NaN due to the lack of data points.
        self.data['mean'] = self.data['close'].rolling(
            window=periods, min_periods=1).mean()

    def execute_trades(self):
        """
        Execute the mean reversion trading strategy on the historical data.
        """
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
                    self.stoploss = current_price * \
                        (1 - self.stoploss_threshold)
                    self.take_profit = current_price * \
                        (1 + self.take_profit_threshold)

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
        """
        Analyze the performance of the Mean Reversion trading strategy based on the trade history.
        """
        final_balance = self.balance
        profit = final_balance - self.initial_balance
        percentage_profit = (profit / self.initial_balance) * 100

        return final_balance, profit, percentage_profit

    def plot_performance(self):
        """
        Plot the performance of the Mean Reversion trading strategy, including the Close Price and Mean Reversion Trading Signals and Equity Curve.
        """
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.data.index,
                      y=self.data['close'], name='Close Price'))
        fig.add_trace(go.Scatter(
            x=self.data.index, y=self.data['mean'], name=f'{self.mean_period_in_hour}-Hour Mean'))

        trades_df = pd.DataFrame(self.trade_history)

        buys = trades_df[trades_df['action'] == 'buy']
        sells = trades_df[trades_df['action'] == 'sell']

        fig.add_trace(go.Scatter(x=buys['timestamp'], y=buys['price'], mode='markers', marker=dict(
            symbol='triangle-up', color='green'), name='Buy'))
        fig.add_trace(go.Scatter(x=sells['timestamp'], y=sells['price'], mode='markers', marker=dict(
            symbol='triangle-down', color='red'), name='Sell'))

        fig.update_layout(title='Close Price & Mean Reversion Trading Signals',
                          xaxis_title='Date', yaxis_title='Price')

        equity_df = self.build_equity_dataframe()

        fig.add_trace(go.Scatter(
            x=equity_df['timestamp'], y=equity_df['equity'], name='Equity Curve'))

        fig.update_layout(title='Equity Curve',
                          xaxis_title='Date', yaxis_title='Balance')

        fig.show()

    def build_equity_dataframe(self):
        """
        Build a DataFrame of the equity curve based on the trade history.
        """
        # Create an initial DataFrame with only the timestamp column from the original data
        equity_df = pd.DataFrame(self.data.index, columns=['timestamp'])

        # Iterate through the trade history and set the equity (balance) at each trade timestamp        '''
        for trade in self.trade_history:
            timestamp = trade['timestamp']
            equity_df.loc[equity_df['timestamp'] ==
                          timestamp, 'equity'] = trade['balance']

        # Forward-fill the missing equity values (NaN) with the previous equity value
        equity_df['equity'].fillna(method='ffill', inplace=True)

        # Fill any remaining missing values (at the beginning) with the initial balance
        equity_df['equity'].fillna(self.initial_balance, inplace=True)

        return equity_df
