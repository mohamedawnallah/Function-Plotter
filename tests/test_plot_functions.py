import pytest
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from unittest.mock import MagicMock

from function_plotter import FunctionPlotter
import os

@pytest.mark.qt
def test_on_press_canvas(qtbot, function_plotter: FunctionPlotter):
    """Test the on_press function of the function plotter"""
    function_input = "x^2"
    xmin_input, xmax_input = "1", "10"
    qtbot.keyClicks(function_plotter.function_input, function_input)
    qtbot.keyClicks(function_plotter.xmin_input, xmin_input)
    qtbot.keyClicks(function_plotter.xmax_input, xmax_input)
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    event = MagicMock()
    event.inaxes = function_plotter.ax
    event.xdata, event.ydata = 2, 4
    function_plotter.on_press_canvas(event)
    assert function_plotter.press == (2, 4), "on_press function did not set press attribute correctly"

@pytest.mark.qt
def test_on_release_canvas(qtbot, function_plotter: FunctionPlotter):
    function_input = "x^2"
    xmin_input, xmax_input = "1", "10"
    qtbot.keyClicks(function_plotter.function_input, function_input)
    qtbot.keyClicks(function_plotter.xmin_input, xmin_input)
    qtbot.keyClicks(function_plotter.xmax_input, xmax_input)
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    event = MagicMock()
    event.inaxes = function_plotter.ax
    event.xdata, event.ydata = (1, 2)
    function_plotter.on_press_canvas(event)
    function_plotter.on_release_canvas(event)
    xlim = function_plotter.ax.get_xlim()
    ylim = function_plotter.ax.get_ylim()
    assert xlim == (0.55, 10.45), "on_release function did not set xlim correctly"
    assert ylim == (-3.95, 104.95), "on_release function did not set ylim correctly"
    
@pytest.mark.qt
def test_on_motion_canvas(qtbot, function_plotter: FunctionPlotter):
    function_input = "x^2"
    xmin_input, xmax_input = "1", "10"
    qtbot.keyClicks(function_plotter.function_input, function_input)
    qtbot.keyClicks(function_plotter.xmin_input, xmin_input)
    qtbot.keyClicks(function_plotter.xmax_input, xmax_input)
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    event = MagicMock()
    event.inaxes = function_plotter.ax
    event.xdata, event.ydata = (1, 2)
    function_plotter.on_press_canvas(event)
    function_plotter.on_motion_canvas(event)
    assert function_plotter.cursor_label.text() == "x: 1, y: 2", "The cursor label text is not as expected"


@pytest.mark.qt
@pytest.mark.parametrize("function_input, xmin_input, xmax_input, expected_x, expected_y", [
    ("x^2", "1", "10", 1, 100),
    ("sin(x)", "-1", "1", -1, 0),
    ("log(x)", "0.1", "10", 0.1, 1),
    ("1/x", "1", "10", 1, 0.1),
    ("5*x^3 + 2*x", "1", "10", 1, 7),
])
def test_plot_valid_functions(qtbot, function_plotter: FunctionPlotter, function_input, xmin_input, xmax_input, expected_x, expected_y):
    """Test the plotting journey of the function plotter"""
    qtbot.keyClicks(function_plotter.function_input, function_input)
    qtbot.keyClicks(function_plotter.xmin_input, xmin_input)
    qtbot.keyClicks(function_plotter.xmax_input, xmax_input)
    function_plotter.plot()
    x, y = function_plotter.figure.gca().lines[0].get_data()
    x_found, y_found = int(x[0]), int(y[-1])
    assert x_found == expected_x and y_found == expected_y, "The plotted function is not as expected."


@pytest.mark.qt
def test_changing_title(qtbot, function_plotter: FunctionPlotter):
    """Test the changing of the title of the function plotter"""
    function_input = "x^2"
    xmin_input, xmax_input = "1", "10"
    title_input_text = "test title"
    qtbot.keyClicks(function_plotter.function_input, function_input)
    qtbot.keyClicks(function_plotter.xmin_input, xmin_input)
    qtbot.keyClicks(function_plotter.xmax_input, xmax_input)
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    function_plotter.ax.set_title(title_input_text)
    assert (
        function_plotter.ax.get_title() == title_input_text
    ), "The title of the plot is not as expected."


