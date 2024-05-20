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
            dbc.Col(dbc.Button(id='rotate-button', children="Rotate", n_clicks=1, disabled=True), width=1),
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
            dbc.Col([html.Div('Similar Images', className="text-primary text-center fs-3"),
                     html.Div(id='output-image-found'),
                     html.Hr(style={"height": "30px"}),
                     ]),
        ]),
        dbc.Row([
            dbc.Col([html.Div('Image to Find', className="text-primary text-center fs-3"),
                     html.Div(id='output-image-upload'),
                     html.Hr(style={"height": "10px"}),
                     ]),
        ]),
    ], fluid=True)


def parse_contents(contents, filename, date):
    image = ih.image_from_base64(contents)
    # print(image.size)
    height, ii, width, _, _ = ih.resize_image_keep_aspect_ratio(image)
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
    height, ii, width, _, _ = ih.resize_image_keep_aspect_ratio(image)
    # print(ii.size)
    return html.Div([
        html.H5(path),
        html.H6(f"{width} x {height}"),
        # html.H6(datetime.datetime.fromtimestamp(date)),
        html.Img(src=ii),
    ])


@callback(Output('output-image-upload', 'children'),
          Output("find-button", "n_clicks"),
          [Input('upload-image', 'contents')],
          [Input('upload-image', 'filename')],
          [Input('upload-image', 'last_modified')],
          prevent_initial_call=True,
          )
def upload_image(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)]
        return children, 1
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
              (Output("rotate-button", "disabled"), True, False),
              ]
      )
def find_images(clicks, root_dir, hash_function, image_to_find, threshold):
    print(f"{clicks} {root_dir} {hash_function} {threshold}")
    image_searcher = ImageSearcher(root_dir, hash_function)

    image = ih.image_from_base64(image_to_find)
    print(f"hidden image {image.height} {image.width}")

    images = image_searcher.find_similar_image(image, "Uploaded", threshold=threshold)
    if images is not None and len(images) > 0:
        image_html = [load_image(a) for a in images]
        return image_html
    return html.Div('No Images Found', className="text-danger text-center fs-3", style={"color": "red", "font-weight": "bold"},)


@callback(Output('image-to-find-hidden', 'src'),
          Output('image-to-find', 'src'),
          Output("find-button", "n_clicks", allow_duplicate=True),
          Input("rotate-button", "n_clicks"),
          State('image-to-find-hidden', 'src'),
          prevent_initial_call=True,
          running=[
              (Output("catalog-button", "disabled"), True, False),
              (Output("find-button", "disabled"), True, False),
              (Output("rotate-button", "disabled"), True, False),
              ]
      )
def rotate_image(clicks, image_to_find_64):
    image_to_find = ih.image_from_base64(image_to_find_64)
    image = ih.rotate_image(image_to_find, -90)
    height, ii, width, new_height, new_width = ih.resize_image_keep_aspect_ratio(image)
    print(f"image_to_find hidden image {image_to_find.height} {image_to_find.width}")
    print(f"rotated hidden image {image.height} {image.width}")
    print(f"display image {new_height} {new_width}")
    return image, ii, 1


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
                   (Output("rotate-button", "disabled"), True, False),
                   (Output("catalog-alert", "is_open"), True, False),
                   ]
          )
def catalog_images(clicks, root_dir, hash_function):
    print(f"{clicks} {root_dir} {hash_function}")
    ImageSearcher(root_dir, hash_function, catalog=True)
    print(f"catalog finished")
    return html.Div("Warning cataloging images may take a long time")

def main(args):
    # Initialize the app - incorporate a Dash Bootstrap theme
    external_stylesheets = [dbc.themes.CERULEAN]
    app = Dash(__name__,
               external_stylesheets=external_stylesheets,
               suppress_callback_exceptions=True, )

    # App layout
    app.layout = layout(args.root_dir)
    app.run_server(debug=args.debug, host=args.host, port=args.port)


if __name__ == '__main__':
    parser = ArgumentParser(description="Find image files in a directory tree.")
    parser.add_argument("-r", "--root_dir", required=False, default=f"{os.getenv('HOME')}/Pictures/Media/photos/scanned",
                        help="The root directory to search for images and location of the catalog.")
    parser.add_argument("-d", "--debug", required=False, default=False, action='store_true',
                        help="Enable debug mode.")
    parser.add_argument("-H", "--host", required=False, default="127.0.0.1",
                        help="The hostname or ip of the server.")
    parser.add_argument("-p", "--port", required=False, default="8050",
                        help="The port the server is listening on.")
    args = parser.parse_args()
    main(args)

