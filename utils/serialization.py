import json
from graphics.node_item import Node
from graphics.edge_item import Edge
from graphics.port_item import Port

def serialize_scene(scene):
    nodes_data = []
    edges_data = []
    
    # Collect nodes and edges
    for item in scene.items():
        if isinstance(item, Node):
            node_data = {
                "id": item.id,
                "x": item.pos().x(),
                "y": item.pos().y(),
                "label": item.label.toPlainText(),
                "inputs": [p.label.toPlainText() for p in item.input_ports],
                "outputs": [p.label.toPlainText() for p in item.output_ports],
                "function": getattr(item, 'function', ""),
                "internal_graph": getattr(item, 'internal_graph', None)
            }
            nodes_data.append(node_data)
        elif isinstance(item, Edge):
            out_port = item.output_port
            in_port = item.input_port
            out_node = out_port.node
            in_node = in_port.node
            
            out_index = out_node.output_ports.index(out_port)
            in_index = in_node.input_ports.index(in_port)
            
            edges_data.append({
                "output_node_id": out_node.id,
                "output_port_index": out_index,
                "input_node_id": in_node.id,
                "input_port_index": in_index
            })
            
    return {
        "nodes": nodes_data,
        "edges": edges_data
    }

def deserialize_scene(scene, data):
    # Clear existing items
    scene.clear()
    scene.dragging_edge = None
    scene.drag_start_port = None
    
    nodes_by_id = {}
    
    # Recreate nodes
    for node_data in data.get("nodes", []):
        node = Node(
            x=node_data["x"],
            y=node_data["y"],
            label=node_data.get("label", "Node"),
            inputs=node_data.get("inputs", []),
            outputs=node_data.get("outputs", []),
            node_id=node_data["id"],
            function=node_data.get("function", ""),
            internal_graph=node_data.get("internal_graph", None)
        )
        scene.addItem(node)
        nodes_by_id[node.id] = node
        
    # Recreate edges
    for edge_data in data.get("edges", []):
        out_node_id = edge_data["output_node_id"]
        in_node_id = edge_data["input_node_id"]
        
        if out_node_id in nodes_by_id and in_node_id in nodes_by_id:
            out_node = nodes_by_id[out_node_id]
            in_node = nodes_by_id[in_node_id]
            
            out_idx = edge_data["output_port_index"]
            in_idx = edge_data["input_port_index"]
            
            if out_idx < len(out_node.output_ports) and in_idx < len(in_node.input_ports):
                out_port = out_node.output_ports[out_idx]
                in_port = in_node.input_ports[in_idx]
                
                # Check connection validity to be safe
                if in_port.can_connect():
                    edge = Edge(out_port, in_port)
                    scene.addItem(edge)

def save_to_file(scene, filepath):
    data = serialize_scene(scene)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def load_from_file(scene, filepath):
    import os
    if not os.path.exists(filepath):
        return False
    with open(filepath, 'r') as f:
        data = json.load(f)
    deserialize_scene(scene, data)
    return True
