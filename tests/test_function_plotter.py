import pytest
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from unittest.mock import MagicMock

from function_plotter import FunctionPlotter
import os


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
