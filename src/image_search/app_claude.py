import base64
import io
import os

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True
    ),
    html.Div(id='output-images', children=[])
])

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'png' in filename:
            extension = '.png'
        elif 'jpg' in filename:
            extension = '.jpg'
        else:
            extension = '.jpeg'
        image_data = f'data:image/{extension[1:]};base64,{contents.split(",")[1]}'
        return html.Img(src=image_data)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing the file.'
        ])

@app.callback(Output('output-images', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'))
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [parse_contents(c, n) for c, n in zip(list_of_contents, list_of_names)]
        return children

if __name__ == '__main__':
    app.run_server(debug=True)