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
# from ta.momentum import StochasticOscillator
# import pandas_ta as ta

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
    #   INPUT: str - a stock ticker
    #   OUTPUT: fig - a series of charts from stock price

    stock = value
    df = web.DataReader(str(stock), data_source='yahoo', start='01-01-2020')
    
    # Adding Stochastic Indicators
#    df.ta.stoch(high='high', low='low', k=14, d=3, append=True)
    k_period = 19
    d_period = 4

    df['n_high'] = df['High'].rolling(k_period).max() 
    df['n_low'] = df['Low'].rolling(k_period).min() 
    df['%K'] = (df['Close'] - df['n_low']) * 100 / (df['n_high'] - df['n_low'])
    df['%D'] = df['%K'].rolling(d_period).mean()
    
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

   # Stochastic
#    stoch = StochasticOscillator(high=df['High'],
#            close=df['Close'],
#            low=df['Low'],
#            window=14,
#            smooth_window=3)

    
    # Make 3 charts
    fig = make_subplots(rows=3, cols=1, 
            shared_xaxes=True,
            vertical_spacing=0, 
            subplot_titles=(value,),
            row_width=[0.2, 0.1, 0.7]
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
#    fig.add_trace(go.Scatter(x=df.index,
#        y=stoch.stoch_signal(),
#        line=dict(color='red', width=1)
#        ), row=3, col=1)
    fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['%K'],
                line=dict(color='red', width=1),
                name='%K'), col=1, row=3)

    fig.add_trace(
           go.Scatter(
               x=df.index,
               y=df['%D'],
               line=dict(color='yellow', width=1),
               name='%D'), col=1, row=3)
            
    fig.add_hline(y=32, col=1, row=3, line_width=1, line_dash='dash')
    fig.add_hline(y=80, col=1, row=3, line_width=1, line_dash='dash')
    fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
    return fig


#------------------------------------------------------------------------------
#   - Initiate -
#------------------------------------------------------------------------------
app.run_server(debug=True)
