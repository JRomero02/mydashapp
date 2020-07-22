#libraries
#pip install s3fs
import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import boto3


app = dash.Dash(__name__)
#server = app.server
application = app.server




# get your credentials from environment variables

client = boto3.client('s3', aws_access_key_id='....',
        aws_secret_access_key='..')

path='s3://......csv'
df = pd.read_csv(path)
# bucket_name = 'my_bucket'

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)

df = df.groupby(['State', 'Year', 'state_code'])[['Unemployment_rate']].mean() 
df.reset_index(inplace=True)
#print(df[:5])



# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Unemployement Percentage from 2000 to 2019 ", style={'text-align': 'center'}),

    #dcc.Dropdown(id="slct_year",
    dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "2000", "value": 2000},
                     {"label": "2001", "value": 2001},
                     {"label": "2002", "value": 2002},
                     {"label": "2003", "value": 2003},
                     {"label": "2004", "value": 2004},
                     {"label": "2005", "value": 2005},
                     {"label": "2006", "value": 2006},
                     {"label": "2007", "value": 2007},
                     {"label": "2008", "value": 2008},
                     {"label": "2009", "value": 2009},
                     {"label": "2010", "value": 2010},
                     {"label": "2011", "value": 2011},
                     {"label": "2012", "value": 2012},
                     {"label": "2013", "value": 2013},
                     {"label": "2014", "value": 2014},
                     {"label": "2015", "value": 2015},
                     {"label": "2016", "value": 2016},
                     {"label": "2017", "value": 2017},
                     {"label": "2018", "value": 2018},
                     {"label": "2019", "value": 2019}],
                 multi=False,
                 value=2019,
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_map', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Year"] == option_slctd]

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Unemployment_rate',
        hover_data=['State', 'Unemployment_rate'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Unemployment rate': '% Unemployed'},
        template='plotly_dark'
    )
     #Plotly Graph Objects (GO)
    fig = go.Figure(
         data=[go.Choropleth(
             locationmode='USA-states',
             locations=dff['state_code'],
             z=dff["Unemployment_rate"].astype(float),
             colorscale='Reds',
         )]
     )

    fig.update_layout(
         title_text="Unemployment Rates in the US from 2000 to 2019",
         title_xanchor="center",
         title_font=dict(size=24),
         title_x=0.5,
         geo=dict(scope='usa'),
     )


    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    #app.run_server(debug=True)
    application.run(debug=True, port=8080)


