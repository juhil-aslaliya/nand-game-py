from graphics.node_item import Node
from graphics.edge_item import Edge

class GraphEvaluator:
    
    @staticmethod
    def evaluate_subgraph(graph_data, input_signals):
        """Headless evaluator that runs Kahn's Algorithm purely on JSON dicts"""
        nodes = graph_data.get("nodes", [])
        edges = graph_data.get("edges", [])
        
        in_degree = {n["id"]: 0 for n in nodes}
        node_by_id = {n["id"]: n for n in nodes}
        edge_map = {}
        
        for e in edges:
            out_node = node_by_id[e["output_node_id"]]
            in_node = node_by_id[e["input_node_id"]]
            in_degree[in_node["id"]] += 1
            
            if out_node["id"] not in edge_map:
                edge_map[out_node["id"]] = []
                
            out_idx = e["output_port_index"]
            in_idx = e["input_port_index"]
            
            # Map port indexes to their names securely
            out_name = out_node["outputs"][out_idx] if out_node.get("outputs") and out_idx < len(out_node["outputs"]) else None
            in_name = in_node["inputs"][in_idx] if in_node.get("inputs") and in_idx < len(in_node["inputs"]) else None
            
            edge_map[out_node["id"]].append({
                "out_name": out_name, "to_node": in_node["id"], "in_name": in_name
            })
            
        queue = [n for n in nodes if in_degree[n["id"]] == 0]
        node_memory = {n["id"]: {} for n in nodes}
        
        # 1. Map incoming signals to the internal "Input Pins"
        input_pins = sorted([n for n in nodes if n.get("label") == "Input Pin"], key=lambda x: x["y"])
        for pin in input_pins:
            # Grab the custom port name
            in_key = pin["outputs"][0] if pin.get("outputs") else "Val"
            if in_key in input_signals:
                node_memory[pin["id"]][in_key] = input_signals[in_key]
                
        output_pins = sorted([n for n in nodes if n.get("label") == "Output Pin"], key=lambda x: x["y"])
        output_signals = {}
        
        # 2. Execute the headless graph
        while queue:
            current = queue.pop(0)
            local_env = dict(node_memory[current["id"]])
            
            if current.get("label") == "Input Pin":
                # Ensure the local environment uses the custom port name
                port_name = current["outputs"][0] if current.get("outputs") else "Val"
                local_env[port_name] = node_memory[current["id"]].get(port_name, False)
            elif current.get("internal_graph"):
                # RECURSION: If a component has components inside it!
                local_env.update(GraphEvaluator.evaluate_subgraph(current["internal_graph"], local_env))
            elif current.get("function"):
                try:
                    exec(current["function"], {}, local_env)
                except:
                    pass
                    
            # 3. Propagate forward
            if current["id"] in edge_map:
                for conn in edge_map[current["id"]]:
                    node_memory[conn["to_node"]][conn["in_name"]] = local_env.get(conn["out_name"])
                    in_degree[conn["to_node"]] -= 1
                    if in_degree[conn["to_node"]] == 0:
                        queue.append(node_by_id[conn["to_node"]])
                        
        # 4. Extract answers from the internal "Output Pins"
        for pin in output_pins:
            out_key = pin["inputs"][0] if pin.get("inputs") else "Val"
            output_signals[out_key] = node_memory[pin["id"]].get(out_key, False)
            
        return output_signals

    @staticmethod
    def evaluate(scene):
        nodes = [item for item in scene.items() if isinstance(item, Node)]
        edges = [item for item in scene.items() if isinstance(item, Edge)]
        for edge in edges:
            edge.set_live(False)

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

            live_out_name = out_node.output_ports[out_idx].label.toPlainText()
            live_in_name = in_node.input_ports[in_idx].label.toPlainText()
                
            edge_map[out_node.id].append({
                "out_name": live_out_name,
                "to_node": in_node.id,
                "in_name": live_in_name,
                "edge_item": edge
            })

        queue = [node for node in nodes if in_degree[node.id] == 0]
        node_memory = {node.id: {} for node in nodes}

        while queue:
            current = queue.pop(0)
            local_env = dict(node_memory[current.id])
            
            # --- THE NEW EXECUTION BLOCK ---
            if hasattr(current, 'internal_graph') and current.internal_graph:
                # Step inside the component!
                try:
                    component_outputs = GraphEvaluator.evaluate_subgraph(current.internal_graph, local_env)
                    local_env.update(component_outputs)
                except Exception as e:
                    print(f"Error in Component [{current.label.toPlainText()}]: {e}")
            elif current.function:
                # Standard Python node
                try:
                    exec(current.function, {}, local_env)
                except Exception as e:
                    print(f"Error in [{current.label.toPlainText()}]: {e}")
            # -------------------------------
                    
            if current.label.toPlainText() == "Output Pin":
                input_name = current.input_ports[0].label.toPlainText() if current.input_ports else "Val"
                val = local_env.get(input_name, False) 
                current.pin_state = bool(val)
                current.update_visuals()

            if current.id in edge_map:
                for connection in edge_map[current.id]:
                    out_val = local_env.get(connection["out_name"], None)
                    target_id = connection["to_node"]
                    target_in_name = connection["in_name"]
                    visual_edge = connection.get("edge_item")
                    if visual_edge:
                        visual_edge.set_live(bool(out_val))
                    node_memory[target_id][target_in_name] = out_val
                    
                    in_degree[target_id] -= 1
                    if in_degree[target_id] == 0:
                        queue.append(node_by_id[target_id])