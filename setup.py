from setuptools import setup, find_packages

from __init__ import __version__

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    author='Jeff Wang',
    author_email='jeffwji@test.com',
    version=__version__,

    name="PandasProfileCustomization",

    packages=find_packages(
        exclude=['tests', '*.tests', '*.tests.*']
    ),

    package_data={
        '': ['*.md', '*.py'],
        'config': ['*.properties']
    },
    install_requires=requirements,
)
