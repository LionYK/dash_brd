import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd


df1 = pd.read_csv('C://Users//User//Desktop//Учеба//diam.csv',sep = ';')
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True


SIDESTYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#222222",
}


CONTSTYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}





app.layout = html.Div([
    dcc.Location(id="url"),
    html.Div(
        [
            html.H2("Map", className="display-3", style={'color': 'white'}),
            html.Hr(style={'color': 'white'}),
            dbc.Nav(
                [
                    dbc.NavLink("Analysis", href="/page1", active="exact"),
                    dbc.NavLink("The effect", href="/page2", active="exact"),
                    dbc.NavLink("Thanks", href="/page3", active="exact"),
                ],
                vertical=True,pills=True),
        ],
        style=SIDESTYLE,
    ),
    html.Div(id="page-content", children=[], style=CONTSTYLE)
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")])




def pagecontent(pathname):
    if pathname == "/page1":
        return [

            html.Div(
                children=[
                    html.H1(children='Analysis diamonds dataset', className='header-title'),

                    html.P(children='maybe this demo will be useful to someone (:', className='header-description')
                ], className='header'),

            html.Div([
                dcc.Dropdown(
                    id='demo_drop',
                    options=[
                        {'label': 'Огранка', 'value': 'cut'},
                        {'label': 'Ясность(чистота)', 'value': 'clarity'},
                        {'label': 'Цвет', 'value': 'color'}
                    ],
                    value='cut', className="dropdown", style= {'margit-bottom':'32px'}
                ), dcc.Graph(id='output_graph')], className="card")
                ]

    elif pathname == "/page2":
        return [
            html.Div(
                children=[
                html.H1('The effect of the carat on price',className='header-title',
                        style={'textAlign':'center'})
                    ], className='header'),
                dcc.Graph(id='graph1',
                         figure=px.scatter(df1,x='carat',
                         y= 'price'),className="card"),

                dcc.Graph(id='graph2',
                         figure=px.scatter(df1,x='carat',
                         y= 'price',facet_col= 'color'),className="card")
                ]
    elif pathname == "/page3":
        return [
            html.Div(
                children=[
                    html.H1(children='Thank you for your attention! :)', className='header-title'),

                ], className='header')

                ]

@app.callback(
    Output(component_id='output_graph', component_property='figure'),
    [Input(component_id='demo_drop', component_property='value')]
)

def update_output(value):
    if value == 'cut':
        h = df1.groupby(['cut'], as_index=False, sort=False)['carat'].count()
    elif value == 'clarity':
        h = df1.groupby(['clarity'], as_index=False, sort=False)['carat'].count()
    elif value == 'color':
        h = df1.groupby(['color'], as_index=False, sort=False)['carat'].count()
    fig = px.bar(h, x=value, y="carat", labels={"carat": "Count"})
    return fig

if __name__=='__main__':
    app.run_server(debug=True, port=3000)