from setuptools import setup

setup(
    name="BingSearchTool",
    version="1.0",
    py_modules=["client"],
    install_requires=[
        "click",
        "PyInquirer"
    ],
    entry_points="""
        [console_scripts]
        bingsearch=client:main
    """,
)