from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from textwrap import dedent

from dashapp import DM
from tools.factories import two_columns_content_row as cr

left_width = 6
right_width = 6

preprocess_div = html.Div([
    cr(html.H4('Introduction'), dcc.Markdown(DM.PREPROCESS_INTRO), html.Div()),
    cr(html.H4('Fichiers source'), dcc.Markdown(DM.PREPROCESS_XML), html.Div([dcc.Markdown(DM.PREPROCESS_XML_EX), html.Div('Figure X: Exemple de fichier source XML', className='r2c-legend')])),
], className='text-content')

