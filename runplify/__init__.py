from ._version import __version__
from .handlers import TutorialHandler


""" def _jupyter_labextension_paths():
    return [{
        "src": "labextension",
        "dest": "runplify"
    }] """

def _jupyter_server_extension_points():
    return [{
        "module": "runplify"
    }]

def load_jupyter_server_extension(server_app):
    handlers = [("/mybutton/hello", TutorialHandler)]
    server_app.web_app.add_handlers(".*$", handlers)
