THEME_COLOR = {
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "green": (0, 255, 0),
    "yellow": (255, 250, 200),
    "purple": (230, 20, 255),
}


def color(text: str | int | None, r: int, g: int, b: int) -> str:
    """
    Apply an RGB foreground color to the given text using ANSI escape codes.

    This function wraps the input text with ANSI codes to display it
    in the specified RGB color in the terminal.

    Args:
        text: The text (or value) to color. If not a string, it will be
        converted.
        r: Red component (0–255).
        g: Green component (0–255).
        b: Blue component (0–255).

    Returns:
        A string formatted with ANSI escape codes for colored output.
    """
    if isinstance(text, str):
        return f"\033[38;2;{r};{g};{b}m{text}\033[0m"
    return f"\033[38;2;{r};{g};{b}m{str(text)}\033[0m"


def bg_color(text: str | int, r: int, g: int, b: int) -> str:
    """
    Apply an RGB background color to the given text using ANSI escape codes.

    This function wraps the input text with ANSI codes to display it
    with the specified RGB background color in the terminal.

    Args:
        text: The text (or value) to display. If not a string, it will be
        converted.
        r: Red component (0–255).
        g: Green component (0–255).
        b: Blue component (0–255).

    Returns:
        A string formatted with ANSI escape codes for background-colored
        output.
    """
    if isinstance(text, str):
        return f"\033[48;2;{r};{g};{b}m{str(text)}\033[0m"
    return f"\033[48;2;{r};{g};{b}m{text}\033[0m"
