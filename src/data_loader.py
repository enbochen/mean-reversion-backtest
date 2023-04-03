import pandas as pd


def load_data(file_path):
    # Load data
    data = pd.read_csv(file_path, index_col='timestamp', parse_dates=True)
    data.index = pd.to_datetime(data.index, unit='ms')
    return data


def clean_data(data):
    # Print data information
    print(data.info())

    # Remove any duplicate rows
    print(data[data.duplicated()])
    data = data[~data.index.duplicated()]

    # Remove any rows with missing data
    data.dropna(inplace=True)

    # Validate data types and set correct columns
    data = data.astype({
        'open': 'float',
        'high': 'float',
        'low': 'float',
        'close': 'float',
        'vol': 'float'
    })

    return data
