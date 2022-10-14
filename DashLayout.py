from dash import Dash, dcc, html, Input, Output, State
import plotly
import plotly.graph_objects as go
from MonitorKeyboard import *
import threading

app = Dash(__name__) #App


app.layout = html.Div([
    html.H6(children = "Change the value in the text box to see callbacks in action!"),
    html.Div([
        html.H5(children="Input: "),

        html.Button(id = "enableListener", children="enable listening",n_clicks=0),
        dcc.Input(id='textField', value='initial value', type='text')
    ]),
    html.Div(id="hiddenDiv",children = "xxx", style={"display":"None"}),
    html.Div(id="hiddenDiv2",children = "xxx", style={"display":"None"}),
    html.Br(),
    html.Div(id='my-output'),
    dcc.Graph(id="keysGraph"),
    dcc.Interval(
        id='intervalComponent',
        interval=1 * 250,  # in milliseconds
        n_intervals = 0
    ),
    html.H5(children="some text")
    # dcc.Graph(id="keysGraph2")
])

xList = []
yList = []
print(xList)
@app.callback(
    Output(component_id='keysGraph', component_property='figure'),
    [Input(component_id='textField', component_property='value'),
     Input(component_id='intervalComponent', component_property='n_intervals')]
)

# @app.callback(
#     Output(component_id='keysGraph', component_property='figure'),
#     Input(component_id='textField', component_property='value'),
#     State(component_id='intervalComponent', component_property='n_intervals')
# )
def updated_fig(value,interval):
    global xList
    data = get_keys() #gets keys
    print(interval)
    if interval < 5:
        xList = []
        data = []
    # if len(data)>25:
        # xList,data = xList[-25:],data[-25:]
    # Create the graph with subplots
    # fig = go.Figure(data=[go.Scatter(x=[i[0] for i in data], y=[i[1] for i in data])])
    # fig = go.Figure(data=[go.Scatter(x=[i for i in range(len(data))], y=[i[1] for i in data]) ])
    xList.append(interval)
    if len(data)<len(xList):
        data.append(["N/A",-0.25])
    fig = go.Figure(data=[go.Scatter(x=xList,
                                     y=[i[1] for i in data],
                                     #hovertext=[i[0] for i in data]
                                     )]
                    # layout=go.Layout(title="test",hovermode='closest')
                    )
    return fig

# @app.callback(
#     Output(component_id='keysGraph2', component_property='figure'),
#     Input(component_id='textField', component_property='value')
# )
# def updated_fig2(value):
#     data2 = get_keys()  # gets keys
#     fig = go.Figure(data=[go.Scatter(x=[i for i in range(len(data2))], y=[i[1] for i in data2]) ])
#     return fig
###########################
@app.callback(
    Output(component_id="hiddenDiv", component_property="children"),
    Input(component_id="enableListener",component_property="n_clicks"),
)
def enable_listener(n_click):
    print("listening has been enabled")
    if n_click == 1:
        start_listening()
    elif n_click > 1: #WIP - stopping doesn't work quite yet
        print("attempting to stop to listen")
        stop_listening()

@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='textField', component_property='value')
)
def update_output_div(input_value):
    get_keys()
    return f'Output: {input_value}'


if __name__ == '__main__':
    # process = threading.Thread(target=start_listening).start()
    # process.start()
    # start_listening()
    app.run_server(debug=True)