from mean_reversion import MeanReversionStrategy
from data_loader import load_data, analyze_data, clean_data
from result_analysis import analyze_performance, plot_performance


def main():
    # prepare, analyze and clean the data
    file_path = 'data/ohlc.csv'
    data = load_data(file_path)
    analyze_data(data)
    cleaned_data = clean_data(data)

    # use the mean reversion strategy to execute trades
    strategy = MeanReversionStrategy(cleaned_data)
    strategy.calculate_mean()
    trade_history, final_balance = strategy.execute_trades()

    # analyze the performance of the strategy
    analyze_performance(final_balance)
    plot_performance(cleaned_data, trade_history)


if __name__ == '__main__':
    main()
