from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

# Import app and cache only if needed
# If using DataManagers, import them from dashapp on this line as well
# from dashapp import app, cache
from dashapp import DM

page_name = 'doc_page'

# Example jumbotron
# The text layout can easily be set with dbc rows and cols
doc_title_card = dbc.Card([
    dbc.Row([
        dbc.Col([
            html.H2('Project documentation, tutorial and examples', className='jumbotron-title')
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            html.P('Project description', className='content-text'),
        ], lg=4),
        dbc.Col([
            html.P('Author info etc.', className='content-text')
        ], lg=4),
    ])
], body=True, className='content-card')

doc_card = dbc.Card([
    dbc.CardHeader([
        html.H3('Project Documentation'),
        dbc.Tabs([
            dbc.Tab(label='Readme', tab_id='tab-readme'),
            dbc.Tab(label='Data Doc', tab_id='tab-df'),
        ],
            id='doc-page-doc-card-tabs',
            active_tab='tab-readme',
            className='card-tabs',
        ),
    ], className='content-card-head'),
    dbc.CardBody([
        dcc.Markdown('readme', className='content-text doc-md', id='doc-page-doc-card-markdown')
    ])
],  className='content-card')

# Page layout holding the different components
# Name should be changed to <page_name>_layout and id to <page-name> (should be done automatically if using template)
#
# Useful notes:
#   Use <width> param to specify col width. True will expand, 'auto' fit to content, and 1-12 span a fixed number of
#       grid columns.
#   Alternatively (recommended), use <lg> to specify width on large screens and leave auto on mobile / small.
#   Use <no_gutters=True> to remove spacing between columns
#   Use <align> to set vertical alignment of cols within a row. Can be used on Col to set for all children or on Row to
#       override the Col setting. Values: 'start', 'center', 'end'
#   Use <justify> to set the horizontal alignment within a row. Values: 'start', 'center', 'end', 'between', 'around'
doc_page_layout = dbc.Container([
    # Jumbotron Row, delete if not needed
    dbc.Row([
       dbc.Col([
           doc_title_card
       ], lg=8),
    ], justify='center'),

    # First card row, two columns
    dbc.Row([
        dbc.Col(doc_card, lg=8),
    ], justify='center'),
], id='doc-page-layout', className='std-content-div', fluid=True)


@callback(
    Output('doc-page-doc-card-markdown', 'children'),
    [Input('doc-page-doc-card-tabs', 'active_tab'), ]
)
def update_doc_card_content(active_tab):
    r = 'Not found!'
    if active_tab == 'tab-readme':
        r = DM.README_MD
    elif active_tab == 'tab-df':
        r = DM.DOC_MD
    return r


