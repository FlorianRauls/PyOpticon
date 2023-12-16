from dash import Dash, html, dash_table
import dash_core_components as dcc
import pandas as pd
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

# set query
query = "SELECT * FROM tracking"

# get data from db
df = refreshData(db, query, pd.DataFrame())

# add dash chart
chart = dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': df['T'], 'y': df['Upload_speed'], 'type': 'line', 'name': 'Upload Speed'},
                {'x': df['T'], 'y': df['Download_speed'], 'type': 'line', 'name': 'Download Speed'},
                {'x': df['T'], 'y': df['Memory_usage'], 'type': 'line', 'name': 'Memory Usage'},
                {'x': df['T'], 'y': df['Cpu_usage'], 'type': 'line', 'name': 'CPU Usage'},
                {'x': df['T'], 'y': df['Uptime'], 'type': 'line', 'name': 'Uptime'},
                {'x': df['T'], 'y': df['Readtime'], 'type': 'line', 'name': 'Read Time'},
                {'x': df['T'], 'y': df['Writetime'], 'type': 'line', 'name': 'Write Time'},
            ],
            'layout': {
                'title': 'PyOpticon Dashboard'
            }
        }
    )

# add button to refresh data
button = html.Button('Refresh Data', id='button')


# App layout
app.layout = html.Div([
    html.Div(children='PyOpticon Dashboard'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    chart,
    button
])


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8080, host='0.0.0.0')
                