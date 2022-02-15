from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

# If using DataManagers, import them from dashapp on this line as well
# from dashapp import app, cache  # , DM

page_name = 'theory-page'


theory_card = dbc.Card([
    dbc.CardHeader([
        html.H3('Chapitre 1: Contexte théorique'),
        html.P('Présentation'),
        dbc.Tabs([
                dbc.Tab(label='L\'explication scientifique', tab_id='tab-0'),
                dbc.Tab(label='Les humanités numériques', tab_id='tab-1'),
            ],
            id='theory-tabs',
            active_tab='tab-0',
            className='card-tabs'
        ),
    ], className='content-card-head'),

    dbc.CardBody([
        html.Div(id='theory-tab-content')
    ])

], className='content-card')


theory_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            theory_card,
        ], lg=10),
    ], justify='center'),
], id='theory-page-layout', className='std-content-div', fluid=True)


@callback(
    Output('theory-tab-content', 'children'),
    [Input('theory-tabs', 'active_tab'), ]
)
def update_doc_card_content(active_tab):
    r = 'Not found!'
    if active_tab == 'tab-0':
        r = 'tab-0'
        # r = DM.README_MD
    elif active_tab == 'tab-1':
        r = 'tab-1'
        # r = DM.DOC_MD
    return r
