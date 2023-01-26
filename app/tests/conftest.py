import pytest
from function_plotter import FunctionPlotter
from utils.widgets import CustomMessageBox
@pytest.fixture
def function_plotter(qtbot):
    plotter = FunctionPlotter()
    qtbot.addWidget(plotter)
    return plotter

@pytest.fixture
def custom_message_box(qtbot):
    w = CustomMessageBox()
    qtbot.addWidget(w)
    return w