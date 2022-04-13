from dash import dcc, html, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from dashapp import DM, cache

df = DM.LEXCORRS_PARAS_FULL_DF
#print(df)

lex_probs_maindiv = html.Div([
    dbc.Row([
        dbc.Col([
            html.H4('Bayesish'),
        ]),
    ]),
])