@pytest.mark.qt
def test_change_xaxis_label(qtbot, function_plotter: FunctionPlotter):
    """Test the changing of the x-axis label of the function plotter"""
    function_input = "x^2"
    xmin_input, xmax_input = "1", "10"
    xaxis_label, submitted_ok  = "test x-axis", True
    qtbot.keyClicks(function_plotter.function_input, function_input)
    qtbot.keyClicks(function_plotter.xmin_input, xmin_input)
    qtbot.keyClicks(function_plotter.xmax_input, xmax_input)
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    function_plotter.change_x_label(label=xaxis_label, ok=submitted_ok)
    assert (
        function_plotter.ax.get_xlabel() == xaxis_label
    ), "The x-axis label of the plot is not as expected."


@pytest.mark.qt
def test_change_yaxis_label(qtbot, function_plotter: FunctionPlotter):
    """Test the changing of the y-axis label of the function plotter"""
    function_input = "x^2"
    xmin_input, xmax_input = "1", "10"
    yaxis_label, submitted_ok = "test y-axis", True
    qtbot.keyClicks(function_plotter.function_input, function_input)
    qtbot.keyClicks(function_plotter.xmin_input, xmin_input)
    qtbot.keyClicks(function_plotter.xmax_input, xmax_input)
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    function_plotter.change_y_label(label=yaxis_label, ok=submitted_ok)
    assert (
        function_plotter.ax.get_ylabel() == yaxis_label
    ), "The y-axis label of the plot is not as expected."


@pytest.mark.qt
def test_zoom_in(qtbot, function_plotter: FunctionPlotter):
    """Test the zooming of the function plotter"""
    function_input = "x^2"
    xmin_input, xmax_input = "1", "10"
    qtbot.keyClicks(function_plotter.function_input, function_input)
    qtbot.keyClicks(function_plotter.xmin_input, xmin_input)
    qtbot.keyClicks(function_plotter.xmax_input, xmax_input)
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    xlim_before = function_plotter.ax.get_xlim()
    ylim_before = function_plotter.ax.get_ylim()
    function_plotter.zoom_in()
    xlim_after = function_plotter.ax.get_xlim()
    ylim_after = function_plotter.ax.get_ylim()
    assert (
        (xlim_after[0] == xlim_before[0] * 0.9)
        and (xlim_after[1] == xlim_before[1] * 0.9)
        and (ylim_after[0] == ylim_before[0] * 0.9)
        and (ylim_after[1] == ylim_before[1] * 0.9)
    ), "Zooming in did not work as expected"


@pytest.mark.qt
def test_zoom_out(qtbot, function_plotter: FunctionPlotter):
    """Test the zooming of the function plotter"""
    function_input = "x^2"
    xmin_input, xmax_input = "1", "10"
    qtbot.keyClicks(function_plotter.function_input, function_input)
    qtbot.keyClicks(function_plotter.xmin_input, xmin_input)
    qtbot.keyClicks(function_plotter.xmax_input, xmax_input)
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    xlim_before = function_plotter.ax.get_xlim()
    ylim_before = function_plotter.ax.get_ylim()
    function_plotter.zoom_out()
    xlim_after = function_plotter.ax.get_xlim()
    ylim_after = function_plotter.ax.get_ylim()
    assert (
        (xlim_after[0] == xlim_before[0] * 1.1)
        and (xlim_after[1] == xlim_before[1] * 1.1)
        and (ylim_after[0] == ylim_before[0] * 1.1)
        and (ylim_after[1] == ylim_before[1] * 1.1)
    ), "Zooming out did not work as expected"


@pytest.mark.qt
def test_save_image(qtbot, function_plotter: FunctionPlotter):
    """Test the saving of the image of the function plotter"""
    function_input = "x^2"
    xmin_input, xmax_input = "1", "10"
    file_name = "function_plot.png"
    qtbot.keyClicks(function_plotter.function_input, function_input)
    qtbot.keyClicks(function_plotter.xmin_input, xmin_input)
    qtbot.keyClicks(function_plotter.xmax_input, xmax_input)
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    function_plotter.save_image(file_name)
    assert os.path.exists(file_name), "Saving the image did not work as expected."

