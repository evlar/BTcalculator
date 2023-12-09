from setuptools import setup

APP = ['BTcalculator.py']  # Replace with your script's filename
DATA_FILES = []  # Any additional files
OPTIONS = {
    'argv_emulation': True,
    'packages': ['requests', 'tkinter'],  # Required packages
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
