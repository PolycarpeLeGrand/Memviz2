from dash import html, Input, Output, callback
import dash_bootstrap_components as dbc

# If using DataManagers, import them from dashapp on this line as well
# from dashapp import app, cache  # , DM

from dashapp.extras.extras_test import extras_test_maindiv
from dashapp.extras.extras_tags import extras_tags_lemmas_maindiv, extras_tags_words_maindiv
from dashapp.extras.extras_meta import extras_meta_maindiv
from dashapp.extras.extras_prob import lex_probs_maindiv

page_name = 'extras-page'


extras_card = dbc.Card([
    dbc.CardHeader([
        html.H3('Données supplémentaires'),
        dbc.Tabs([
                dbc.Tab(label='Metadonnées', tab_id='extras-meta-tab'),
                dbc.Tab(label='Test', tab_id='extras-test-tab'),
                dbc.Tab(label='Lemmes', tab_id='extras-lemmas-tab'),
                dbc.Tab(label='Mots', tab_id='extras-words-tab'),
                dbc.Tab(label='Probs', tab_id='extras-probs-tab'),
            ],
            id='extras-tabs',
            active_tab='extras-meta-tab',
            className='card-tabs'
        ),
    ], className='content-card-head'),

    dbc.CardBody([
        html.Div(id='extras-tab-content')
    ])

], className='content-card')


extras_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            extras_card,
        ], lg=12),
    ], justify='center'),
], id='extras-page-layout', className='std-content-div', fluid=True)


@callback(
    Output('extras-tab-content', 'children'),
    [Input('extras-tabs', 'active_tab'), ]
)
def update_doc_card_content(active_tab):
    r = 'Not found!'
    if active_tab == 'extras-test-tab':
        r = extras_test_maindiv
        # r = DM.README_MD
    elif active_tab == 'extras-lemmas-tab':
        r = extras_tags_lemmas_maindiv
    elif active_tab == 'extras-words-tab':
        r = extras_tags_words_maindiv
    elif active_tab == 'extras-meta-tab':
        r = extras_meta_maindiv
    elif active_tab == 'extras-probs-tab':
        r = lex_probs_maindiv
    return r
