#%%
import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
import plotly.express as px
from Channel import channel
import pandas as pd
import re
import os
from functools import reduce

# def parse_time(time_str):
#     re.search()
pd.set_option('display.max_columns', None)
youtubers = {
    #"Mark Rober": "UCY1kMZp36IQSyNx_9h4mpCg",
    #"Marques Brownlee":'UUBJycsmduvYEL83R_U4JriQ',
    "Kurzgesagt": 'UCsXVk37bltHxD1rDPwtNM8Q',
    #"Joma Tech": 'UCV0qA-eDDICsRR9rPcnG7tw',
    #"Linus Tech Tips": 'UCXuqSBlHAE6Xw-yeJA0Tunw',
    #"Hacksmith Industries": 'UCjgpFI5dU-D1-kh9H1muoxQ',
    #"Jayz Two Cents": "UCkWQ0gDrqOCarmUKmppD7GQ",
    "Lofi Girl": "UCSJ4gkVC6NrvII8umztf0Ow",
    "Dani": "UCIabPXjvT5BVTxRDPCBBOOQ",
    #"Matt Lowne": "UCiW7-IEQCTqS9l7223whHZA",
    #"SethEverman": "UCoNRSwYHJdy-yV1b82ZdHfQ",
    #"VICE": "UCn8zNIfYAQNdrFRrr8oibKw",
    #"SmarterEveryDay": "UC6107grRI4m0o2-emgoDnAA"
}

#%%
# if os.path.isfile("cache/master_df.tsv"):
#     master_df = pd.read_csv("cache/master_df.tsv",sep='\t')
#     master_df['publishedAt'] = pd.to_datetime(master_df['publishedAt'])
#     master_df['duration'] = pd.to_timedelta(master_df['duration'])
# else:
df_list = []
print("Loading data...")
for name, key in youtubers.items():
    print(name)
    ytchannel = channel(key)
    df_list.append(ytchannel.get_all_data())

master_df = reduce(lambda x, y: pd.concat([x,y], ignore_index=True), df_list)

out_df = master_df.copy()

out_df.to_csv(".cache/master_df.tsv", index=False,sep='\t')

#%%
## Post-process on master_df 
master_df['channelTitle'] = master_df['channelTitle'].str.split(" –").str[0]

#%% 
## Initial Plots
# violin = px.violin(y=master_df.loc[master_df.'viewCount'], box=True, hover_data=master_df.columns)
# %%
metrics = ['log_views', 'log_likes', 'log_comments']
app = dash.Dash()
app.layout = html.Div(children=[
    html.H1(children='Youtube Channel Dashboard'),
    html.P(children='''
        This is a dashboard that interacts with the Youtube V3 API to provide channel metrics and info.  
    '''),
    html.Div([
        html.Div([
            html.H2(children='Single Channel Metrics'),
            dcc.Dropdown(
                id="YouTube Channel", options=[{'label': i,'value': i} for i in youtubers.keys()], 
                value='All', #style={'display': 'none'}
            )]
        )
    ]   
    ),
    html.Div([
        dcc.Graph(id='Channel Metrics', style={'width': '60vh', 'height': '60vh'})
    ],style={'display': 'flex', 'flex-direction': 'row'} #'width': '25%'}
    ),
    html.H2(children='Channel Comparisons'),
    html.Div([
        dcc.Dropdown(id="Metrics", options=[{'label': i,'value': i} for i in metrics], value='All',
            #style={'display': 'none'}
        ),
        html.Br(),
        dcc.Graph(id='Channel Comparison Metrics',style={'width': '60vh', 'height': '60vh'} )
    ],style={'padding': 10, 'display': 'flex', 'flex-direction': 'row'}
    ),
], style={})

display_channels = []
@app.callback(
    dash.dependencies.Output('Channel Comparison Metrics', 'figure'),
    [dash.dependencies.Input('Metrics', 'value') ]
)
def update_box_comparison(metric):
    #plot = px.histogram(x=df['viewCount']) #, box=True, hover_data=df.columns)
    plot = px.box(master_df, x='channelTitle', y=metric)
    return plot

display_channels = []
@app.callback(
    dash.dependencies.Output('Channel Metrics', 'figure'),
    [dash.dependencies.Input('YouTube Channel', 'value')]
)
def update_box_channel(channel):
    df = master_df.loc[master_df['channelTitle'] == channel]
    plot = px.box(df, y=metrics)
    return plot

#%%
if __name__ == '__main__':
    app.run_server()
    # fig = px.box(master_df, x='channelTitle', y='viewCount')
    # fig.show()
# %%
