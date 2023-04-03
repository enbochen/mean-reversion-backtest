from mean_reversion import MeanReversionStrategy
from data_loader import load_data, analyze_data, clean_data


def main():
    # prepare, analyze and clean the data
    file_path = 'data/ohlc.csv'
    data = load_data(file_path)
    analyze_data(data)
    cleaned_data = clean_data(data)

    # use the mean reversion strategy to execute trades
    strategy = MeanReversionStrategy(cleaned_data)
    strategy.calculate_mean()
    strategy.execute_trades()

    # analyze the performance of the strategy
    strategy.analyze_performance()
    strategy.plot_performance()


if __name__ == '__main__':
    main()
