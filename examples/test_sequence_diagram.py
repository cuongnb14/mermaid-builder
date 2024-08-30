import os

from mermaid_builder import sequence_diagram as sd
from mermaid_builder.base import Color

current_dir = os.path.dirname(os.path.abspath(__file__))


def test_sequence_diagram():
    diagram = sd.SequenceDiagram(title="Simple Sequence Diagram", show_number=True)

    # Add Participants
    runner = sd.Participant(sequence_diagram=diagram, name="Github Runner", is_actor=True)
    azure = sd.Participant(sequence_diagram=diagram, name="Azure")
    mcr = sd.Participant(sequence_diagram=diagram, name="MCR")
    aks = sd.Participant(sequence_diagram=diagram, name="AKS")

    runner.send(azure, message="Login", active=True)
    runner.activate()

    azure.return_message(runner, message="Token", active=False)

    runner.send_and_wait_response(mcr, message="Push docker image")
    runner.send_and_wait_response(aks, message="Check existing install")
    aks.note("Conditionally<br/>Force Uninstall")
    diagram.note_over("optional", runner, aks)

    runner.send_and_wait_response(aks, message="Helm Install dry run")

    with diagram.fragment(sd.Fragment.BACKGROUND, Color.hex_to_rgb(Color.CYAN)) as _:
        runner.send(aks, message="Helm Install", active=True)
        runner.send(aks, message="Check deployment status")

        aks.send_and_wait_response(mcr, message="Pull docker image")
        aks.self_message(message="Deploy app")

        with diagram.fragment(sd.Fragment.LOOP, "Wait") as _:
            aks.self_message(message="Check IP Address")

        aks.return_message(runner, message="IP Address", active=False)
        runner.deactivate()

    diagram.save(current_dir + "/outputs/sequence_diagram.mmd")
    print(diagram.get_mermaid_live_url())


test_sequence_diagram()
