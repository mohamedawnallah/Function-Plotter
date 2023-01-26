import pytest
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from function_plotter import FunctionPlotter
import os

@pytest.fixture
def function_plotter(qtbot):
    plotter = FunctionPlotter()
    qtbot.addWidget(plotter)
    return plotter

def test_init_variables(function_plotter: FunctionPlotter):
    """Test the initialization of the variables"""
    assert function_plotter.ax is None, "The ax attribute should be None"
    assert function_plotter.grid_visible == False, "The grid_visible attribute should be False"
    assert function_plotter.legend_visible == False, "The legend_visible attribute should be False"

@pytest.mark.qt
def test_create_widgets(function_plotter: FunctionPlotter):
    """Test the creation of the widgets"""
    assert function_plotter.scroll_area is not None, "The scroll area should not be None"
    assert function_plotter.function_label is not None, "The function label should not be None"
    assert function_plotter.function_input is not None, "The function input should not be None"
    assert function_plotter.xmin_label is not None, "The xmin label should not be None"
    assert function_plotter.xmin_input is not None, "The xmin input should not be None"
    assert function_plotter.xmax_label is not None, "The xmax label should not be None"
    assert function_plotter.xmax_input is not None, "The xmax input should not be None"
    assert function_plotter.plot_button is not None, "The plot button should not be None"
    assert function_plotter.zoom_in_button is not None, "The zoom in button should not be None"
    assert function_plotter.zoom_out_button is not None, "The zoom out button should not be None"
    assert function_plotter.reset_button is not None, "The reset button should not be None"
    assert function_plotter.save_image_button is not None, "The save image button should not be None"
    assert function_plotter.derivative_button is not None, "The derivative button should not be None"
    assert function_plotter.integral_button is not None, "The integral button should not be None"
    assert function_plotter.change_color_button is not None, "The change color button should not be None"
    assert function_plotter.toggle_grid_button is not None, "The toggle grid button should not be None"
    assert function_plotter.toggle_legend_button is not None, "The toggle legend button should not be None"
    assert function_plotter.add_function_button is not None, "The add function button should not be None"
    assert function_plotter.x_label_button is not None, "The x label button should not be None"
    assert function_plotter.y_label_button is not None, "The y label button should not be None"
    assert function_plotter.title_button is not None, "The title button should not be None"
    assert function_plotter.cursor_label is not None, "The cursor label should not be None"
    assert function_plotter.figure is not None, "The figure should not be None"
    assert function_plotter.canvas is not None, "The canvas should not be None"
    assert function_plotter.canvas.minimumSize().width() == 800, "The canvas minimum width should be 800"
    assert function_plotter.canvas.minimumSize().height() == 420, "The canvas minimum height should be 420"

@pytest.mark.qt
def test_create_layout(function_plotter: FunctionPlotter):
    """Test the creation of the layout"""
    assert function_plotter.layout is not None, "The layout should not be None"
    assert function_plotter.layout.count() == 22, "The layout should have 22 widgets"

@pytest.mark.qt
def test_connect_signals(function_plotter: FunctionPlotter):
    """Test the connection of the signals"""
    assert function_plotter.plot_button.clicked is not None, "The plot button should have a clicked signal"
    assert function_plotter.zoom_in_button.clicked is not None, "The zoom in button should have a clicked signal"
    assert function_plotter.zoom_out_button.clicked is not None, "The zoom out button should have a clicked signal"
    assert function_plotter.reset_button.clicked is not None, "The reset button should have a clicked signal"
    assert function_plotter.save_image_button.clicked is not None, "The save image button should have a clicked signal"
    assert function_plotter.derivative_button.clicked is not None, "The derivative button should have a clicked signal"
    assert function_plotter.integral_button.clicked is not None, "The integral button should have a clicked signal"
    assert function_plotter.change_color_button.clicked is not None, "The change color button should have a clicked signal"
    assert function_plotter.toggle_grid_button.clicked is not None, "The toggle grid button should have a clicked signal"
    assert function_plotter.toggle_legend_button.clicked is not None, "The toggle legend button should have a clicked signal"
    assert function_plotter.add_function_button.clicked is not None, "The add function button should have a clicked signal"
    assert function_plotter.x_label_button.clicked is not None, "The x label button should have a clicked signal"
    assert function_plotter.y_label_button.clicked is not None, "The y label button should have a clicked signal"
    assert function_plotter.title_button.clicked is not None, "The title button should have a clicked signal"
    assert function_plotter.canvas.mpl_connect is not None, "The canvas should have a mpl_connect signal"

@pytest.mark.qt
def test_plot(qtbot, function_plotter: FunctionPlotter):
    """Test the plotting journey of the function plotter"""
    function_input = "x^2"
    xmin_input, xmax_input = "1", "10"
    qtbot.keyClicks(function_plotter.function_input, function_input)
    qtbot.keyClicks(function_plotter.xmin_input, xmin_input)
    qtbot.keyClicks(function_plotter.xmax_input, xmax_input)
    function_plotter.plot()
    x, y = function_plotter.figure.gca().lines[0].get_data()
    assert x[0] == 1 and y[-1] == 100, "The plotted function is not as expected."


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
