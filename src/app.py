from dash import dcc as dcc
from dash import html as html
import dash_bootstrap_components as dbc
import src.ui.oil as oil
import src.ui.crypto as crypto
import src.ui.equities as equities
from dash.dependencies import Input, Output, State, MATCH


is_open = {'verticalAlign':'middle', 'display':'block'}
is_closed = {'verticalAlign':'middle', 'display':'none'}

content_style = {
    'marginRight':'2rem',
    'marginLeft':'2rem',
    'padding':'2rem 1rem'
}

content = html.Div(id='page-content',style=content_style)
sidebar = dbc.NavbarSimple(brand='Analytics',
    children=[
        dbc.NavItem(dbc.NavLink("🛢️ Oil",href='/oil',active='exact')),
        dbc.NavItem(dbc.NavLink("🪙 Crypto",href='/crypto',active='exact')),
        dbc.NavItem(dbc.NavLink("🏛️ Equities",href='/equities',active='exact') )
    ],dark=True,color='dark',expand='lg'
)

layout = html.Div([dcc.Location(id='url'),sidebar,content])


def render_page(pathname):
    try:

        if pathname.endswith('/'):
            return html.H3('Welcome to cross-asset analytics!')
        elif pathname.endswith('/oil'):
            return oil.layout
        elif pathname.endswith('/crypto'):
            return crypto.layout
        elif pathname.endswith('/equities'):
            return equities.layout
    except:
        return html.Div('Error occured')

def register_callbacks(app):
    app.callback(Output('page-content','children'),Input('url','pathname'))(render_page)


