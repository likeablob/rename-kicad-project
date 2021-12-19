from rich.console import Console
from rich.theme import Theme
from enum import Enum


class LogLevel(str, Enum):
    INFO = "info"
    WARNING = "warning"
    DANGER = "danger"


custom_theme = Theme(
    {
        LogLevel.INFO: "dim cyan",
        LogLevel.WARNING: "magenta",
        LogLevel.DANGER: "bold red",
    }
)


logger = Console(theme=custom_theme)
