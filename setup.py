from setuptools import setup

setup(
    name="BingSearch",
    version="1.2.0",
    py_modules=["bingsearch"],
    install_requires=[
        "questionary",
        "tqdm"
    ],
    entry_points="""
        [console_scripts]
        bingsearch=bingsearch:menu
    """,
)