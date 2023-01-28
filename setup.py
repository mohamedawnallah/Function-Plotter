from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

with open("app/requirements.txt", "r") as f:
    install_requirements = f.read().splitlines()

NAME='function_plotter'
VERSION = '0.3'
AUTHOR = 'Mohamed Awnallah'
EMAIL = "mohamedmohey2352@gmail.com"
DESCRIPTION = 'Discover the power of function plotting with Function Plotter'

# Setting up
setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(exclude=['tests', 'tests.*',"logs","logs.*",".gitignore"]),
    install_requires=install_requirements,
    keywords=['python', 'function', 'plotting', 'function plotter', 'visualization', 'gui'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)

