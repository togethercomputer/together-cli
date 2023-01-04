from setuptools import setup, find_packages

setup(
    name='together_node',
    author="Xiaozhe Yao",
    author_email="askxzyao@gmail.com",
    description="Toma Cluster Manager",
    version='0.0.3',
    scripts=["together_node/bin/together_node"],
    package_dir={'together_node': 'together_node'},
    packages=find_packages(),
    install_requires=[
        "typer",
        "requests",
        "rich",
        "loguru",

    ]
)