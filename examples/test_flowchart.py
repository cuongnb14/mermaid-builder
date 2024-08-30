import os

from mermaid_builder.base import Color, Icon
from mermaid_builder.flowchart import *

current_dir = os.path.dirname(os.path.abspath(__file__))


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

    chart.save(current_dir + "/outputs/flowchart.mmd")


test_flowchart()
