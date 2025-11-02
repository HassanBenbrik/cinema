from setuptools import setup, find_packages

setup(
    name="Cinema",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4",
        "requests",
        "Pillow"
    ],
    description="A GUI application to manage movies with Tkinter",
    author="Hassan Benbrik",
    python_requires='>=3.8',
)
