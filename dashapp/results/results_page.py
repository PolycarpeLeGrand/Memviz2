from dash import html, Input, Output, callback
import dash_bootstrap_components as dbc

# If using DataManagers, import them from dashapp on this line as well
# from dashapp import app, cache  # , DM

from dashapp.results.topics_scatter import topics_scatter_maindiv
from dashapp.results.topic_details import topic_details_maindiv
from dashapp.results.cluster_details import cluster_details_maindiv
from dashapp.results.lex_corrs import lex_corrs_maindiv
from dashapp.results.coocs import coocs_maindiv
from dashapp.results.cooc_refs import cooc_refs_maindiv

page_name = 'results-page'


results_card = dbc.Card([
    dbc.CardHeader([
        html.H3('Chapitre 3: Résultats'),
        html.P('Présentation'),
        dbc.Tabs([
                dbc.Tab(label='Topics et clusters', tab_id='topics-scatter-tab'),
                dbc.Tab(label='Détails des topics', tab_id='topic-details-tab'),
                dbc.Tab(label='Détails des clusters', tab_id='cluster-details-tab'),
                dbc.Tab(label='Lexique et corrélations', tab_id='lexcorrs-tab'),  # fréquences?
                dbc.Tab(label='Cooccurrences', tab_id='coocs-top'),
                dbc.Tab(label='Exemples de cooccurrences', tab_id='cooc-refs'),
            ],
            id='results-tabs',
            active_tab='topics-scatter-tab',
            className='card-tabs'
        ),
    ], className='content-card-head'),

    dbc.CardBody([
        html.Div(id='results-tab-content')
    ])

], className='content-card')


results_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            results_card,
        ], lg=12),
    ], justify='center'),
], id='results-page-layout', className='std-content-div', fluid=True)


@callback(
    Output('results-tab-content', 'children'),
    [Input('results-tabs', 'active_tab'), ]
)
def update_doc_card_content(active_tab):
    r = 'Not found!'
    if active_tab == 'topics-scatter-tab':
        r = topics_scatter_maindiv
    elif active_tab == 'topic-details-tab':
        r = topic_details_maindiv
    elif active_tab == 'cluster-details-tab':
        r = cluster_details_maindiv
    elif active_tab == 'lexcorrs-tab':
        r = lex_corrs_maindiv
    elif active_tab == 'coocs-top':
        r = coocs_maindiv
    elif active_tab == 'cooc-refs':
        r = cooc_refs_maindiv
    return r
