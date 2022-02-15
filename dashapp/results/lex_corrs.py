from dash import dcc, html, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from dashapp import DM, cache


def make_lexcorr_heatmap():
    df = DM.LEXCORRS_PARAS_FULL_DF
    fig = px.imshow(df)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_yaxes(showspikes=True, spikemode='toaxis', spikesnap='data', showline=False, spikedash='dot')
    fig.update_xaxes(showspikes=True, spikemode='toaxis', spikesnap='data', showline=False, spikedash='dot')
    return fig


modal_div = html.Div([
    dbc.Button('Voir le détail des champs', id='lexcorrs-details-btn'),
    dbc.Modal([
            dbc.ModalBody(
                dcc.Markdown('\n'.join(
                    f'* **{lex}:** ' + ', '.join(w for w in words) for lex, words in DM.LEXICON_DICT.items() if lex != 'common'
                ))
            ),
        ],
        id='lexcorrs-details-modal',
        centered=True,
        is_open=False,
        scrollable=True,
    )
])

lex_corrs_maindiv = html.Div([
    dbc.Row([
        dbc.Col([
            html.H4('Lexique et corrélations'),
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            html.P('Corrélations paragraphe-paragraphe sur l\'ensemble des textes.'),
            modal_div,
            dcc.Graph(figure=make_lexcorr_heatmap(), style={'height': '90vw', 'width': '100%'}),
        ], width=12),
    ]),
    dbc.Row([
        dbc.Col([]),
    ]),
    dbc.Row([
        dbc.Col([]),
    ]),
])


@callback(Output('lexcorrs-details-modal', 'is_open'),
          [Input('lexcorrs-details-btn', 'n_clicks')],
          [State('lexcorrs-details-modal', 'is_open')],)
def toggle_modal(n, is_open):
    if n:
        return not is_open
    return is_open

