from PySide6.QtWidgets import QMessageBox
from PySide6.QtTest import QTest

import pytest
from utils.widgets import CustomMessageBox

@pytest.fixture
def custom_message_box(qtbot):
    w = CustomMessageBox()
    qtbot.addWidget(w)
    return w

def test_custom_message_box(custom_message_box):
    assert custom_message_box.timeout == 0
    assert custom_message_box.autoclose == False
    assert custom_message_box.currentTime == 0

def test_custom_message_box_showEvent(custom_message_box):
    custom_message_box.showEvent(None)
    assert custom_message_box.currentTime == 0
    assert custom_message_box.autoclose == False
    
def test_custom_message_box_timerEvent(custom_message_box):
    custom_message_box.timerEvent(None)
    assert custom_message_box.currentTime == 1
    assert custom_message_box.autoclose == False
    
def test_custom_message_box_showWithTimeout():
    timeout_seconds = 1
    title = "Test Title"
    message = "Test Message"
    icon = QMessageBox.Information
    buttons = QMessageBox.Ok
    CustomMessageBox.showWithTimeout(timeout_seconds, title, message, icon, buttons)
    QTest.qWait(timeout_seconds * 1000 + 100)
    assert True