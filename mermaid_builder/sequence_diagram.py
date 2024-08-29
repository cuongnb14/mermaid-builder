from .base import INTENT_CHAR, BaseDiagram


class Arrow:
    SYNC = "->>"
    ASYNC = "-)"
    RETURN = "--)"


class SequenceDiagram(BaseDiagram):
    def __init__(self, title, theme=None):
        super().__init__(title, theme)
        self.records = []
        self.participants = []
        self.actors = []

    def draw(self):
        result = self.get_header_lines()
        result += ["sequenceDiagram"]
        for participant in self.participants:
            if participant.is_actor:
                result.append(f"{INTENT_CHAR}actor {participant.name}")
            else:
                result.append(f"{INTENT_CHAR}participant {participant.name}")
        result.extend([f"{INTENT_CHAR}{x}" for x in self.records])
        return "\n".join(result)


class Participant:
    def __init__(self, sequence_diagram, name, is_actor=False):
        self.sequence_diagram = sequence_diagram
        self.name = name
        self.is_actor = is_actor
        self.sequence_diagram.participants.append(self)

    def sync_message(self, to, message):
        self.sequence_diagram.records.append(f"{self.name}{Arrow.SYNC}{to.name}:{message}")

    def async_message(self, to, message):
        self.sequence_diagram.records.append(f"{self.name}{Arrow.ASYNC}{to.name}:{message}")

    def return_message(self, to, message):
        self.sequence_diagram.records.append(f"{self.name}{Arrow.RETURN}{to.name}:{message}")
