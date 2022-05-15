from dash import dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px

from dashapp import DM, cache
from . import CLUSTER_MAP

# Graph settings inputs
controls_div = html.Div([
    # 2d 3d
    # topics ou clusters
    # tsne ou umap?
    # N docs, genre 10-25-50-100%
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Label('Representation type', className='radio-label'), # Since each article's position is determined by its topic profile, dimensionality reduction algorithm is required
                dbc.RadioItems(
                    options=[{'label': '3d T-SNE', 'value': 3}, {'label': '2d T-SNE', 'value': 2}],
                    value=3,
                    id='topics-scatter-dims-radio',
                    className='content-text-small'
                ),
            ], className='input-div')
        ], ),
    ]),

    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Label('Rendered documents', className='radio-label'), # Chose wheter to render a random subset of documents or the full corpus. To help with performance and readability.
                dbc.RadioItems(
                    options=[
                        {'label': f'10% ({int(0.1*len(DM.METADATA_CORPUSFRAME))} documents)', 'value': int(0.1*len(DM.METADATA_CORPUSFRAME))},
                        {'label': f'25% ({int(0.25*len(DM.METADATA_CORPUSFRAME))} documents)', 'value': int(0.25*len(DM.METADATA_CORPUSFRAME))},
                        {'label': f'50% ({int(0.5*len(DM.METADATA_CORPUSFRAME))} documents)', 'value': int(0.5*len(DM.METADATA_CORPUSFRAME))},
                        {'label': f'100% ({len(DM.METADATA_CORPUSFRAME)} documents)', 'value': len(DM.METADATA_CORPUSFRAME)}
                    ],
                    value=int(0.25*len(DM.METADATA_CORPUSFRAME)),
                    id='topics-scatter-ndocs-radio',
                    className='content-text-small'
                ),
            ], className='input-div'),
        ]),
    ]),

])


left_div = html.Div([
    dbc.Row([
        dbc.Col([
            html.Div('Graph settings', className='cshps-subtitle')
        ]),
    ], style={'margin-top': '1rem'}),

    dbc.Row([
        dbc.Col([
            controls_div
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.Div(dcc.Markdown('Click on a point to show the document\'s details'), id='topics-scatter-details')
        ])
    ])
])

# Graph object
graph_div = html.Div([
    #dbc.Spinner(dcc.Graph(id='topics-scatter-graph', style={'height': '90vh', 'max-height': '100vw'})),
    html.Div(dbc.Spinner(dcc.Graph(id='topics-scatter-graph', className='graph-large')), className='graph-container'),
])

cshps_topics_scatter_maindiv = dbc.Card([
    dbc.Row([
        dbc.Col([
            # Title
            html.Div('Topics and Clusters Visualisation', className='cshps-title')
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            # Explanatory text
            dcc.Markdown(
                'Each point on the figure represents an article. Colors represent each of the 4 clusters.' +
                '\n\n' +
                'Use scroll to zoom in and out, and left clic to rotate. Specific clusters can be hidden by clicking their name in the legend.',
                className='cshps-md'
            ),
        ], lg=6),
    ]),

    dbc.Row([
        dbc.Col([
            html.Hr(className='cshps-hr-full'),
        ])
    ]),

    dbc.Row([
        dbc.Col([
            graph_div
        ], className='order-lg-last', lg=9),

        dbc.Col([
            left_div,
        ], lg=3),

    ]),
], body=True, className='content-card')


@callback(Output('topics-scatter-graph', 'figure'),
          [Input('topics-scatter-dims-radio', 'value'),
           Input('topics-scatter-ndocs-radio', 'value'),])
