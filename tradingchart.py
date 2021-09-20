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

external_stylesheets = ["/assets/style.css"]
#------------------------------------------------------------------------------
#   - Dash App -
#------------------------------------------------------------------------------
app = dash.Dash(__name__)

app.layout = html.Div(
    [
    dcc.Input(
        id='stockInput',
        type="text",
        value="SPY",
        placeholder="",
        debounce=True,
        ),

    dcc.Graph(id="graph")
    ],
)


@app.callback(
    Output("graph", "figure"), 
    [Input("stockInput", "value")])

def display_stock(value):
    stock = value
    df = web.DataReader(str(stock), data_source='yahoo', start='01-01-2019')
    
    # Create the Charts and moving averages
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
    avg_25 = df.Close.rolling(window=25, min_periods=1).mean()
    Trace2 = {
        'x': df.index,
        'y': avg_25,
        'type': 'scatter',
        'mode': 'lines',
        'line': {
            'width': 1,
            'color': 'purple',
                },
        'name': '25 Day'
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
    # Make 2 charts
    fig = make_subplots(rows=2, cols=1, 
            shared_xaxes=True,
            vertical_spacing=0, 
            subplot_titles=(value,),
            row_width=[0.2, 0.7]
            )
    # Add layout options
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        height=850
        )
    # Add Traces to the figre
    fig.add_trace(Trace1)
    fig.add_trace(Trace2)
    fig.add_trace(Trace3)
    fig.add_trace(Trace4)
    fig.add_trace(Trace5)
    fig.add_trace(Trace6, 2,1) #row2, col1
    return fig


#------------------------------------------------------------------------------
#   - Initiate -
#------------------------------------------------------------------------------
app.run_server(debug=True)
