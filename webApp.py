import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output



# Attach the refined playerBoxScore to this if needed. This is a good foundation to the web app.

#df = playerBoxScore

app = dash.Dash(__name__)

app.layout = html.Div([
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} 
                for i in df.columns],
        data=df.to_dict('records'),
        style_cell=dict(textAlign='right'),
        style_header=dict(backgroundColor="mediumorchid" ,fontWeight='bold'),
        style_cell_conditional=[
        {'if': {'column_id': 'TEAM_ABBREVIATION'},
         'width': '100px'},
        {'if': {'column_id': 'PLAYER_NAME'},
         'width': '200px'},],
        style_data=dict(backgroundColor="yellow")

    )
    
])

app.run_server(debug=True)