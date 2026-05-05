THEME_COLOR = {
    "green": (50, 255, 55, 255),
    "red": (230, 41, 55, 255),
    "purple": (200, 122, 255, 255),
    "black": (0, 0, 0, 255),
    "brown": (127, 106, 79, 255),
    "orange": (255, 161, 0, 255),
    "maroon": (190, 33, 55, 255),
    "gold": (255, 203, 0, 255),
    "darkred": (139, 0, 0, 255),
    "violet": (135, 60, 190, 255),
    "crimson": (220, 20, 60, 255),
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
