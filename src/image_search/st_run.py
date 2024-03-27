import sys
from streamlit.web import cli as stcli
from pathlib import Path


def main():
    directory = Path(__file__).parent.resolve()
    app = "st_upload.py"
    app_path = f"{directory}/{app}"

    sys.argv = [
        "streamlit",
        "run",
        app_path
    ]
    sys.exit(stcli.main())

if __name__ == '__main__':
    main()