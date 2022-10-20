from setuptools import setup

setup(
    name='download',
    version='1.0',
    py_modules=['download'],
    install_requires=[
        'click',
        'python-twitter',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        download=download:main
    ''',
)
