from dataclasses import dataclass

from .base import INTENT_CHAR, Theme, BaseDiagram


class Direction:
    LR = 'LR'
    TB = 'TB'


class NodeShape:
    RECTANGLE = "rect"
    ROUNDED_RECTANGLE = "rounded"
    STADIUM = "stadium"
    FRAMED_RECTANGLE = "fr-rect"
    CYLINDER = "cyl"
    CIRCLE = "circle"
    ODD = "odd"
    DIAMOND = "diam"
    HEXAGON = "hex"
    LEAN_RIGHT = "lean-r"
    LEAN_LEFT = "lean-l"
    TRAPEZOID_BASE_BOTTOM = "trap-b"
    TRAPEZOID_BASE_TOP = "trap-t"
    DOUBLE_CIRCLE = "dbl-circ"
    TEXT_BLOCK = "text"
    NOTCHED_RECTANGLE = "notch-rect"
    LINED_RECTANGLE = "lin-rect"
    SMALL_CIRCLE = "sm-circ"
    FRAMED_CIRCLE = "fr-circ"
    FILLED_RECTANGLE = "fork"
    HOURGLASS = "hourglass"
    CURLY_BRACE = "brace"
    CURLY_BRACE_RIGHT = "brace-r"
    CURLY_BRACES = "braces"
    LIGHTNING_BOLT = "bolt"
    DOCUMENT = "doc"
    HALF_ROUNDED_RECTANGLE = "delay"
    HORIZONTAL_CYLINDER = "h-cyl"
    LINED_CYLINDER = "lin-cyl"
    CURVED_TRAPEZOID = "curv-trap"
    DIVIDED_RECTANGLE = "div-rect"
    TRIANGLE = "tri"
    WINDOW_PANE = "win-pane"
    FILLED_CIRCLE = "f-circ"
    LINED_DOCUMENT = "lin-doc"
    TRAPEZOIDAL_PENTAGON = "notch-pent"
    FLIPPED_TRIANGLE = "flip-tri"
    SLOPED_RECTANGLE = "sl-rect"
    STACKED_DOCUMENT = "docs"
    STACKED_RECTANGLE = "st-rect"
    FLAG = "flag"
    BOW_TIE_RECTANGLE = "bow-rect"
    CROSSED_CIRCLE = "cross-circ"
    TAGGED_DOCUMENT = "tag-doc"
    TAGGED_RECTANGLE = "tag-rect"


class LinkShape:
    ARROW_HEAD = "-->"
    OPEN = "---"
    DOTTED = "-.-"
    DOTTED_ARROW = "-.->"
    THICK = "==>"


@dataclass
class Node:
    name: str
    shape: NodeShape
    connections: list = ()
    class_name: str = ""
    icon: str = ""

    def get_id(self) -> str:
        return self.name.lower().replace(" ", "_")

    def add_connection(self, next_node, link):
        if not self.connections:
            self.connections = []

        self.connections.append(Connection(link=link, next_node=next_node))

    def add_connections(self, link, *nodes):
        for node in nodes:
            self.add_connection(next_node=node, link=link)

    def draw_node(self):
        if self.icon:
            text = f"{self.icon} {self.name}"
        else:
            text = self.name

        if self.class_name:
            result = f"{self.get_id()}:::{self.class_name}@"
        else:
            result = f"{self.get_id()}@"
        result += "{" + f'shape: {self.shape}, label: "{text}"' + '}'

        return result

    def get_lines(self, indent=0):
        result = []
        for connection in self.connections:
            result.append(
                f"{indent * INTENT_CHAR}{self.draw_node()}{connection.link.draw()}{connection.next_node.draw_node()}"
            )
        return result


@dataclass
class Link:
    shape = LinkShape.ARROW_HEAD
    text: str = ''
    length: int = 1

    def get_shape(self):
        if self.length == 1:
            return self.shape
        if self.shape == LinkShape.DOTTED:
            return f"-{'.' * self.length}-"
        if self.shape == LinkShape.DOTTED_ARROW:
            return f"-{'.' * self.length}->"

        return f"{self.shape[0] * (self.length - 1)}{self.shape}"

    def draw(self):
        if self.text:
            return f"{self.get_shape()} |{self.text}|"
        return f"{self.get_shape()}"


@dataclass
class Connection:
    link: Link
    next_node: Node


class Subgraph:
    def __init__(self, name, direction=Direction.TB):
        self.name = name
        self.direction = direction
        self.nodes = []
        self.connections = []

    def add_connections(self, link, *nodes):
        for node in nodes:
            self.add_connection(next_node=node, link=link)

    def add_connection(self, next_node, link):
        if not self.connections:
            self.connections = []

        self.connections.append(Connection(link=link, next_node=next_node))

    def get_id(self) -> str:
        return self.name.lower().replace(" ", "_")

    def add_nodes(self, *nodes):
        self.nodes.extend(nodes)

    def draw_node(self):
        return self.get_id()

    def get_lines(self, indent=0):
        result = [
            f"{INTENT_CHAR * indent}style {self.get_id()} rx:10,ry:10",
            f"{INTENT_CHAR * indent}subgraph {self.get_id()} [{self.name}]",
            f"{INTENT_CHAR * (indent + 1)}direction {self.direction}",
        ]
        for node in self.nodes:
            if isinstance(node, Subgraph):
                result.extend(node.get_lines(indent + 1))
            else:
                result.append(f"{INTENT_CHAR * (indent + 1)}{node.draw_node()}")
        result.append(f"{INTENT_CHAR * indent}end")

        for connection in self.connections:
            result.append(
                f"{indent * INTENT_CHAR}{self.draw_node()}{connection.link.draw()}{connection.next_node.draw_node()}"
            )
        return result


@dataclass
class Style:
    class_name: str
    fill: str
    color: str

    def draw(self):
        return f"classDef {self.class_name} fill:{self.fill},color:{self.color}"


class Flowchart(BaseDiagram):
    def __init__(self, title, theme: Theme = None, direction=Direction.LR):
        super().__init__(title, theme)
        self.direction = direction
        self.items = []
        self.styles = []

    def add_styles(self, *items):
        self.styles.extend(items)

    def add_items(self, *items):
        self.items.extend(items)

    def draw(self):
        result = [
            *self.get_header_lines(),
            f"flowchart {self.direction}",
        ]

        for item in self.items:
            result.extend(item.get_lines(indent=1))

        for style in self.styles:
            result.append(style.draw())

        return "\n".join(result)
