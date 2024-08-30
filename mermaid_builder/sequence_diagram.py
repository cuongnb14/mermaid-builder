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
    def __init__(self, title, theme=None, show_number=False):
        super().__init__(title, theme)
        self.records = []
        self.participants = []
        self.actors = []
        self.intent_index = 1
        self.show_number = show_number

    def add_record(self, record):
        self.records.append(self.intent_index * INTENT_CHAR + record)

    def draw(self):
        result = self.get_header_lines()
        result += ["sequenceDiagram"]
        if self.show_number:
            result += [f"{INTENT_CHAR}autonumber"]
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

    def set_sequence_diagram(self, sequence_diagram):
        self.sequence_diagram = sequence_diagram

    def _get_state_char(self, active):
        state = ""
        if active is not None:
            if active:
                state = State.ACTIVATE
            else:
                state = State.DEACTIVATE
        return state

    def send(self, to, message, active=None):
        state = self._get_state_char(active)
        self.sequence_diagram.add_record(f"{self.name}{Arrow.SYNC}{state}{to.name}:{message}")

    def asend(self, to, message, active=None):
        state = self._get_state_char(active)
        self.sequence_diagram.add_record(f"{self.name}{Arrow.ASYNC}{state}{to.name}:{message}")

    def return_message(self, to, message, active=None):
        state = self._get_state_char(active)
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

    def send_and_wait_response(self, to, message, response_message="ok"):
        self.send(to, message, active=True)
        to.return_message(self, response_message, active=False)
