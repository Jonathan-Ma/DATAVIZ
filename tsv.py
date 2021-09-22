import dash
import dash_table
import pandas as pd
import dash_html_components as html


app = dash.Dash(__name__)

df = pd.read_csv('choleraDeaths.tsv', sep='\t')
df['Total'] = df['Attack'] + df['Death']
app.layout = html.Div([dash_table.DataTable(
    columns=[
        {"name": i, "id": i} for i in df.columns
    ],
    data=df.to_dict('records'),
    page_action='none',
    style_table={'height': '500px', 'overflowY': 'auto'},
    style_cell={'textAlign': 'center'}
)])


if __name__ == '__main__':
    app.run_server(debug=True)