def update_topic_scatter(n_dims: int, n_docs: int):

    color_col = 'cluster'
    viz_data = 'cluster'
    reduc_cols = ['main_topic_name', 'main_topic', 'cluster', 'tsne_3d_x', 'tsne_3d_y', 'tsne_3d_z']

    df = DM.TOPIC_REDUCTIONS.sample(n_docs).loc[:, reduc_cols]
    df[['title', 'source', 'collab', 'year', 'citation']] = DM.METADATA_CORPUSFRAME.loc[df.index, ['title', 'source', 'collab', 'year', 'citation']]

    df['cluster'] = df.cluster.map(CLUSTER_MAP)

    title = 'Document-Topics Scattterplot'
    hover_name = df.apply(lambda x: f'{x["collab"]} ({x["year"]})', axis=1)
    hover_data = {
                     'Title': df['title'].map(lambda x: x if len(x) < 60 else x[:60] + '...'),
                     'Journal': df['source'],
                     'Main Topic': df['main_topic_name'],
                     'Cluster': df['cluster'],
                     'tsne_3d_x': False,
                     'tsne_3d_y': False,
                     'tsne_3d_z': False,
                     'main_topic': False,
                     'main_topic_name': False,
                     'cluster': False
                 }

    category_orders = {color_col: df[color_col].sort_values().values}
    if n_dims == 2:
        fig = px.scatter(df, x='tsne_3d_x', y='tsne_3d_y', color=color_col,
                         title=title, hover_name=hover_name, hover_data=hover_data,
                         custom_data=[df.index], category_orders=category_orders).update_traces(marker={'size': 3})
    else:
        fig = px.scatter_3d(df, x='tsne_3d_x', y='tsne_3d_y', z='tsne_3d_z', color=color_col,
                            title=title, hover_name=hover_name, hover_data=hover_data,
                            custom_data=[df.index], category_orders=category_orders).update_traces(marker={'size': 2})

    fig.update_layout(legend_title='Clusters', legend_itemsizing='constant',
                      margin_t=60, margin_b=30, margin_l=30, margin_r=30)
    #.update_layout(legend_title='Topics', legend_itemsizing='constant', paper_bgcolor='#fcfcfc',
    #               margin_t=60, margin_l=10, margin_b=60, margin_r=10, )
    #fig.update_scenes(xaxis={'showticklabels': False, 'title': {'text': ''}},
    #                  yaxis={'showticklabels': False, 'title': {'text': ''}},
    #                  zaxis={'showticklabels': False, 'title': {'text': ''}})
    return fig


@callback(
    Output('topics-scatter-details', 'children'),
    [Input('topics-scatter-graph', 'clickData')], prevent_initial_call=True
)
def update_doc_details(click_data):

    article_id = click_data['points'][0]['customdata'][0]
    article_data = DM.METADATA_CORPUSFRAME.loc[article_id]

    head = dcc.Markdown(f'**Selected document:** {article_data["collab"]} ({article_data["year"]})')
    title = article_data['title']
    source = article_data['source']
    citation = dcc.Markdown('**Full citation:** ' + article_data['citation'], className='content-text-tiny')

    cluster = DM.TOPIC_REDUCTIONS.loc[article_id, 'cluster']
    top_topics = DM.DOCTOPICS_DF.loc[article_id].nlargest(10)

    #columns = [{'name': 'Top document topics', 'id': 'topic'}, {'name': 'Weights', 'id': 'weight'}]
    #data = [{'topic': DM.TOPIC_NAMES_MAP[t], 'weight': f'{w:.4f}'} for t, w in top_topics.iteritems()]

    header = [html.Thead(html.Tr([
        html.Th('Topics', className='cshps-small-table-data'),
        html.Th('Weights', className='cshps-small-table-data')
    ]), className='content-text-small', style={'padding': '0.25rem'})]

    body = [html.Tbody([
        html.Tr([html.Td(DM.TOPIC_NAMES_MAP[t], className='cshps-small-table-data'), html.Td(f'{w:.4f}', className='cshps-small-table-data')]) for t, w in top_topics.iteritems()
    ])]

    details = f'**Title:** {title}  \n**Journal:** {source}  \n**Cluster:** {cluster}'

    return html.Div([
        html.H6(head),
        dcc.Markdown(details, className='content-text-small'),
        #dash_table.DataTable(columns=columns, data=data),
        dbc.Table(header+body, bordered=True, striped=True, hover=True),
        citation,
    ])


