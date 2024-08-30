from mermaid_builder.base import Color, Icon
from mermaid_builder.flowchart import *
from mermaid_builder import sequence_diagram as sd


def test_flowchart():
    chart = Flowchart(title="Simple Flowchart")

    user_node = Node(name="User", shape=NodeShape.ROUND_EDGE, icon=Icon.USER)
    elb_node = Node(name="ELB", shape=NodeShape.ROUND_EDGE, icon=Icon.LOAD_BALANCER)
    order_node = Node(name="Order Service", shape=NodeShape.ROUND_EDGE, class_name="api")
    payment_node = Node(name="Payment Service", shape=NodeShape.ROUND_EDGE, class_name="api")
    redis_node = Node(name="Redis", shape=NodeShape.ROUND_EDGE, class_name="storage")
    db_node = Node(name="DB", shape=NodeShape.ROUND_EDGE, icon=Icon.DATABASE, class_name="storage")

    user_node.add_connections(Link(text="call"), elb_node)
    elb_node.add_connections(Link(), order_node, payment_node)

    order_node.add_connections(Link(), redis_node, db_node)

    subgraph = Subgraph(name="Storage")
    subgraph.add_nodes(redis_node, db_node)
    payment_node.add_connections(Link(), subgraph)

    chart.add_items(user_node, order_node, subgraph, payment_node, redis_node, elb_node)
    chart.add_styles(Style(class_name="api", fill=Color.ORANGE, color=Color.WHITE))
    chart.add_styles(Style(class_name="storage", fill=Color.GREEN, color=Color.WHITE))

    chart.save("./outputs/flowchart.mmd")


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

    runner.sync_message(aks, message="Helm Install", state=sd.State.ACTIVATE)
    runner.sync_message(aks, message="Check deployment status", )

    aks.call_and_wait_response(mcr, message="Pull docker image")
    aks.self_message(message="Deploy app")

    with diagram.fragment(sd.Fragment.LOOP, "Wait") as _:
        aks.self_message(message="Check IP Address")

    aks.return_message(runner, message="IP Address", state=sd.State.DEACTIVATE)
    runner.deactivate()

    diagram.save("./outputs/sequence_diagram.mmd")
    print(diagram.get_mermaid_live_url())


test_sequence_diagram()
test_flowchart()
