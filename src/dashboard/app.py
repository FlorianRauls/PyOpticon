from dash import Dash, html, dash_table, dependencies
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
from datetime import datetime
import mysql.connector


def refreshData(connector, query, df):
    # get data from db
    df = pd.read_sql(query, con=connector)
    return df

   

# Initialize the app
app = Dash(__name__)

# connect to db
db = mysql.connector.connect(
    host="tracker-db",
    user="root",
    password="",
    port="3306",
    database="tracker"
    )

# get data from db
query = "SELECT * FROM tracking"
df_system = refreshData(db, query, pd.DataFrame())


# create scatter plot for data
fig = px.scatter(df_system, x="T", y="Upload_speed")
fig2 = px.scatter(df_system, x="T", y="Download_speed")
fig3 = px.scatter(df_system, x="T", y="Memory_usage")
fig4 = px.scatter(df_system, x="T", y="Cpu_usage")
fig5 = px.scatter(df_system, x="T", y="Uptime")
fig6 = px.scatter(df_system, x="T", y="Readtime")
fig7 = px.scatter(df_system, x="T", y="Writetime")


# Create a Dash layout
app.layout = html.Div([
    html.H1("PyOpticon Dashboard"),
    html.Div(id='live-update-text'),
    dcc.Graph(id='graph1', figure=fig),
    dcc.Graph(id='graph2', figure=fig2),
    dcc.Graph(id='graph3', figure=fig3),
    dcc.Graph(id='graph4', figure=fig4),
    dcc.Graph(id='graph5', figure=fig5),
    dcc.Graph(id='graph6', figure=fig6),
    dcc.Graph(id='graph7', figure=fig7),
    dcc.Interval(
        id='interval-component',
        interval=1*1000, # in milliseconds
        n_intervals=0
    )
])

# Define callback to update graph
@app.callback(
    [dependencies.Output('graph1', 'figure'),
    dependencies.Output('graph2', 'figure'),
    dependencies.Output('graph3', 'figure'),
    dependencies.Output('graph4', 'figure'),
    dependencies.Output('graph5', 'figure'),
    dependencies.Output('graph6', 'figure'),
    dependencies.Output('graph7', 'figure')],
    [dependencies.Input('interval-component', 'n_intervals')])

def update_graph(n):
    # get data from db
    query = "SELECT * FROM tracking"
    df_system = refreshData(db, query, pd.DataFrame())
    
    # create scatter plot for data
    fig = px.scatter(df_system, x="T", y="Upload_speed")
    fig2 = px.scatter(df_system, x="T", y="Download_speed")
    fig3 = px.scatter(df_system, x="T", y="Memory_usage")
    fig4 = px.scatter(df_system, x="T", y="Cpu_usage")
    fig5 = px.scatter(df_system, x="T", y="Uptime")
    fig6 = px.scatter(df_system, x="T", y="Readtime")
    fig7 = px.scatter(df_system, x="T", y="Writetime")
    
    return fig, fig2, fig3, fig4, fig5, fig6, fig7

# Style the app
# https://codepen.io/chriddyp/pen/bWLwgP.css
app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8080)