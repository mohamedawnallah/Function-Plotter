import pytest
import sympy
from PySide6.QtWidgets import QMessageBox
from utils.exceptions import ValidationError
from utils.enums import MessageType
from unittest import mock
from utils import helpers
def test_parse_function_string():
    function_string = "x^2+3*x-1"
    parsed_function = helpers.parse_function_string(function_string)
    assert parsed_function == sympy.parse_expr(function_string.replace("^", "**"))

def test_empty_parse_function_string():
    function_string = ""
    with pytest.raises(ValidationError, match="function is empty"):
        helpers.parse_function_string(function_string)
        
def test_validate_function():
    function_string = ""
    with pytest.raises(ValidationError, match="function is empty"):
        helpers.validate_function(function_string)

def test_normalize_function():
    function_string = "x^2+3*x-1"
    assert helpers.normalize_function(function_string) == "x**2+3*x-1"

def test_parse_function_string_to_sympy():
    function_string = helpers.normalize_function("x^2+3*x-1")
    parsed_function = helpers.parse_function_string_to_sympy(function_string)
    assert parsed_function == sympy.parse_expr(function_string)

    function_string = "invalid function"
    with pytest.raises(ValidationError, match="function is not valid"):
        helpers.parse_function_string_to_sympy(function_string)
        
def test_get_x_range():
    xmin_input = "0"
    xmax_input = "10"
    xmin, xmax = helpers.get_x_range(xmin_input, xmax_input)
    assert xmin == 0 and xmax == 10
    
    xmin_input = "10"
    xmax_input = "0"
    with pytest.raises(ValidationError, match="xmin must be less than xmax."):
        helpers.get_x_range(xmin_input, xmax_input)

    xmin_input = "invalid input"
    xmax_input = "10"
    with pytest.raises(ValidationError, match="Please enter a valid number for the minimum and maximum values of x."):
        helpers.get_x_range(xmin_input, xmax_input)

def test_get_xy_data():
    function_string = helpers.normalize_function("x^2+3*x-1")
    function_parsed = sympy.parse_expr(function_string)
    xmin = 0
    xmax = 10
    x_data, y_data = helpers.get_xy_data(function_parsed, xmin, xmax)
    assert len(x_data) == 101
    assert len(y_data) == 101

def test_show_message():
    timeout_seconds = 2
    title = "Test"
    message = "Test message"
    message_type = MessageType.INFORMATION

    with mock.patch("utils.widgets.CustomMessageBox.showWithTimeout") as mock_show_with_timeout:
        helpers.show_message(timeout_seconds, title, message, message_type)
        mock_show_with_timeout.assert_called_once_with(timeout_seconds=timeout_seconds, title=title, message=message, icon=QMessageBox.Information)
