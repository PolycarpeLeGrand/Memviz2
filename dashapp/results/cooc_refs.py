from dash import dcc, html, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
import json

from dashapp import DM, cache
from config import STATIC_PATH


def make_cooc_refs_select(c_id, value):
    return dbc.Select(
        options=[
            {'label': w, 'value': w} for w in DM.COOC_REFS_WORDS_LIST
        ],
        value=value,
        id=c_id,
        style={'max-width': '15rem'}
    )


cooc_refs_content_div = html.Div([

], id='cooc-refs-content-div')

cooc_refs_maindiv = html.Div([

    dbc.Row([
        dbc.Col([
            html.H4('Exemples de cooccurrences')
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Label('Choisir le premier mot: '),
            make_cooc_refs_select('cooc-refs-select-0', 'mechanism'),

            dbc.Label('Choisir le deuxième mot: '),
            make_cooc_refs_select('cooc-refs-select-1', 'understand'),

            dbc.Label(id='cooc-refs-total-label'),
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            html.Hr(style={'margin': '2rem'}),
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            cooc_refs_content_div
        ]),
    ]),
])


def make_ref_section(d):
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.Span(f'{d["rank"]+1}. {d["citation"]}'),
                html.Br(),
                html.Span(f'Cluster: {d["cluster"]}'),
                html.Br(),
                html.Span('Top topics: ' + ', '.join(DM.TOPIC_NAMES_MAP[t] for t in d['topics']))
            ]),
        ], style={'margin-bottom': '1rem'}),

        dbc.Row([
            dbc.Col([
                html.Span(f'Texte du paragraphe (paragraphe {d["para_num"]}/{d["tot_paras"]})',
                          style={'font-weight': '700'}),
                html.Div(d['para_text'], style={'padding-top': '1rem'})
            ]),
            dbc.Col([
                html.Span('Texte de l\'abstract', style={'font-weight': '700'}),
                html.Div(d['abs_text'], style={'padding-top': '1rem'})
            ]),
        ]),

        dbc.Row([
            dbc.Col([
                html.Hr(style={'margin': '2rem'})
            ]),
        ]),
    ])

@callback(Output('cooc-refs-content-div', 'children'),
          [Input('cooc-refs-select-0', 'value'),
           Input('cooc-refs-select-1', 'value')],)
def update_cooc_refs(w0, w1):

    w0, w1 = sorted([w0, w1])
    path = STATIC_PATH / 'cooc_refs' / f'{w0}_{w1}.json'
    d = json.load(open(path, 'rb'))
    return [make_ref_section(d) for d in d]