def test_save_image_cleanup():
    """Test the cleanup of the image of the function plotter"""
    file_name = "function_plot.png"
    os.remove(file_name)
    assert not os.path.exists(
        file_name
    ), "Cleaning up the image did not work as expected."

@pytest.mark.qt
def test_get_derivative(qtbot, function_plotter: FunctionPlotter):
    """Test the getting of the derivative of the function plotter"""
    function_input = "x^2"
    xmin_input, xmax_input = "1", "10"
    qtbot.keyClicks(function_plotter.function_input, function_input)
    qtbot.keyClicks(function_plotter.xmin_input, xmin_input)
    qtbot.keyClicks(function_plotter.xmax_input, xmax_input)
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    derivative = function_plotter.get_derivative()
    assert derivative == "2*x", "Getting the derivative did not work as expected."

@pytest.mark.qt
def test_get_integral(qtbot, function_plotter: FunctionPlotter):
    """Test the getting of the integral of the function plotter"""
    function_input = "x^2"
    xmin_input, xmax_input = "1", "10"
    qtbot.keyClicks(function_plotter.function_input, function_input)
    qtbot.keyClicks(function_plotter.xmin_input, xmin_input)
    qtbot.keyClicks(function_plotter.xmax_input, xmax_input)
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    integral = function_plotter.get_integral()
    assert integral == "x**3/3 + C", "Getting the integral did not work as expected."

@pytest.mark.qt
def test_change_color(qtbot, function_plotter: FunctionPlotter):
    """Test the changing of the color of the function plotter"""
    function_input = "x^2"
    xmin_input, xmax_input = "1", "10"
    color = QColor.fromRgbF(1, 0.3, 0.5, 1)
    qtbot.keyClicks(function_plotter.function_input, function_input)
    qtbot.keyClicks(function_plotter.xmin_input, xmin_input)
    qtbot.keyClicks(function_plotter.xmax_input, xmax_input)
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    color_before = function_plotter.ax.get_lines()[0].get_color()
    function_plotter.change_color(color_input=color)
    color_after = function_plotter.ax.get_lines()[0].get_color()
    assert color_before != color_after, "Changing the color did not work as expected."

@pytest.mark.qt
def test_toggle_grid(qtbot, function_plotter: FunctionPlotter):
    """Test the toggling of the grid of the function plotter"""
    function_input = "x^2"
    xmin_input, xmax_input = "1", "10"
    qtbot.keyClicks(function_plotter.function_input, function_input)
    qtbot.keyClicks(function_plotter.xmin_input, xmin_input)
    qtbot.keyClicks(function_plotter.xmax_input, xmax_input)
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    function_plotter.toggle_grid()
    assert (
        function_plotter.grid_visible == True
    ), "Toggling the grid did not work as expected."


@pytest.mark.qt
def test_toggle_legend(qtbot, function_plotter: FunctionPlotter):
    """Test the toggling of the legend of the function plotter"""
    function_input = "x^2"
    xmin_input, xmax_input = "1", "10"
    qtbot.keyClicks(function_plotter.function_input, function_input)
    qtbot.keyClicks(function_plotter.xmin_input, xmin_input)
    qtbot.keyClicks(function_plotter.xmax_input, xmax_input)
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    function_plotter.toggle_legend()
    assert (
        function_plotter.legend_visible == True
    ), "Toggling the legend did not work as expected."


@pytest.mark.qt
def test_add_another_function(qtbot, function_plotter: FunctionPlotter):
    """Test the adding of another function to the function plotter"""
    function_input, another_function_input = "x", "-x"
    xmin_input, xmax_input = "1", "1000"
    qtbot.keyClicks(function_plotter.function_input, function_input)
    qtbot.keyClicks(function_plotter.xmin_input, xmin_input)
    qtbot.keyClicks(function_plotter.xmax_input, xmax_input)
    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)
    qtbot.keyClicks(function_plotter.function_input, another_function_input)
    function_plotter.add_another_function()
    assert (
        len(function_plotter.ax.get_lines()) == 2
    ), "Adding another function did not work as expected."
