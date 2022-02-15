from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from dashapp import DM
import pandas as pd

# Import app and cache only if needed
#from dashapp import cache


def make_cluster_profiles():

    c = {}

    s_df = DM.SUBJECTS_CORPUSFRAME
    s_df = s_df.div(s_df.sum(axis=1), axis=0)
    s_df['cluster'] = DM.TOPIC_REDUCTIONS['cluster']

    subj_groups = s_df.groupby('cluster').apply(lambda grp: grp.mean(numeric_only=True).nlargest(10))

    topic_groups = DM.TOPIC_REDUCTIONS.groupby('cluster')['main_topic_name'].apply(lambda grp: grp.value_counts().nlargest(10))

    j_df = DM.METADATA_CORPUSFRAME
    j_df['cluster'] = DM.TOPIC_REDUCTIONS['cluster']
    journal_groups = j_df.groupby('cluster')['source'].apply(lambda grp: grp.value_counts().nlargest(10))

    for cluster in sorted(DM.TOPIC_REDUCTIONS['cluster'].unique()):
        d = pd.concat([topic_groups[cluster].reset_index(), subj_groups[cluster].reset_index(), journal_groups[cluster].reset_index()], axis=1)
        d.columns = ['Topic Name', 'Docs with topic as main', 'Subject', 'Probability', 'Source', 'Number of docs']
        c[cluster] = d.to_markdown(index=False)
        # c.append(d.to_records(index=False))
    return c


content_card = dbc.Card([
    dbc.CardHeader([
        html.H3('Cluster profiles'),
    ], className='content-card-head'),
    dbc.CardBody([
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div([dcc.Markdown(c) for c in make_cluster_profiles().values()])
                    #dcc.Markdown(cluster_topic_profiles().to_markdown())
                ]),
                #dbc.Col([
                #    dcc.Markdown(calc_subject_profiles().to_markdown())
                #])
            ])
        ], className='content-text'),
    ])
],  className='content-card')


metatest_page_layout = dbc.Container([
    dbc.Row([
        dbc.Col(content_card, lg=10),
    ], justify='center'),
], id='page-id', className='std-content-div', fluid=True)
