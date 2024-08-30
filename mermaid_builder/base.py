import json
from dataclasses import dataclass

from mermaid_builder.utils import get_mermaid_live_url

INTENT_CHAR = '    '


class Color:
    GREEN = "#789E3E"
    BLUE = "#2873BA"
    YELLOW = "#DAA840"
    ORANGE = "#E07941"
    PURPLE = "#800080"
    RED = "#E38A8A"
    CYAN = "#E0FFFF"
    MAGENTA = "#F57DF5"
    WHITE = "#FFFFFF"
    BLACK = "#000000"

    @staticmethod
    def hex_to_rgb(hex_value):
        hex_value = hex_value.lstrip('#')
        rgb = tuple(int(hex_value[i:i+2], 16) for i in (0, 2, 4))
        return f"rgb{rgb}"


class Icon:
    USER = "fa:fa-user"
    DATABASE = "fa:fa-database"
    SERVER = "fa:fa-server"
    STREAM = "fa:fa-stream"
    FILE = "fa:fa-file"
    LOAD_BALANCER = "fa:fa-sitemap"
    SHIELD = "fa:fa-shield-alt"
    MOBILE = "fa:fa-mobile"
    LAPTOP = "fa:fa-laptop"


@dataclass
class Theme:
    name: str = "light"
    font_family: str = "Monospace"
    sequence_show_number: bool = False

    def draw(self):
        data = {
            "theme": self.name,
            "themeVariables": {
                "fontFamily": self.font_family,
            },
        }
        if self.sequence_show_number:
            data["sequence"] = {
                "showSequenceNumbers": self.sequence_show_number,
            }
        return json.dumps(data)


class BaseDiagram:
    def __init__(self, title: str, theme: Theme = None):
        if theme is None:
            self.theme = Theme()
        else:
            self.theme = theme
        self.title = title

    def draw(self):
        raise NotImplementedError

    def get_header_lines(self):
        return [
            "---",
            "title: " + self.title,
            "---",
            "%%{init: " + self.theme.draw() + "}%%",
        ]

    def save(self, file_path):
        with open(file_path, "w") as file:
            file.write(self.draw())

    def get_mermaid_live_url(self):
        return get_mermaid_live_url(self.draw())
