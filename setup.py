from setuptools import setup

APP = [{
    'script':'menubar.py',
    'name':'Maturita',
    'version':'1.0.0',
}]
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
    },
    'packages': ['rumps'],
    'iconfile':'icon.icns',
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)