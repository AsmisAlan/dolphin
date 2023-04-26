import json
import concurrent.futures
from graph import Graph
from dfs import depth_first_search

# Transformation functions


def to_string(data):
    return str(data)


TRANSFORMATIONS = {
    'to_string': to_string,
}


def has_circular_dependency(graph_data, start_node, visited=None, recursion_stack=None):
    if visited is None:
        visited = set()
    if recursion_stack is None:
        recursion_stack = set()

    visited.add(start_node)
    recursion_stack.add(start_node)

    for edge in graph_data["edges"]:
        if edge["source"] == start_node:
            destination_node = edge["destination"]

            # If the destination_node is already in the recursion_stack, there is a circular dependency
            if destination_node in recursion_stack:
                return True

            # If the destination_node has not been visited, perform DFS
            if destination_node not in visited:
                if has_circular_dependency(graph_data, destination_node, visited, recursion_stack):
                    return True

    recursion_stack.remove(start_node)
    return False


# Circular dependency detection
if depth_first_search(graph_data):
    raise ValueError("Circular dependency detected in the graph")

# Graph execution
graph = Graph(modules)


def execute_node_and_transform(node, input_key, transformation_name):
    result = graph.exec_instruction(node)
    transformation_func = TRANSFORMATIONS[transformation_name]
    return (input_key, transformation_func(result))


def execute_graph(graph_data, graph):
    # Find the start node and execute the connected nodes
    start_node = graph_data["nodes"]["start"]
    for edge in graph_data["edges"]:
        if edge["source"] == "start":
            destination_node = graph_data["nodes"][edge["destination"]]
            execute_node_recursive(destination_node, graph_data, graph)


def execute_node_recursive(current_node, graph_data, graph):
    # Execute the current node if it's not the special "start" node
    if current_node.get("type") != "start":
        result = graph.exec_instruction(current_node)

        # Update the input of connected nodes and execute them
        for edge in graph_data["edges"]:
            if edge["source"] == current_node["feature"]:
                destination_node = graph_data["nodes"][edge["destination"]]

                # Apply input transformation if specified
                if "input_transformations" in destination_node:
                    input_key = edge["input_key"]
                    if input_key in destination_node["input_transformations"]:
                        transformation_name = destination_node["input_transformations"][input_key]
                        transformation_func = TRANSFORMATIONS[transformation_name]
                        result = transformation_func(result)

                # Update input and execute connected nodes
                destination_node["input"][edge["input_key"]] = result
                execute_node_recursive(destination_node, graph_data, graph)


# Execute the graph starting from the "start" node
execute_graph(graph_data, graph)
