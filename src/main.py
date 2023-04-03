from mean_reversion import MeanReversionStrategy, load_and_clean_data


def display_results(strategy, final_balance, profit, percentage_profit):
    print(f"Initial balance: ${strategy.initial_balance:.2f}")
    print(f"Final balance: ${final_balance:.2f}")
    print(f"Profit: ${profit:.2f}")
    print(f"Percentage profit: {percentage_profit:.2f}%")


def main():
    file_path = 'data/ohlc.csv'
    data = load_and_clean_data(file_path)
    strategy = MeanReversionStrategy(data)
    strategy.calculate_mean()
    strategy.execute_trades()
    final_balance, profit, percentage_profit = strategy.analyze_performance()

    display_results(strategy, final_balance, profit, percentage_profit)
    strategy.plot_performance()


if __name__ == '__main__':
    main()
