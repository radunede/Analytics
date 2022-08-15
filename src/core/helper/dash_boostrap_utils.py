import dash_bootstrap_components as dbc
from dash.dash_table.Format import Format, Scheme, Group, Trim, Sign
from dash import dash_table

def generate_bootstrao_table(df):
    return dbc.Table.from_dataframe(df,striped=True,bordered=True,hover=True,size='sm')

def generate_table_with_formatting(dataframe, precision=1):
    columns = [{'name': i,'id': i,'type':'numeric','format': Format(
    precision=precision,
    scheme=Scheme.fixed,
    trim=Trim.yes,
    group=Group.yes,
    groups=3,
    group_delimiter=",",
    decimal_delimiter=".").sign(Sign.parantheses)} for i in dataframe.columns ]

    return dash_table.DataTable(
    data=dataframe.to_dict('records'),
    style_table={ 'margin':'auto'},
    sort_action='native',
    style_header={
    'fontWeight': 'bold'
    },
    style_cell={'textAlign': 'center'},
    columns=columns,
    style_data_conditional=(
        [
            {
           'if': {
            'filter _query': '{{{}}} > 0'.format(col),
            'column_id': col
            },
            'backgroundColor':'#3ccf48',
            'color':'black'
            } for col in [x for x in dataframe.columns]
        ]+
        [
            {
                'if' : {
            'filter_query': '{{{}}} < 0'.format(col),
            'column_id': col
            },
        'backgroundColor' :'＃FF514B',
        'color': 'black'
            } for col in [x for x in dataframe.columns]
        ])
    )