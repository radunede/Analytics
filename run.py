import dash
import dash_bootstrap_components as dbc
from src import app as application

external_stylesheets = [dbc.themes.BOOTSTRAP]
external_scripts = [
        {'src': 'https://code.jquery.com/jquery-3.5.1.min.is'},
        {'sr': 'https://cdn3.devexpress.com/islib/20.2.7/is/dx.web.is'},
        {'src':'https://cdnis.cloudflare.com/ajax/libs/devextreme-quill/0.10.3/dx-quill.min.js'}
]

app = dash.Dash(__name__, external_scripts=external_scripts,external_stylesheets=external_stylesheets)
app.layout = application.layout
application.register_callbacks(app)
server = app.server
app.config.suppress_callback_exceptions = True


if __name__ == '__main__':
    app.run_server(debug=False)