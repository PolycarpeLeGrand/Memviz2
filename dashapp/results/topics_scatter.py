from dash import dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px

from dashapp import DM, cache


# Graph settings inputs
controls_div = html.Div([
    # 2d 3d
    # topics ou clusters
    # tsne ou umap?
    # N docs, genre 10-25-50-100%
    dbc.Row([
        dbc.Col([
            dbc.Label('Topics ou clusters'),
            dbc.RadioItems(
                options=[{'label': 'Clusters', 'value': 'clusters'}, {'label': 'Topics', 'value': 'topics'}],
                value='clusters',
                id='topics-scatter-data-radio'
            ),
        ], width=6),
        dbc.Col([
            dbc.Label('Nombre de dimensions'),
            dbc.RadioItems(
                options=[{'label': '3 Dimensions', 'value': 3}, {'label': '2 Dimensions', 'value': 2}],
                value=3,
                id='topics-scatter-dims-radio'
            ),
        ], width=6),
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Label('Nombre de documents affichés'),
            dbc.RadioItems(
                options=[
                    {'label': f'10% ({int(0.1*len(DM.METADATA_CORPUSFRAME))} documents)', 'value': int(0.1*len(DM.METADATA_CORPUSFRAME))},
                    {'label': f'25% ({int(0.25*len(DM.METADATA_CORPUSFRAME))} documents)', 'value': int(0.25*len(DM.METADATA_CORPUSFRAME))},
                    {'label': f'50% ({int(0.5*len(DM.METADATA_CORPUSFRAME))} documents)', 'value': int(0.5*len(DM.METADATA_CORPUSFRAME))},
                    {'label': f'100% ({len(DM.METADATA_CORPUSFRAME)} documents)', 'value': len(DM.METADATA_CORPUSFRAME)}
                ],
                value=int(0.25*len(DM.METADATA_CORPUSFRAME)),
                id='topics-scatter-ndocs-radio'
            ),
        ], width=8),
    ]),

])


left_div = html.Div([
    dbc.Row([
        dbc.Col([
            controls_div
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(html.H6('Cliquer sur un point pour afficher les détails du document'), id='topics-scatter-details')
        ])
    ])
])

# Graph object
graph_div = html.Div([
    dbc.Spinner(dcc.Graph(id='topics-scatter-graph', style={'height': '90vh', 'max-height': '100vw'})),
])

topics_scatter_maindiv = html.Div([

    dbc.Row([
        dbc.Col([
            html.H4('Visualisation des topics et clusters')
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            left_div,
        ], lg=3),
        dbc.Col([
            graph_div
        ], lg=9),
    ]),
])


@callback(Output('topics-scatter-graph', 'figure'),
          [Input('topics-scatter-data-radio', 'value'),
           Input('topics-scatter-dims-radio', 'value'),
           Input('topics-scatter-ndocs-radio', 'value'),])
def update_topic_scatter(viz_data, n_dims: int, n_docs: int):

    color_col = 'main_topic_name' if viz_data == 'topics' else 'cluster'
    reduc_cols = ['main_topic_name', 'main_topic', 'cluster', 'tsne_3d_x', 'tsne_3d_y', 'tsne_3d_z']

    df = DM.TOPIC_REDUCTIONS.sample(n_docs).loc[:, reduc_cols]
    df[['title', 'source', 'collab', 'year', 'citation']] = DM.METADATA_CORPUSFRAME.loc[df.index, ['title', 'source', 'collab', 'year', 'citation']]

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

    fig.update_layout(legend_title=viz_data.capitalize(), legend_itemsizing='constant')

    return fig


@callback(
    Output('topics-scatter-details', 'children'),
    [Input('topics-scatter-graph', 'clickData')], prevent_initial_call=True
)
def update_doc_details(click_data):

    article_id = click_data['points'][0]['customdata'][0]
    article_data = DM.METADATA_CORPUSFRAME.loc[article_id]

    head = f'Document sélectionné: {article_data["collab"]} ({article_data["year"]})'
    title = article_data['title']
    source = article_data['source']
    citation = article_data['citation']

    cluster = DM.TOPIC_REDUCTIONS.loc[article_id, 'cluster']
    top_topics = DM.DOCTOPICS_DF.loc[article_id].nlargest(10)

    columns = [{'name': 'Topic', 'id': 'topic'}, {'name': 'Poids', 'id': 'weight'}]
    data = [{'topic': DM.TOPIC_NAMES_MAP[t], 'weight': f'{w:.4f}'} for t, w in top_topics.iteritems()]

    details = f'**Titre:** {title}  \n**Source:** {source}  \n**Cluster:** {cluster}'

    return html.Div([
        html.H6(head),
        dcc.Markdown(details),
        dash_table.DataTable(columns=columns, data=data),
        citation,
    ])


