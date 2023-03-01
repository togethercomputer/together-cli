from setuptools import setup, find_packages

setup(
    name='together_cli',
    author="togethercomputer",
    author_email="support@together.xyz",
    description="Together cli is a tool to help you join together computer",
    version='0.0.84',
    scripts=["together_cli/bin/together-cli"],
    package_dir={'together_cli': 'together_cli'},
    packages=find_packages(),
    install_requires=[
        "typer",
        "requests",
        "rich",
        "loguru",
        "huggingface-hub",
        "pynvml"
    ]
)