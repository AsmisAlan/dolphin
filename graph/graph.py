import json
from typing import List, Any, TypedDict


class Node:
    """
    Node represents a node in the graph
    """

    def __init__(self, description: str, instruction: str, configuration: TypedDict, key: str):
        self.key = key
        self.description = description
        self.instruction = instruction
        self.configuration = configuration


class Edge:
    """
    Edge represents a directed edge between two nodes
    """

    def __init__(self, source: str, destination: str):
        self.source = source
        self.destination = destination


class Graph:
    """
    Graph represents a graph of nodes and edges
    """

    def __init__(self, version: str, description: str, nodes: TypedDict, edges: List[Edge]):
        self.version = version
        self.description = description
        self.nodes = nodes
        self.edges = edges
        # Check the names of the nodes
        if not self.are_node_names_valid():
            raise Exception("Node names are not valid")

        if self.has_circular_dependency():
            raise Exception("Circular dependency detected")

    def are_node_names_valid(self):
        """
        check if the node names are valid.
        """
        nodes_keys = self.nodes
        edges = self.edges

        for edge in edges:
            source = edge.source
            destination = edge.destination

            if source == "start" and destination not in nodes_keys:
                return False
            elif source != "start" and source not in nodes_keys or destination not in nodes_keys:
                return False

        return True

    def build_adjacency_list(self, edges: List[Edge]):
        """
        build_adjacency_list builds an adjacency list from a list of edges
        """
        adjacency_list = {}

        for edge in edges:
            source = edge.source
            destination = edge.destination

            if source not in adjacency_list:
                adjacency_list[source] = []

            adjacency_list[source].append(destination)

        return adjacency_list

    def dfs_visit(self, node, adjacency_list, visited, recursion_stack):
        """
        dfs_visit performs a depth first search on the graph
        """
        visited.add(node)
        recursion_stack.add(node)

        if node in adjacency_list:
            for neighbor in adjacency_list[node]:
                if neighbor not in visited:
                    if self.dfs_visit(neighbor, adjacency_list, visited, recursion_stack):
                        return True
                elif neighbor in recursion_stack:
                    return True

        recursion_stack.remove(node)
        return False

    def has_circular_dependency(self):
        """
        has_circular_dependency checks if the graph has a circular dependency
        """
        adjacency_list = self.build_adjacency_list(self.edges)
        visited = set()
        recursion_stack = set()

        for node in adjacency_list:
            if node not in visited:
                if self.dfs_visit(node, adjacency_list, visited, recursion_stack):
                    return True

        return False

    def get_start_node(self) -> Node:
        """
        get_start_node returns the start node of the graph
        """
        name_to_find = 'start'
        initial_edge: Edge = None

        for edge in self.edges:
            if edge.source == name_to_find:
                initial_edge = edge
                break

        if not initial_edge:
            raise Exception("No start node found")

        return self.nodes.get(initial_edge.destination)

    def get_node(self, nodeKey: str) -> Node:
        return self.nodes.get(nodeKey)

    def get_outgoing_edges(self, source: str) -> List[Edge]:
        outgoing_edges = []

        for edge in self.edges:
            if edge.source == source:
                outgoing_edges.append(edge)

        return outgoing_edges


def create_graph_from_json(json_string: str) -> Graph:
    """
    create_graph_from_json creates a Graph instance from a JSON string
    """
    data = json.loads(json_string)

    # Create Node instances
    nodes = {}
    for node_name, node_data in data["nodes"].items():
        nodes[node_name] = Node(
            description=node_data["description"],
            instruction=node_data["instruction"],
            configuration=node_data["configuration"],
            key=node_name
        )

    # Create Edge instances
    edges = [
        Edge(
            source=edge_data["source"],
            destination=edge_data["destination"]
        )
        for edge_data in data["edges"]
    ]

    # Create Graph instance
    graph = Graph(
        version=data["version"],
        description=data["description"],
        nodes=nodes,
        edges=edges
    )

    return graph


if __name__ == "__main__":
    # JSON string
    json_string = """
    {
        "version": "1.0",
        "description": "Create a news article for a given topic",
        "nodes": {
            "search_content": {
                "description": "Look for the given information",
                "instruction": "search_engine_ddg",
                "configuration": {
                    "max_results": 10,
                    "output": "json"
                }
            },
            "create_summary": {
                "description": "Make a summary of the given links",
                "instruction": "natural_language_openai_chat_gpt",
                "configuration": {
                    "max_tokens": 100,
                    "temperature": 0.9,
                    "model": "gpt-3.5-turbo",
                    "api_key": "your-api-key",
                    "system_role": "Crea el texto de una noticia con el siguiente contenido"
                }
            }
        },
        "edges": [
            {
                "source": "start",
                "destination": "search_content"
            },
            {
                "source": "search_content",
                "destination": "create_summary"
            }
        ]
    }
    """

    # Create the Graph instance from the JSON string
    graph_from_json = create_graph_from_json(json_string)

    print("graph version: ", graph_from_json.version)
    print("graph description: ", graph_from_json.description)

    starting_node = graph_from_json.get_start_node()

    print("Initial node: ", starting_node.description)
