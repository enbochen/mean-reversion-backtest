# Mean Reversion Trading Backtest

This project is an implementation of [mean reversion coding task](https://gist.github.com/ekreutz/7f4cd0706e456c53a98d8fd24ba160de/)

This mean reversion trading strategy backtest analyzes historical price data and executes trades based on deviations from the moving average. It also includes data visualization of the performance.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/mean-reversion-trading-strategy.git
   cd mean-reversion-trading-strategy
   ```

1. Create a virtual environment (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

1. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

1. run the backtest script:

   ```bash
   python src/main.py
   ```

1. run the tests:

   ```bash
   python tests/test_mean_reversion.py
   ```

## Result

![data analysis](docs/data_analysis.png)

The market in the question should be ETH based on the price history and volumn.

Performance:

```txt
Initial balance: $1000.00
Final balance: $979.35
Profit: $-20.65
Percentage profit: -2.06%
```

![equity curve](docs/equity_curve.png)

## Consideration for future improvements

- The close price is the used for calculating the mean for simpilicity even though the average of open, high, low, close data might provide a broader view of the volatile markets, where prices can fluctuate rapidly and unpredictably

- Trading fees/ gas fees is not considered in this impelementation but in reality it plays an important role especially in cryptocurrency.

- Performance is not the focus of this task, but it should be some kind of more efficient way than iteration loop(e.g vectorized calculation?)
