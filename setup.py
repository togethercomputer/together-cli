from setuptools import setup, find_packages

setup(
    name='toma',
    author="Xiaozhe Yao",
    author_email="askxzyao@gmail.com",
    description="Toma Cluster Manager",
    version='0.0.1',
    scripts=["toma_starter/bin/toma"],
    package_dir={'toma_starter': 'toma_starter'},
    packages=find_packages(),
    install_requires=[
        "typer",
        "jsonrpc-websocket",
        "netifaces",
        "pynvml",
        "py3nvml",
        "requests",
    ]
)