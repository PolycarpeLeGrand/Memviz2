"""
Generic page template

The design consists of an optional jumbotron to show page instructions, explanations or top-level menus. The content
can be placed in one or many cards. Everything should be held in the <page_name>_layout dbc.Container (name should be
changed from default page_layout to avoid conflicts) and the layout handled with dbc.Row and dbc.Col.

app is imported so callbacks can be registered directly from the page file to keep things neat. To add a new page,
simply import <page_name>_layout in dashapp/layout.py and edit PAGES.

Complex pages can be broken down in multiple files following the same general idea. This file should specify the general
page layout (and possibly some simple components) and use imported Divs or Containers to specify Cards or Jumbotron
content. Callbacks specific to the imported content can be registered in their respective file to keep things tidy.

Style for these components is defined in assets/01_style.css
"""
from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc

# Import app and cache only if needed
#from dashapp import app, cache


# Example card with tabs
# Requires a callback to update content on click. Should have active_tab as input and CardBody-children as output.
ex_tab_card = dbc.Card([
    dbc.CardHeader([
        html.H3('This is a title above the card tabs'),
        dbc.Tabs([
                dbc.Tab(label='Tab 1', tab_id='tab-1'),
                dbc.Tab(label='Tab 2', tab_id='tab-2'),
            ],
            id='ex-page-tabs',
            active_tab='tab-1',
            className='card-tabs',
        ),
    ], className='content-card-head'),
    dbc.CardBody([
        html.P('Placeholder card content', id='ex-page-tab-card-content', className='content-text'),
    ]),
], id='ex-page-tab-card', className='content-card')

# Regular card
ex_card = dbc.Card([
    dbc.CardHeader([
        html.H3('Card Title'),
    ], className='content-card-head'),
    dbc.CardBody([
        html.P('Card content', className='content-text'),
    ])
],  className='content-card')

# Page layout holding the different components
# Name should be changed to <page_name>_layout and id to <page-name> (should be done automatically if using template)
#
# Useful notes:
#   Use <width> param to specify col width. True will expand, 'auto' fit to content, and 1-12 span a fixed number of
#       grid columns.
#   Alternatively (recommanded), use <lg> to specify width on large screens and leave auto on mobile / small.
#   Use <no_gutters=True> to remove spacing between columns
#   Use <align> to set vertical alignment of cols within a row. Can be used on Col to set for all children or on Row to
#       override the Col setting. Values: 'start', 'center', 'end'
#   Use <justify> to set the horizontal alignment within a row. Values: 'start', 'center', 'end', 'between', 'around'
template_page_layout = dbc.Container([

    dbc.Row([
        dbc.Col(ex_tab_card, lg=6),
        dbc.Col(ex_card, lg=4),
    ]),
], id='page-id', className='std-content-div', fluid=True)


@callback(
    Output('ex-page-tab-card-content', 'children'),
    [Input('ex-page-tabs', 'active_tab')]
)
def update_tab_content(active_tab):
    r = 'Not found!'
    if active_tab == 'tab-1':
        r = 'tab-1 content'
    elif active_tab == 'tab-2':
        r = 'tab-2 content'
    return r

