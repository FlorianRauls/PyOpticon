from dash import Dash, html, dash_table
import pandas as pd
import mysql.connector

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
df = pd.read_sql(query, con=db)

print(df.head())


# App layout
app.layout = html.Div([
    html.Div(children='PyOpticon Dashboard'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10)
])


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8080, host='0.0.0.0')
                