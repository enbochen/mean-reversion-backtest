# Mean Reversion Trading Backtest

This project is an implementation to answer [Mean reversion coding task](https://gist.github.com/ekreutz/7f4cd0706e456c53a98d8fd24ba160de/)

It implements a Mean Reversion Trading Strategy backtest using Python. The backtest analyzes historical price data and executes trades based on deviations from the moving average. It also includes functionality for visualizing the performance of the strategy.

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

1. run the script:

```bash
    python src/main.py
```

### Consideration

1. The market in question should be ETH based on the price history and volumn
1. The close price is the most commonly used price point for calculating the mean in Mean Reversion trading strategy. On the other hand, it could be caculated using average of open, close, high, and low price, which can provide a broader view of the volatile markets(I discovered the difference of those can be up to 8%) such as cryptocurrencies, where prices can fluctuate rapidly and unpredictably. I compared the results, which is so different (profit -2.06% with close price and 71.68% with the average of 4 prices). But for simpilicity, the close price is used in this implementation.
1.
