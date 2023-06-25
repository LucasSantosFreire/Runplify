#__import__('setuptools').setup()
from setuptools import setup
setup(
    name="runplify",
    include_package_data=True,
    data_files=[
        (
            "etc/jupyter/jupyter_server_config.d",
            ["jupyter-config/jupyter_server_config.d/runplify.json"]
        ),
    ]

)