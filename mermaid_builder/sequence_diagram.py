from contextlib import contextmanager

from .base import INTENT_CHAR, BaseDiagram


class Arrow:
    SYNC = "->>"
    ASYNC = "-)"
    RETURN = "--)"


class State:
    ACTIVATE = "+"
    DEACTIVATE = "-"


class Fragment:
    LOOP = "loop"
    ALT = "alt"
    PARALLEL = "par"
    CRITICAL = "critical"
    BREAK = "break"
    BACKGROUND = "rect"
    OPTION = "opt"


class SequenceDiagram(BaseDiagram):
    def __init__(self, title, theme=None):
        super().__init__(title, theme)
        self.records = []
        self.participants = []
        self.actors = []
        self.intent_index = 1
        
    def add_record(self, record):
        self.records.append(self.intent_index * INTENT_CHAR + record)

    def draw(self):
        result = self.get_header_lines()
        result += ["sequenceDiagram"]
        for participant in self.participants:
            if participant.is_actor:
                result.append(f"{INTENT_CHAR}actor {participant.name}")
            else:
                result.append(f"{INTENT_CHAR}participant {participant.name}")
        result.extend(self.records)
        return "\n".join(result)

    def note_over(self, text, *participants):
        p = ", ".join([p.name for p in participants])
        self.add_record(f"Note over {p}: {text}")

    def fragment(self, fg_type, name):
        @contextmanager
        def loop_context_manager():
            self.add_record(f"{fg_type} {name}")
            self.intent_index += 1
            try:
                yield
            finally:
                self.intent_index -= 1
                self.add_record(f"end")

        return loop_context_manager()

    def fm_else(self, name=""):
        self.add_record(f"else {name}")

    def fm_and(self, name):
        self.add_record(f"and {name}")

    def fm_option(self, name):
        self.add_record(f"option {name}")


class Participant:
    def __init__(self, sequence_diagram, name, is_actor=False):
        self.sequence_diagram = sequence_diagram
        self.name = name
        self.is_actor = is_actor
        self.sequence_diagram.participants.append(self)

    def sync_message(self, to, message, state=''):
        self.sequence_diagram.add_record(f"{self.name}{Arrow.SYNC}{state}{to.name}:{message}")

    def async_message(self, to, message, state=''):
        self.sequence_diagram.add_record(f"{self.name}{Arrow.ASYNC}{state}{to.name}:{message}")

    def return_message(self, to, message, state=''):
        self.sequence_diagram.add_record(f"{self.name}{Arrow.RETURN}{state}{to.name}:{message}")

    def self_message(self, message):
        self.sequence_diagram.add_record(f"{self.name}{Arrow.SYNC}{self.name}:{message}")

    def note(self, text, is_left=False):
        if is_left:
            r = f"Note left of {self.name}: {text}"
        else:
            r = f"Note right of {self.name}: {text}"
        self.sequence_diagram.add_record(r)

    def activate(self):
        self.sequence_diagram.add_record(f"activate {self.name}")

    def deactivate(self):
        self.sequence_diagram.add_record(f"deactivate {self.name}")

    def call_and_wait_response(self, to, message, response_message="ok"):
        self.sync_message(to, message, State.ACTIVATE)
        to.return_message(self, response_message, State.DEACTIVATE)
