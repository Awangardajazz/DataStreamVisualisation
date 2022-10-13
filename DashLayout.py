from dash import Dash, dcc, html, Input, Output
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
    html.Br(),
    html.Div(id='my-output'),
    dcc.Graph(id="keysGraph")

])

@app.callback(
    Output(component_id='keysGraph', component_property='figure'),
    Input(component_id='textField', component_property='value')
)
def updated_fig(value):
    data = get_keys() #gets keys
    # Create the graph with subplots
    # fig = go.Figure(data=[go.Scatter(x=[i[0] for i in data], y=[i[1] for i in data])])
    fig = go.Figure(data=[go.Scatter(x=[i for i in range(len(data))], y=[i[1] for i in data]) ])

    # fig['layout']['margin'] = {
    #     'l': 30, 'r': 10, 'b': 30, 't': 10
    # }
    # fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
    #
    # fig.append_trace({
    #     'x': data[0],
    #     'y': data[1],
    #     'name': 'aaa',
    #     'mode': 'bbb',
    #     'type': 'scatter'
    # }, 1, 1)
    # fig.append_trace({
    #     'x': data['Longitude'],
    #     'y': data['Latitude'],
    #     'text': data['time'],
    #     'name': 'Longitude vs Latitude',
    #     'mode': 'lines+markers',
    #     'type': 'scatter'
    # }, 2, 1)

    return fig

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