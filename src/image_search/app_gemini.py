import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import base64
import PIL.Image
import io

MAX_IMAGE_WIDTH = 400  # Define a maximum width for uploaded images

app = dash.Dash(__name__)

# Define layout for app
app.layout = html.Div([
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files'),
        ]),
        multiple=True
    ),
    html.Div(id='output-image-container')
])

# Callback function to process uploaded images
@app.callback(
    Output(component_id='output-image-container', component_property='children'),
    [Input(component_id='upload-image', component_property='contents')]
)
def update_output(contents):
    if contents is not None:
        images = []
        for content in contents:
            # Decode and convert uploaded content to PIL image
            data = content.split(',')[1]
            decoded_data = base64.b64decode(data)
            image_stream = io.BytesIO(decoded_data)
            image = PIL.Image.open(image_stream)

            # Resize image to fit within MAX_IMAGE_WIDTH while maintaining aspect ratio
            width, height = image.size
            if width > MAX_IMAGE_WIDTH:
                ratio = MAX_IMAGE_WIDTH / float(width)
                height = int(height * ratio)
                image = image.resize((MAX_IMAGE_WIDTH, height))

            # Convert image to encoded format for display
            encoded_image = base64.b64encode(image.convert('RGB').tobytes()).decode('utf-8')

            # Prepare image display with Dash HTML components
            images.append(html.Div([
                html.Img(src=encoded_image)  # Set image width to 100% of container
            ]))

        return images
    else:
        return [html.Div(children='Drag & Drop images here or click to upload?')]

if __name__ == '__main__':
    app.run_server(debug=True)
