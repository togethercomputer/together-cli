from setuptools import setup, find_packages

setup(
    name='together_node',
    author="Xiaozhe Yao",
    author_email="askxzyao@gmail.com",
    description="Together Node is a tool to help you join together computer",
    version='0.0.40',
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