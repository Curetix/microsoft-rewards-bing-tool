from setuptools import setup

setup(
    name="BingSearch",
    version="1.1",
    py_modules=["bingsearch"],
    install_requires=[
        "click",
        "PyInquirer"
    ],
    entry_points="""
        [console_scripts]
        bingsearch=bingsearch:cli
    """,
)