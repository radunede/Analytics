from dash import dcc as dcc
from dash import html as html
import dash_bootstrap_components as dbc
import src.core.crypto_stats as cs

stats = cs.CryptoStats()

layout = html.Div(
    [
        dbc.Row(dbc.Col(html.Div(stats.get_summary_table(['MANA','ALGO'])),width=6))
    ]
)

