#------------------------------------------------------------------------------
#   - Dash Stock App -
#   - By: Klassh -
#   - 2021.08.08 -
#------------------------------------------------------------------------------
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from pandas_datareader import data as web
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime

stock = "GOOGL"
df = web.DataReader(stock, data_source='yahoo', start='01-01-2019')
#------------------------------------------------------------------------------
#   - Different Traces to add to charts -
#------------------------------------------------------------------------------

# Main candle stick chart
Trace1 = {
    'x': df.index,
    'open': df.Open,
    'close': df.Close,
    'high': df.High,
    'low': df.Low,
    'type': 'candlestick',
    'name': stock,
    'showlegend':True,
    'line_width': 1,
    'opacity': 1
}

# Moving average for 10 days line
avg_10 = df.Close.rolling(window=10, min_periods=1).mean()
Trace2 = {
    'x': df.index,
    'y': avg_10,
    'type': 'scatter',
    'mode': 'lines',
    'line': {
        'width': 1,
        'color': 'purple',
            },
    'name': '10 Day'
}

# Moving average for 50 days line
avg_50 = df.Close.rolling(window=50, min_periods=1).mean()
Trace3 = {
    'x': df.index,
    'y': avg_50,
    'type': 'scatter',
    'mode': 'lines',
    'line': {
        'width': 1,
        'color': 'Yellow',
            },
    'name': '50 Day'
}
# Moving average for 100 days line
avg_100 = df.Close.rolling(window=100, min_periods=1).mean()
Trace4 = {
    'x': df.index,
    'y': avg_100,
    'type': 'scatter',
    'mode': 'lines',
    'line': {
        'width': 1,
        'color': 'turquoise',
            },
    'name': '100 Day'
}

# Moving average for 200 days line
avg_200 = df.Close.rolling(window=200, min_periods=1).mean()
Trace5 = {
    'x': df.index,
    'y': avg_200,
    'type': 'scatter',
    'mode': 'lines',
    'line': {
        'width': 1,
        'color': 'white',
            },
    'name': '200 Day'
}
# Volume Bar Graph
Trace6 = {
    'x': df.index,
    'y': df.Volume,
    'type': 'bar',
    'name': 'Trading Volume'
}


#------------------------------------------------------------------------------
#   - Dash App -
#------------------------------------------------------------------------------
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Checklist(
        id='toggle-rangeslider',
        options=[{'label': 'Include Rangeslider', 
                  'value': 'slider'}],
        value=['slider']
    ),
    dcc.Graph(id="graph"),
])

@app.callback(
    Output("graph", "figure"), 
    [Input("toggle-rangeslider", "value")])
def display_stock(value):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
            vertical_spacing=0.03, subplot_titles=(str(stock), 'Volume'),
            row_width=[0.2, 0.7])
    fig.update_layout(
        xaxis_rangeslider_visible='slider' in value,
        template="plotly_dark")
    fig.add_trace(Trace1, row=1, col=1)
    fig.add_trace(Trace2, row=1, col=1)
    fig.add_trace(Trace3, row=1, col=1)
    fig.add_trace(Trace4, row=2, col=1)
    fig.add_trace(Trace5, row=2, col=1)
    fig.add_trace(Trace6, row=2, col=1)
    return fig









#------------------------------------------------------------------------------
#   - Initiate -
#------------------------------------------------------------------------------
app.run_server(debug=True)