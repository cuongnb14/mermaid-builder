import os

from mermaid_builder import sequence_diagram as sd
from mermaid_builder.base import Color

current_dir = os.path.dirname(os.path.abspath(__file__))


def test_sequence_diagram():
    diagram = sd.SequenceDiagram(title="Simple Sequence Diagram")

    # Add Participants
    runner = sd.Participant(sequence_diagram=diagram, name="Github Runner", is_actor=True)
    azure = sd.Participant(sequence_diagram=diagram, name="Azure")
    mcr = sd.Participant(sequence_diagram=diagram, name="MCR")
    aks = sd.Participant(sequence_diagram=diagram, name="AKS")

    runner.sync_message(azure, message="Login", state=sd.State.ACTIVATE)
    runner.activate()

    azure.return_message(runner, message="Token", state=sd.State.DEACTIVATE)

    runner.call_and_wait_response(mcr, message="Push docker image")
    runner.call_and_wait_response(aks, message="Check existing install")
    aks.note("Conditionally<br/>Force Uninstall")
    diagram.note_over("optional", runner, aks)

    runner.call_and_wait_response(aks, message="Helm Install dry run")

    with diagram.fragment(sd.Fragment.BACKGROUND, Color.hex_to_rgb(Color.ORANGE)) as _:
        runner.sync_message(aks, message="Helm Install", state=sd.State.ACTIVATE)
        runner.sync_message(aks, message="Check deployment status")

        aks.call_and_wait_response(mcr, message="Pull docker image")
        aks.self_message(message="Deploy app")

        with diagram.fragment(sd.Fragment.LOOP, "Wait") as _:
            aks.self_message(message="Check IP Address")

        aks.return_message(runner, message="IP Address", state=sd.State.DEACTIVATE)
        runner.deactivate()

    diagram.save(current_dir + "/outputs/sequence_diagram.mmd")
    print(diagram.get_mermaid_live_url())


test_sequence_diagram()
