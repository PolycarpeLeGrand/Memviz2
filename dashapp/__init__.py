import dash
from flask_caching import Cache
import plotly.io as pio
import plotly.graph_objects as go

from config import PROJECT_TITLE, IS_PROD, USE_CACHE, CACHE_CONFIG, DATA
from data.datamanager import DataManager


app = dash.Dash(
    __name__,
    title=PROJECT_TITLE,
    suppress_callback_exceptions=IS_PROD,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
)


if USE_CACHE:
    cache = Cache(
        app.server,
        config=CACHE_CONFIG
    )

# Inits de DfManager object as specified in config
# Dataframes can be accessed in modules by importing DM (e.g. import DM; DM.TEST_DF)
DM = DataManager(
    sd_list=DATA
)


# Plotly template
# TODO move editable part to config or other to avoid having to meddle with init
pio.templates['custom_template'] = go.layout.Template(
    layout={
        # Background color outside graph area, should match container background as set in CSS
        'paper_bgcolor': '#fcfcfc',
        # Graph area background
        # 'plot_bgcolor': '#98AFBA',
        # Discrete colors for 'color' axis
        'colorway': ['#188caf', '#AF4979', '#F39530', '#A171A0', '#00836B', '#FFEACE', '#5ED99C'], ##FFEACE
        # Font property is a dict, family, size, color, etc.
        'font': {'family': 'Sans-serif, Helvetica', 'color': '#212529'}
    }
)

pio.templates.default = 'plotly+custom_template'



