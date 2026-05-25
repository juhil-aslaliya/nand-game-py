from graphics.node_item import Node
from graphics.edge_item import Edge

class GraphEvaluator:
    @staticmethod
    def evaluate(scene):
        print("\n--- Starting Execution ---")
        nodes = [item for item in scene.items() if isinstance(item, Node)]
        edges = [item for item in scene.items() if isinstance(item, Edge)]
        in_degree = {node.id: 0 for node in nodes}
        node_by_id = {node.id: node for node in nodes}
        edge_map = {}
        for edge in edges:
            out_node = edge.output_port.node
            in_node = edge.input_port.node
            in_degree[in_node.id] += 1
            out_idx = out_node.output_ports.index(edge.output_port)
            in_idx = in_node.input_ports.index(edge.input_port)
            if out_node.id not in edge_map:
                edge_map[out_node.id] = []
            edge_map[out_node.id].append({
                "out_name": out_node.outputs[out_idx],
                "to_node": in_node.id,
                "in_name": in_node.inputs[in_idx]
            })
        queue = [node for node in nodes if in_degree[node.id] == 0]
        node_memory = {node.id: {} for node in nodes}
        executed_count = 0
        while queue:
            current = queue.pop(0)
            executed_count += 1
            local_env = dict(node_memory[current.id])
            if current.function:
                try:
                    exec(current.function, {}, local_env)
                    print(f"Executed [{current.label.toPlainText()}]: {local_env}")
                except Exception as e:
                    print(f"Error in [{current.label.toPlainText()}]: {e}")
                    continue
            else:
                print(f"Skipped [{current.label.toPlainText()}]: No function defined")
            if current.id in edge_map:
                for connection in edge_map[current.id]:
                    out_val = local_env.get(connection["out_name"], None)
                    target_id = connection["to_node"]
                    target_in_name = connection["in_name"]
                    node_memory[target_id][target_in_name] = out_val
                    in_degree[target_id] -= 1
                    if in_degree[target_id] == 0:
                        queue.append(node_by_id[target_id])
        if executed_count < len(nodes):
            print("Warning: Infinite loop or cycle detected. Some nodes were skipped.")
        print("--- Execution Finished ---\n")