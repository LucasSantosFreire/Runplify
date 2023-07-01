from ._version import __version__
from .handlers import RunplifyHandler

def _jupyter_server_extension_points():
    return [{
        "module": "runplify"
    }]

def load_jupyter_server_extension(server_app):
    handlers = [("/runplify", RunplifyHandler)]
    server_app.web_app.add_handlers(".*$", handlers)
