from dash import dcc, html, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
import json

from dashapp import DM, cache
from config import STATIC_PATH
from . import CLUSTER_MAP

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

cshps_cooc_refs_maindiv = dbc.Card([

    dbc.Row([
        dbc.Col([
            html.Div('Cooccurrence Samples', className='cshps-title')
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            # Explanatory text
            dcc.Markdown(
                'Sample excerpts can be viewed to help with understanding the contexts in which different words cooccur. ' +
                'These excerpts were selected randomly from the set of every instance the two words were found cooccurring across the corpus. ' +
                'For each excerpt, the article\'s metadata, top topics, cluster, and full abstract are also displayed to provide aditional context. ' +
                'To help navigate the data, we suggest using your browser search function (typically ctrl-f) on one of the selected words.' +
                # '' +
                # '\n\n' +
                '',
                className='cshps-md'
            ),
        ], lg=6),
    ]),

    dbc.Row([
        dbc.Col([
            html.Hr(className='cshps-hr-full'),
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Label('Select first term: '),
            make_cooc_refs_select('cooc-refs-select-0', 'mechanism'),
        ], lg=2),
        dbc.Col([
            dbc.Label('Select second term: '),
            make_cooc_refs_select('cooc-refs-select-1', 'understanding'),

            dbc.Label(id='cooc-refs-total-label'),
        ], lg=2),
        dbc.Col([
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
], body=True, className='content-card')


def make_ref_section(d):
    return html.Div([
        dbc.Row([
            dbc.Col([
                dcc.Markdown(f'**Sample {d["rank"]+1}**'),
                dcc.Markdown(
                    f'**Reference: **{d["citation"]}  \n' +
                    f'**Cluster: **{CLUSTER_MAP[d["cluster"]]}  \n' +
                    '**Top topics: **' + ', '.join(DM.TOPIC_NAMES_MAP[t] for t in d['topics']),
                    className='cshps-md'
                ),

                #dcc.Markdown(f'**{d["rank"]+1}.** {d["citation"]}'),
                #html.Br(),
                #dcc.Markdown(f'**Cluster: **{d["cluster"]}'),
                #html.Br(),
                #dcc.Markdown('**Top topics: **' + ', '.join(DM.TOPIC_NAMES_MAP[t] for t in d['topics']))
            ]),
        ], style={'margin-bottom': '1rem'}),

        dbc.Row([
            dbc.Col([
                html.Span(f'Text excerpt (paragraph {d["para_num"]}/{d["tot_paras"]})',
                          style={'font-weight': '700'}),
                html.Div(d['para_text'], style={'padding-top': '1rem'}, className='cshps-md')
            ]),
            dbc.Col([
                html.Span('Article abstract', style={'font-weight': '700'}),
                html.Div(d['abs_text'], style={'padding-top': '1rem'}, className='cshps-md')
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

