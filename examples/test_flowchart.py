import os

from mermaid_builder.base import Color, Icon
from mermaid_builder.flowchart import *

current_dir = os.path.dirname(os.path.abspath(__file__))


def test_flowchart():
    chart = Flowchart(title="Simple Flowchart")

    # Declare nodes
    subgraph = Subgraph(name="Storage")

    user_node = Node(name="User", shape=NodeShape.ROUNDED_RECTANGLE, icon=Icon.USER)
    elb_node = Node(name="ELB", shape=NodeShape.ROUNDED_RECTANGLE, icon=Icon.LOAD_BALANCER, class_name="gateway")

    order_node = Node(name="Order Service", shape=NodeShape.ROUNDED_RECTANGLE, class_name="api")
    payment_node = Node(name="Payment Service", shape=NodeShape.ROUNDED_RECTANGLE, class_name="api")

    redis_node = Node(name="Redis", shape=NodeShape.ROUNDED_RECTANGLE, class_name="storage", subgraph=subgraph)
    db_node = Node(name="DB", shape=NodeShape.CYLINDER, icon=Icon.DATABASE, class_name="storage", subgraph=subgraph)

    # Declare node connections (edges)
    user_node.add_connections(Link(text="call"), elb_node)
    elb_node.add_connections(Link(), order_node, payment_node)
    order_node.add_connections(Link(), redis_node, db_node)
    payment_node.add_connections(Link(), subgraph)

    # Add items to chart (nodes or subgraph)
    chart.add_items(user_node, order_node, subgraph, payment_node, redis_node, elb_node)

    # Add styles
    chart.add_styles(Style(class_name="gateway", fill=Color.RED, color=Color.WHITE))
    chart.add_styles(Style(class_name="api", fill=Color.ORANGE, color=Color.WHITE))
    chart.add_styles(Style(class_name="storage", fill=Color.GREEN, color=Color.WHITE))

    chart.save(current_dir + "/outputs/flowchart.mmd")
    print(chart.get_mermaid_live_url())


test_flowchart()
