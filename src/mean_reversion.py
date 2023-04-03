
class MeanReversionStrategy:
    def __init__(self, initial_balance=1000, entry_threshold=0.04, stoploss_threshold=0.02, take_profit_threshold=0.03, mean_period_in_hour=4, timeframe_in_minute=5):
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
        self.initial_balance = initial_balance
        self.balance = initial_balance
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

    def calculate_mean(self, data):
        """
        Calculate the rolling mean price for the historical data.
        """
        periods = int((self.mean_period_in_hour * 60) /
                      self.timeframe_in_minute) + 1  # The +1 is to ensure that the first calculated mean value is not NaN due to the lack of data points.
        mean = data['close'].rolling(
            window=periods, min_periods=1).mean()
        return data.assign(mean=mean)

    def execute_trades(self, data):
        """
        Execute the mean reversion trading strategy on the historical data.
        """
        for index, row in data.iterrows():
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
        return self.trade_history, self.balance
