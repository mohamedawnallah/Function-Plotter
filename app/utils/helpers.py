import sympy
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMessageBox
from loguru import logger
import re
from utils.widgets import CustomMessageBox
from utils.enums import MessageType
from utils.exceptions import ValidationError

LOGGING_FILE_PATH = "logs/debug.log"
logger.add(LOGGING_FILE_PATH)

def parse_function_string(function_string: str) -> sympy:
    validate_function(function_string)
    normalized_function: str = normalize_function(function_string)
    function_parsed = parse_function_string_to_sympy(normalized_function)
    return function_parsed
    
def validate_function(function_string: str) -> bool:
    if not function_string:
        raise ValidationError("function is empty")

def normalize_function(function_string: str) -> bool:
    function_string = function_string.replace(" ", "")
    function_string = function_string.replace("^", "**")
    return function_string

def parse_function_string_to_sympy(function_string: str) -> sympy.core:
    try:
        function_string_parsed = sympy.parse_expr(function_string)
    except SyntaxError:
        raise ValidationError("function is not valid")
    return function_string_parsed
    
def get_x_range(xmin_input: str, xmax_input: str) -> tuple[float, float]:
    try:
        xmin = float(xmin_input)
        xmax = float(xmax_input)
        if xmin >= xmax:
            raise ValidationError("xmin must be less than xmax.")
        return xmin, xmax
    except (ValueError, TypeError) as error:
        validation_error_message = "Please enter a valid number for the minimum and maximum values of x." + "-" + str(error)
        raise ValidationError(validation_error_message)
        
def get_xy_data(function_parsed: sympy.core, xmin: float, xmax: float):
    x = sympy.Symbol("x")
    x_data = [xmin + (xmax - xmin) * i / 100 for i in range(101)]
    y_data = [function_parsed.subs(x, xi).evalf() for xi in x_data]
    return x_data, y_data


def show_message(timeout_seconds: float, title: str, message: str, message_type: MessageType) -> None:
    user_message = message.split("-")[0]
    if message_type == MessageType.ERROR:
        logger.error(message)
        CustomMessageBox.showWithTimeout(timeout_seconds=timeout_seconds, title=title, message=user_message, icon=QMessageBox.Warning)
    elif message_type == MessageType.WARNING:
        logger.warning(message)
        CustomMessageBox.showWithTimeout(timeout_seconds=timeout_seconds, title=title, message=user_message, icon=QMessageBox.Warning)
    elif message_type == MessageType.INFORMATION:
        logger.info(message)
        CustomMessageBox.showWithTimeout(timeout_seconds=timeout_seconds, title=title, message=user_message, icon=QMessageBox.Information)
