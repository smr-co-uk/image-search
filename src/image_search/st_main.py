import sys, os
from streamlit.web import cli as stcli
from pathlib import Path
from argparse import ArgumentParser


def main(args):
    directory = Path(__file__).parent.resolve()
    app = "streamlit_app.py"
    app_path = f"{directory}/{app}"

    sys.argv = [
        "streamlit",
        "run",
        "--server.port", args.port,
        "--server.address", args.host,
        app_path,
        "--",
        "--root_dir", args.root_dir
    ]
    sys.exit(stcli.main())

if __name__ == '__main__':
    parser = ArgumentParser(description="Find image files in a directory tree.")
    parser.add_argument("-r", "--root_dir", required=False,
                        default=f"{os.getenv('HOME')}/Pictures/Media/photos/scanned",
                        help="The root directory to search for images and location of the catalog.")
    parser.add_argument("-d", "--debug", required=False, default=False, action='store_true',
                        help="Enable debug mode.")
    parser.add_argument("-H", "--host", required=False, default="localhost",
                        help="The hostname or ip of the server.")
    parser.add_argument("-p", "--port", required=False, default="8501",
                        help="The port the server is listening on.")
    args = parser.parse_args()
    main(args)