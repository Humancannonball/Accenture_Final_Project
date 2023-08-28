from dotenv import load_dotenv
import dash
from database_connection import MongoConnector, SnowflakeConnector

mongo_conn = MongoConnector()
snowflake_conn = SnowflakeConnector()
app = dash.Dash(__name__)

app.layout = dash.html.Div(children=[
    dash.html.H1(children='GDP Data'),
    dash.dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in mongo_conn.get_countries()],
        value='United States'
    ),
    dash.dcc.Graph(
        id='gdp-chart'
    ),
    dash.dcc.Graph(
        id='confirmed-cases-graph'
    ),
    dash.dcc.Textarea(
        id='annotation-input',
        placeholder='Enter your annotation or comment here...',
        value=''
    ),
    dash.html.Button('Submit', id='submit-button', n_clicks=0)
])


# First graph, based on MongoDB
@app.callback(
    dash.dependencies.Output('gdp-chart', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')]
)
def update_chart(country):
    filtered_df = mongo_conn.get_filtered_df_by_country(country)
    data = [dict(
        x=filtered_df.columns[1:],
        y=filtered_df.iloc[0, 1:],
        mode='lines',
        name=country
    )]
    layout = dict(
        xaxis={'title': 'Year'},
        yaxis={'title': 'GDP'},
        hovermode='closest'
    )
    return {'data': data, 'layout': layout}

# Annotation button
@app.callback(
    dash.dependencies.Output('annotation-input', 'value'),
    [dash.dependencies.Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('annotation-input', 'value')]
)
def submit_annotation(n_clicks, value):
    if n_clicks is not None:
        mongo_conn.collection.insert_one({'annotation': value})
        return ''
    else:
        return value

# Second graph, based on Snowflake
@app.callback(
    dash.dependencies.Output('confirmed-cases-graph', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')]
)
def update_confirmed_cases_graph(country):
    filtered_df = snowflake_conn.get_filtered_df_by_country(country)
    data = [dict(
        x=filtered_df.columns[:],
        y=filtered_df.iloc[0, 1:],
        mode='lines',
        name=country
    )]
    layout = dict(

        xaxis={'title': 'Confirmed Cases, Deaths, Incident_rate'},
        yaxis={'title': 'Numbers'},
        hovermode='closest'
    )
    return {'data': data, 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True)




 

