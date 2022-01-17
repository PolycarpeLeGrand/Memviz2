Phidash
=======
*A multipage Dash project template*

**Features Overview**

* Multipage layout with a responsive navbar and url routing
* Quickly add new pages from templates
* Easily editable custom styling built on top of dash bootstrap components
* Data management system making it easier to work with multiple dataframes and markdown files without having to setup a database
* Easy integration of redis caching to optimize performance
* Production ready with detailed instructions


**Quickstart:**

1. Clone the project and follow the setup instructions
2. Set IS_PROD to False in .env or config.py
3. Run wsgi.py to launch the test server


**Notes**
  
Built on Dash 2.0 and Python 3.9.7  
Should work on python 3.8  
See `requirements.txt` for a full list of dependencies

---

Setup
-----

1. Setup the python environment
    * Make and activate a venv for the project
    * Install dependencies via `python -m pip install -r requirements.txt`
    * If using redis cache, install the redis package via `python -m pip install redis`
    * Gunicorn will also be needed it deploying to production (`python -m pip install gunicorn`)
2. Make the .env file with the following info (see below for an example):
    * File should be name ".env" and not "SOMETHING.env". 
    * IS_PROD: True/False, whether to use production configuration
    * LOCAL_IP: Device network IP if running public Flask test server (optional, only used if IS_PROD is False)
    * LOCAL_STORAGE_PATH: Path to the data if it is not stored in the project directory (optional, see config.py for details)
    * Redis (cache) params (optional, see config.py for details)
    * Add .env to gitignore to avoid accidentally sharing secret information 
3. Adjust settings in config.py
    * Set project title and info
    * Set project specific data paths and settings

.env example (file is simply named '.env', not 'something.env'):

```
LOCAL_IP='192.168.0.1'
IS_PROD=False
```

---

Workflow
--------

#### Adding new pages

1. Define the page layout and components in a `dbc.Container` object (see `dashapp/page_template.py` for an example)
2. Import the container in `dashapp/layout.py`
3. Create a new entry in the `PAGES` variable in `dashapp/layout.py` to register the new page. Follow the instruction in the file for additional details.

Each page should have its own .py file. If building a complex project with many pages, consider grouping them in subdirectories to keep things tidy. 
If a page has multiple independent complex components, consider placing each component and its corresponding callbacks in different files and importing
them in the page layout.  
Callbacks and component Ids are registered globally and shared across the whole project. Pages can thus access components from other pages, although it 
is best to keep pages independent to avoid weird behaviours. If some data must be shared between pages, consider using a `dcc.Store` placed in 
`layout.py` instead.  
To avoid accidental conflicts between component ids, it is strongly recommended to prefix component ids with the page name, e.g. `results-page-graph`, `predictions-page-graph`, etc.

#### Building pages

All page components should be added as children of the base `dbc.Container` object. The base layout can be defined using dbc layout 
components (rows and cols) within that container, and specific components placed inside that layout. For a basic example, 
refer to `dashapp/page_template.py`.

The typical page layout consists of one or many `dbc.Card` or `dbc.Jumbotron` in which the actual content is placed. 

SPECIFY DESIGN PATTERNS AND CSS CLASSES HERE (or link to another doc file)


#### Loading new data

The DfManager and MdManager classes make it easy to use and manage Pandas DataFrames and markdown files as the main data sources.

**Dataframes**

This template uses Pandas DataFrames as the default data format. Pickled dataframes, either copied from other projects or generated locally, are loaded in `dashapp/__init__.py` when 
the server starts. Pages and callbacks can access the data by importing the appropriate variables, e.g. `from dashapp import df`. This avoids having to 
setup a database and helps keeping things fast and lightweight, although a more robust solution will be needed if working with large datasets.

IMPORTANT NOTE: Except in some specific cases, callbacks SHOULD NOT edit the dataframes, but only read the data. Editing a dataframe while the app is running can result in serious injuries.

The DfManager class (defined in `data/df_manager.py`) can help keep things organised when working with multiple dataframes. To add a DataFrame to the manager, 
simply add it to `DATAFRAMES_DICT` in `config.py` (see comments for detailed instructions).  
Each df defined in `DATAFRAME_DICT` will be loaded in a DfManager instance named `DM`, which can then be imported in any page with 
`from dashapp import DM` (This is enabled by default, no need to edit anything outside of config). Each df will be accessible as an instance variable 
of `DM`, e.g. `DM.TEST_DF`.  
A doc file (df_doc.md) describing all the loaded dfs is also created (or updated) whenever the app is started. (This can be 
turned off by setting `GENERATE_DF_DOC_FILE` to `False` in `config.py`). This data is also accessible via `DM.doc_md`, which can be useful as a quick 
reference or cheatsheet during development when working with multiple dfs (see `dashapp/examples/df_doc_page.py`).

**Markdowns**

Most texts should be stored as markdown files.

**Others (static, etc.)**

* data is loaded in .dashapp.__init__.py
  * specific data is imported by modules when needed. Never edit base DFs in callbacks!
* .dashapp.tabindex is the main page
  * import tab containers from other files (e.g. exampletab.py and abouttab.py) and update TABS variable
* Tabs should be built as modules in their own subdirectory
  * Tab components can be split into different files for more modularity

---

Deployment
----------

Deployment instructions for Ubuntu with nginx and gunicorn.

Coming soon..

---

Useful tips
-----------

#### Styling and static assets

Base bootstrap style

Custom css in assets (with some general classes)

Favicon and images

#### Data Management and caching

data managers

using in modules

df doc

caching

#### Templates

pycharm templates

#### 


