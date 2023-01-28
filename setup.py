from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    install_requires = f.read().splitlines()

setup(
    name='function_plotter',
    version='0.1',
    packages=find_packages(where='app', include=["app.*"], exclude=['tests']),
    package_dir={'app': 'app'},
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'function_plotter=app.main:main',
        ],
    },
)