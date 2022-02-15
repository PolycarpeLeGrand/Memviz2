from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

# Uncomment the next import if app or cache are needed
# If using DataManagers, import them from dashapp on this line as well
# from dashapp import app, cache  # , DM

page_name = 'example-home'


home_title_card = dbc.Card([
    dbc.Row([
        dbc.Col([
            html.H2('Explication, mécanismes et modèles'),
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            html.P('Résumé', className='content-text'),
        ]),
        dbc.Col([
            html.P('À propos')
        ]),
    ]),
], className='content-card', body=True)

home_intro_card = dbc.Card([
    dbc.CardHeader([
        html.H3('Introduction'),
        dbc.Tabs([
                dbc.Tab(label='Mise en contexte', tab_id='tab-0'),
                dbc.Tab(label='Problématique', tab_id='tab-1'),
                dbc.Tab(label='Présentation des sections', tab_id='tab-2'),
                dbc.Tab(label='Plan détaillé', tab_id='tab-3'),
            ],
            id='home-tabs',
            active_tab='tab-0',
            className='card-tabs'
        ),
    ], className='content-card-head'),

    dbc.CardBody([
        html.Div(id='home-tab-content', className='content-text'),
    ])
], className='content-card')


home_layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            home_title_card
        ], lg=10),
    ], justify='center'),
    dbc.Row([
        dbc.Col([
            home_intro_card,
        ], lg=10),
    ], justify='center'),
], id='example-home-layout', className='std-content-div', fluid=True)


@callback(
    Output('home-tab-content', 'children'),
    [Input('home-tabs', 'active_tab'), ]
)
def update_doc_card_content(active_tab):
    r = 'Not found!'
    if active_tab == 'tab-0':
        r = 'tab-0'
        # r = DM.README_MD
    elif active_tab == 'tab-1':
        r = 'tab-1'
        # r = DM.DOC_MD
    elif active_tab == 'tab-2':
        r = 'tab-2'
    elif active_tab == 'tab-3':
        r = 'tab-3'
    return r
