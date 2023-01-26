from PySide6.QtWidgets import QMessageBox
from PySide6.QtTest import QTest
from utils.widgets import CustomMessageBox

def test_custom_message_box(custom_message_box):
    """Test the CustomMessageBox class."""
    assert custom_message_box.timeout == 0
    assert custom_message_box.autoclose == False
    assert custom_message_box.currentTime == 0

def test_custom_message_box_showEvent(custom_message_box):
    """Test the showEvent method."""
    custom_message_box.showEvent(None)
    assert custom_message_box.currentTime == 0
    assert custom_message_box.autoclose == False
    
def test_custom_message_box_timerEvent(custom_message_box):
    """Test the timerEvent method."""
    custom_message_box.timerEvent(None)
    assert custom_message_box.currentTime == 1
    assert custom_message_box.autoclose == False
    
def test_custom_message_box_showWithTimeout():
    """Test the showWithTimeout method."""
    timeout_seconds = 1
    title = "Test Title"
    message = "Test Message"
    icon = QMessageBox.Information
    buttons = QMessageBox.Ok
    CustomMessageBox.showWithTimeout(timeout_seconds, title, message, icon, buttons)
    QTest.qWait(timeout_seconds * 1000 + 100)
    assert True