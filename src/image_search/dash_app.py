import datetime
import os
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Output, Input, State
from PIL import Image
from image_search import ImageSearcher
from argparse import ArgumentParser
import image_search.image_helper as ih


def layout(root_dir: str) -> dbc.Container:
    return dbc.Container([
        dbc.Row([
            html.Div('Find Similar Images App', className="text-primary text-center fs-3")
        ], className="mb-2"),
        dbc.Row([
            dbc.Col(html.Div("Root directory"), width=3),
            dbc.Col(dbc.Input(id="image-root", value=f"{root_dir}")),
            ], className="border mb-2 mt-2"),
        dbc.Row([
            dbc.Col(html.Div("Warning cataloging images may take a long time", id="warning-text"), width=3),
            dbc.Col(dbc.Button(id='catalog-button', children="Catalog Images", n_clicks=1)),
        ], className="border mb-2 mt-2"),
        dbc.Row([
            dbc.Col(dbc.Alert("Catalog in Progress", id='catalog-alert', color="warning", is_open=False),width=3),
        ], className="border mb-2 mt-2"),
        dbc.Row([
            dbc.Col(html.Div("Find Threshold"), width=3),
            dbc.Col(dbc.Input(id="threshold", value=1, type="number"), width=3),
        ], className="border mb-2 mt-2"),
        dbc.Row([
            dbc.Col(html.Div("Algorithm"), width=3),
            dbc.Col(dbc.RadioItems(id='algorithm-radio',
                               options=[{"label": x, "value": x} for x in ['average_hash', 'phash']],
                               value='average_hash',
                               inline=True,),
                    width="auto"),
            ], className="border mb-2 mt-2"),
        dbc.Row([
            dbc.Col(html.Div("Find images using algorithm and threshold"), width=3),
            dbc.Col(dbc.Button(id='find-button', children="Find", n_clicks=1, disabled=True), width=1),
        ], className="border mb-2 mt-2"),
        dbc.Row([
            dbc.Col([
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
                    # Allow multiple files to be uploaded
                    multiple=True
                ),
            ]),
        ], className="border mb-2"),
        dbc.Row([
            dbc.Col([html.Div('Image to be Found', className="text-primary text-center fs-3"),
                     html.Div(id='output-image-upload'),
                     html.Hr(style={"height": "10px"}),
                     ]),
        ]),
        dbc.Row([
            dbc.Col([html.Div('Images Found', className="text-primary text-center fs-3"),
                     html.Div(id='output-image-found'),
                     html.Hr(style={"height": "30px"}),
                     ]),
        ]),
    ], fluid=True)


def parse_contents(contents, filename, date):
    image = ih.image_from_base64(contents)
    # print(image.size)
    height, ii, width = ih.resize_image_keep_aspect_ratio(image)
    # print(ii.size)
    return html.Div([
        html.H5(filename),
        html.H6(f"{width} x {height}"),
        html.H6(datetime.datetime.fromtimestamp(date)),
        # HTML Images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=image, id="image-to-find-hidden", hidden=True),
        html.Img(src=ii, id="image-to-find"),
    ])


def load_image(path):
    image = Image.open(path)
    # print(image.size)
    height, ii, width = ih.resize_image_keep_aspect_ratio(image)
    # print(ii.size)
    return html.Div([
        html.H5(path),
        html.H6(f"{width} x {height}"),
        # html.H6(datetime.datetime.fromtimestamp(date)),
        html.Img(src=ii),
    ])


@callback(Output('output-image-upload', 'children'),
          Output("find-button", "n_clicks"),
          Input("find-button", "n_clicks"),
          [Input('upload-image', 'contents')],
          [Input('upload-image', 'filename')],
          [Input('upload-image', 'last_modified')],
          prevent_initial_call=True,
          )
def upload_image(clicks, list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)]
        return children, clicks
        # if children is not None and len(children) > 0:
        # return [], 0


@callback(Output('output-image-found', 'children'),
          Input("find-button", "n_clicks"),
          State("image-root", "value"),
          State('algorithm-radio', 'value'),
          State('image-to-find-hidden', 'src'),
          State('threshold', 'value'),
          prevent_initial_call=True,
          running=[
              (Output("catalog-button", "disabled"), True, False),
              (Output("find-button", "disabled"), True, False),
              ]
      )
def find_images(clicks, root_dir, hash_function, image_to_find, threshold):
    print(f"{clicks} {root_dir} {hash_function} {threshold}")
    image_searcher = ImageSearcher(root_dir, hash_function)

    images = image_searcher.find_similar_image(ih.image_from_base64(image_to_find), "Uploaded", threshold=threshold)
    image_html = [load_image(a) for a in images]
    return image_html


@callback(Output('warning-text', 'children'),
          Input("catalog-button", "n_clicks"),
          State("image-root", "value"),
          State('algorithm-radio', 'value'),
          prevent_initial_call=True,
          running=[(Output("warning-text", "children"),
                    "Catalog in progress",
                    "Warning cataloging images may take a long time"),
                   (Output("catalog-button", "disabled"), True, False),
                   (Output("find-button", "disabled"), True, False),
                   (Output("catalog-alert", "is_open"), True, False),
                   ]
          )
def catalog_images(clicks, root_dir, hash_function):
    print(f"{clicks} {root_dir} {hash_function}")
    ImageSearcher(root_dir, hash_function, catalog=True)
    print(f"catalog finished")
    return html.Div("Warning cataloging images may take a long time")


if __name__ == '__main__':
    parser = ArgumentParser(description="Find image files in a directory tree.")
    parser.add_argument("-r", "--root_dir", required=False, default=f"{os.getenv('HOME')}/Pictures/Media/photos/scanned",
                        help="The root directory to search for images and location of the catalog.")
    args = parser.parse_args()
    # Initialize the app - incorporate a Dash Bootstrap theme
    external_stylesheets = [dbc.themes.CERULEAN]
    app = Dash(__name__,
               external_stylesheets=external_stylesheets,
               suppress_callback_exceptions=True, )

    # App layout
    app.layout = layout(args.root_dir)
    app.run_server(debug=True)
