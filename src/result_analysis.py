import plotly.graph_objs as go
import pandas as pd


def analyze_performance(final_balance, initial_balance=1000):
    """
    Analyze the performance of the Mean Reversion trading strategy based on the trade history.
    """
    profit = final_balance - initial_balance
    percentage_profit = (profit / initial_balance) * 100

    print(f"Initial balance: ${initial_balance:.2f}")
    print(f"Final balance: ${final_balance:.2f}")
    print(f"Profit: ${profit:.2f}")
    print(f"Percentage profit: {percentage_profit:.2f}%")


def plot_performance(data, trade_history, initial_balance=1000, mean_period_in_hour=4):
    """
    Plot the performance of the Mean Reversion trading strategy, including the Close Price and Mean Reversion Trading Signals and Equity Curve.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index,
                             y=data['close'], name='Close Price'))
    fig.add_trace(go.Scatter(
        x=data.index, y=data['mean'], name=f'{mean_period_in_hour}-Hour Mean'))

    trades_df = pd.DataFrame(trade_history)

    buys = trades_df[trades_df['action'] == 'buy']
    sells = trades_df[trades_df['action'] == 'sell']

    fig.add_trace(go.Scatter(x=buys['timestamp'], y=buys['price'], mode='markers', marker={
        "symbol": "triangle-up", "color": "green"}, name='Buy'))
    fig.add_trace(go.Scatter(x=sells['timestamp'], y=sells['price'], mode='markers', marker={
        "symbol": "triangle-down", "color": "red"}, name='Sell'))

    equity_df = build_equity_dataframe(data, trade_history, initial_balance)

    fig.add_trace(go.Scatter(
        x=equity_df['timestamp'], y=equity_df['equity'], name='Equity Curve'))

    fig.update_layout(title='Trading Signals / Equity Curve',
                      xaxis_title='Date', yaxis_title='Price / Balance')

    fig.show()


def build_equity_dataframe(data, trade_history, initial_balance):
    """
    Build a DataFrame of the equity curve based on the trade history.
    """
    equity_df = pd.DataFrame(data.index, columns=['timestamp'])

    # Iterate through the trade history and set the equity (balance) at each trade timestamp        '''
    for trade in trade_history:
        timestamp = trade['timestamp']
        equity_df.loc[equity_df['timestamp'] ==
                      timestamp, 'equity'] = trade['balance']

    # Forward-fill the missing equity values (NaN) with the previous equity value
    equity_df['equity'].fillna(method='ffill', inplace=True)

    # Fill any remaining missing values (at the beginning) with the initial balance
    equity_df['equity'].fillna(initial_balance, inplace=True)

    return equity_df
