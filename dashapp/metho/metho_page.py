from dash import html, Input, Output, callback
import dash_bootstrap_components as dbc

from dashapp.metho.corpus.corpus import wordcounts_div
from dashapp.metho.preprocess.preprocess import preprocess_div
# If using DataManagers, import them from dashapp on this line as well
# from dashapp import app, cache  # , DM

page_name = 'metho-page'


metho_card = dbc.Card([
    dbc.CardHeader([
        dbc.Row([
            dbc.Col([
                html.H2('Chapitre 2: Corpus et méthodologie'),
            ]),
        ], className='title-row'),
        dbc.Row([
            dbc.Col([
                html.P('Résumé du chapitre'),
            ], lg=6),
        ]),

        dbc.Tabs([
                dbc.Tab(label='Extraction et prétraitement', tab_id='tab-0'),
                dbc.Tab(label='Présentation du corpus', tab_id='tab-1'),
                dbc.Tab(label='Algorithmes d\'analyse', tab_id='tab-2'),
                # dbc.Tab(label='Annexes', tab_id='tab-3'),
                # dbc.Tab(label='Code et librairies', tab_id='tab-4'),
            ],
            id='metho-tabs',
            active_tab='tab-0',
            className='card-tabs'
        ),
    ], className='content-card-head'),

    dbc.CardBody([
        html.Div(id='metho-tab-content')
    ])

], className='content-card')


metho_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            metho_card,
        ], lg=12),
    ], justify='center'),
], id='metho-page-layout', className='std-content-div', fluid=True)


@callback(
    Output('metho-tab-content', 'children'),
    [Input('metho-tabs', 'active_tab'), ]
)
def update_doc_card_content(active_tab):
    r = 'Not found!'
    if active_tab == 'tab-0':
        r = preprocess_div
        # r = DM.README_MD
    elif active_tab == 'tab-1':
        r = wordcounts_div
        # r = DM.DOC_MD
    elif active_tab == 'tab-2':
        r = 'tab-2'
    return r
