<h1 align="center">
  <img alt="cgapp logo" src="assets/function_plotter_logo.png" width="224px"/><br/>
  Function Plotter
</h1>
<p align="center">Discover the power of function plotting with <b>Function Plotter</b> on GitHub.<br/></br>The ultimate tool for visualizing mathematical functions on Github!</p>

# About
Function Plotter is a powerful tool for visualizing mathematical functions on Github. With this app, you can easily plot and analyze a wide variety of functions, including polynomials, trigonometric functions, and more.

## Features
- Plot any mathematical function with just a few clicks 📊
- Customize plot settings, including color and line width 🎨
- Zoom and pan for detailed analysis 🔍
- Save and share plots with others 💾
- and more!

## Screenshots

## Video Recording

## ⚡️ Quick start

First, install python requirements by using the following command:
```bash
pip3 install -r requirements.txt
```

Next, run the GUI application using the the following commands:
```bash
cd app
python3 main.py
```

That's all you need to know to start! 🎉

## 📖 Examples
Here are a few examples of the types of functions you can plot with Function Plotter:
- Polynomial functions (e.g. `x^2 + 2*x + 1`)
- Trigonometric functions (e.g. `sin(x)`)
- Logarithmic functions (e.g. `log(x)`)

## Project Hierachy

    .
    ├── app                      # Application source code
    ├── assets                   # Assets for the readme file
    ├── requirements.txt         # requirements for third party python libraries 
    ├── .gitignore
    └── README.md

## App Source Code
    .
    ├── ...
    ├── app                      # Documentation files (alternatively `doc`)
    │   ├── figures              # Generated figures by the app
    │   ├── logs                 # Generated logs by the app
    │   ├── tests                # Automated tests for the app
    │   ├── utils                # reusable utilities by the app components
    │   ├── function_plotter     # the main class for the app
    └── ├── main                 # the main entry point for the app

## Tests
To run the tests for the app, navigate to the project root and run the command `pytest`. This will run all the tests in the `app/tests/` directory.

## Licensing
Function Plotter is released under the MIT license. Please see the LICENSE file for more information.
