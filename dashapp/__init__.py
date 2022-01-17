import dash
from flask_caching import Cache

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

