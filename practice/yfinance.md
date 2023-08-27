


The `yfinance` library in Python allows you to fetch historical data over various periods using the `period` parameter. Here are some of the options:

- `"1d"`: One day
- `"5d"`: Five days
- `"1mo"`: One month
- `"3mo"`: Three months
- `"6mo"`: Six months
- `"1y"`: One year
- `"2y"`: Two years
- `"5y"`: Five years
- `"10y"`: Ten years
- `"ytd"`: Year-to-date
- `"max"`: All available data

Here's a quick example to demonstrate how to fetch data for Apple's stock (AAPL) for a 1-year period:

```python
import yfinance as yf

data = yf.download("AAPL", period="1y")
print(data)
```

You can specify the `period` argument when you are not setting the `start` and `end` date explicitly. The `period` parameter gives you a quick and easy way to set the timeframe for the data you want to retrieve.




The `yfinance` library allows you to specify various intervals for historical data retrieval. Here are the options for the `interval` parameter:

- `"1m"`: One minute
- `"2m"`: Two minutes
- `"5m"`: Five minutes
- `"15m"`: Fifteen minutes
- `"30m"`: Thirty minutes
- `"60m"`: Sixty minutes (or one hour)
- `"90m"`: Ninety minutes
- `"1h"`: One hour
- `"1d"`: One day
- `"5d"`: Five days
- `"1wk"`: One week
- `"1mo"`: One month
- `"3mo"`: Three months

Here's a quick example to show how to fetch historical data for Apple's stock (AAPL) with a 15-minute interval:

```python
import yfinance as yf

data = yf.download("AAPL", start="2022-01-01", end="2022-02-01", interval="15m")
print(data)
```

Keep in mind that the available intervals may be constrained by the `start` and `end` dates you choose, as well as by the data Yahoo Finance provides. Some intervals may only be available for more recent timeframes.