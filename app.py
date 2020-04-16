import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

### APP
app = dash.Dash(
    __name__, 
    external_stylesheets=external_stylesheets
)
app.title = 'COVIS19'

server = app.server
app.config.suppress_callback_exceptions = True