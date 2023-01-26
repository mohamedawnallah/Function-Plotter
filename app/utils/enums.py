from enum import Enum

class MessageType(Enum):
    """Enum for message types."""
    ERROR = 1
    WARNING = 2
    INFORMATION = 3