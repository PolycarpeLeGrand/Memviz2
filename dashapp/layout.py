from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc

from dashapp.examples.example_home import example_home_layout
from dashapp.examples.page_template import template_page_layout
from dashapp.examples.doc_page import doc_page_layout

from config import NAV_TITLE, NAV_SUBTITLE, IS_PROD

# Register pages using the following format:
# {'name': 'page-X', 'url': '/PAGE_URL', 'label': 'NAVBAR_LABEL', 'container': IMPORTED_CONTAINER, 'in_nav': True/False}
# One page (usually the landing page) should have '/' as the url, else the base address will throw a 404
# IMPORTANT: name and url fields must be unique across all values
# if use_nav is set to False, no link will be created in the nav bar but the page is still accessible via url or links
# The page should be held in a dbc.Container component, defined in a distinct file and imported here
PAGES = [
    {'name': 'page-0', 'url': '/', 'label': 'Home', 'container': example_home_layout, 'in_nav': True},
    {'name': 'page-1', 'url': '/ex', 'label': 'Example Page', 'container': template_page_layout, 'in_nav': True},
]

# Append pages that should only be available in dev config
if not IS_PROD:
    PAGES.append(
        {'name': 'page-100', 'url': '/doc', 'label': 'Project Doc', 'container': doc_page_layout, 'in_nav': True}
    )



# Collapsable navbar component
# A link will be created for each page specified above
# Will consist of two rows on desktop, the first with title and subtitle and the second with the link
# On mobile, consists of only one row with the title on the left and a burger menu to toggle the links on the right
# Colors for each row (or row and collapse), as well as other style props, can be set in 02_navbar.css
# To have it fit on a single row, place the Collapse element in the first div and remove the second div
navbar = html.Div([

    html.Div([
        html.P(
            NAV_TITLE,
            style={'text-align': 'center'},
            id='navbar-title'
        ),

        # Subtitle, hidden on mobile
        html.P(
            NAV_SUBTITLE,
            style={'text-align': 'center'},
            id='navbar-subtitle'
        ),

        # Burger menu
        html.Span([
            html.Button(
                html.Span(className='navbar-toggler-icon'),
                className="navbar-toggler",
                id='navbar-toggle',
            ),
        ], id='navbar-toggle-span'),

    ], id='navbar-head'),

    html.Div([
        dbc.Collapse(
            dbc.Nav(
                [dbc.NavLink(link['label'], href=link['url'], active='exact', className='navbar-link')
                 for link in PAGES if link['in_nav']],
                pills=False,
            ),
            id="navbar-collapse",
        ),
    ], id='navbar-tail')
], id='navbar')


layout = html.Div([
    dcc.Location(id='url'),
    navbar,
    html.Div(id='page-content')
])


@callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def render_page_content(pathname):
    """Updates page content on url change or navbar click, returns a 404 if url not found in PAGES"""

    try:
        return next(filter(lambda x: x['url'] == pathname, PAGES))['container']
    except StopIteration:
        return dbc.Container(
            [
                html.H1("404: Not found", className='text-danger display-3'),
                html.Hr(className='my-2'),
                html.P(f''),
            ],
            className='p-3 rounded-3'
        )


@callback(
    Output('navbar-collapse', 'is_open'),
    [Input('navbar-toggle', 'n_clicks'),
     Input('url', 'pathname')],
    [State('navbar-collapse', 'is_open')],
)
def toggle_collapse(n, url, is_open):
    """Toggle collapsable burger menu for navitems on small screens. Set collapse threshold in css"""

    if n:
        return not is_open
    return is_open
