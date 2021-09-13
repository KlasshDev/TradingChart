import pandas as pd
from pandas_datareader import data as web
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Pick the stock to track
stock = "GOOGL"

df = web.DataReader(stock, data_source='yahoo', start='01-01-2019')

# Calculate and define moving average of 30 & 50 periods
avg_30 = df.Close.rolling(window=30, min_periods=1).mean()
avg_50 = df.Close.rolling(window=50, min_periods=1).mean()

# Candle stick chart for stock trades
trace1 = {
        'x': df.index,
        'open': df.Open,
        'close': df.Close,
        'high': df.High,
        'low': df.Low,
        'type': 'candlestick',
        'name': stock,
        'showlegend': True
}

# Line for moving average over 30 days
trace2 = {
    'x': df.index,
    'y': avg_30,
    'type': 'scatter',
    'mode': 'lines',
    'line': {
        'width': 1,
        'color': 'blue'
            },
    'name': 'Moving Average of 30 periods'
}

# Line for moving average over 50 days
trace3 = {
    'x': df.index,
    'y': avg_50,
    'type': 'scatter',
    'mode': 'lines',
    'line': {
        'width': 1,
        'color': 'red'
            },
    'name': 'Moving Average of 50 periods'
}

# Bar Graph for volume
trace4 = {
    'x': df.index,
    'y': df.Volume,
    'type': 'bar',
    'name': 'Volume',
}
# Create Figure with secondary y-axis
fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
        vertical_spacing=0.03, subplot_titles=(str(stock), 'Volume'),
        row_width=[0.2, 0.7])
# fig = go.Figure(data=data)
fig.add_trace(trace1, row=1, col=1)
fig.add_trace(trace2, row=1, col=1)
fig.add_trace(trace3, row=1, col=1)
fig.add_trace(trace4, row=2, col=1)
fig.update_layout(template="plotly_dark")
fig.update(layout_xaxis_rangeslider_visible=False)
fig.show()
