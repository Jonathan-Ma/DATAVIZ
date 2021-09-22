import dash
import dash_table
import pandas as pd
from collections import OrderedDict

app = dash.Dash(__name__)

df = pd.read_csv('choleraDeaths.tsv', sep='\t')

app.layout = dash_table.DataTable(
    data=df.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df.columns],
    page_action='none',
    style_table={'height': '300px', 'overflowY': 'auto'}
)

if __name__ == '__main__':
    app.run_server(debug=True)

