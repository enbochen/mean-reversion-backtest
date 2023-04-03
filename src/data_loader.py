import pandas as pd
import plotly.graph_objects as go


def load_data(file_path):
    """
    Load data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        data (pandas.DataFrame): The loaded data as a pandas DataFrame.
    """
    data = pd.read_csv(file_path, index_col='timestamp', parse_dates=True)
    data.index = pd.to_datetime(data.index, unit='ms')
    return data


def analyze_data(data):
    """
    Analyze the given OHLCV data using a candlestick chart.
    """
    print(data.info())

    figure = go.Figure(data=[go.Candlestick(x=data.index,
                                            open=data["open"],
                                            high=data["high"],
                                            low=data["low"],
                                            close=data["close"])])
    figure.update_layout(title="Time Series Analysis (Candlestick Chart)",
                         xaxis_rangeslider_visible=False)
    figure.show()


def clean_data(data):
    """
    Clean data by removing duplicates and rows with missing data, and converting column data types.
    """
    # Check for and warn about duplicate rows
    if data.index.duplicated().any():
        print("WARNING: Duplicate rows detected. Removing duplicates...")
        data = data[~data.index.duplicated()]

    # Validate data types and set correct columns
    data = data.astype({
        'open': 'float',
        'high': 'float',
        'low': 'float',
        'close': 'float',
        'vol': 'float'
    })

    # Validate that float values are greater than 0 and warn about removal
    original_len = len(data)
    data = data[data.apply(lambda x: x > 0)]
    if len(data) != original_len:
        print("WARNING: Rows with non-positive float values detected. Removing...")

    # Remove any rows with missing data and warn about removal
    if data.isnull().values.any():
        print("WARNING: Rows with missing data detected. Removing...")
        data.dropna(inplace=True)

    return data
