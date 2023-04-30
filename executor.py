from graph.graph import Graph, Node, create_graph_from_json
from modules.exec_instruction import exec_instruction
from typing import Any, TypedDict


def execute_node_recursive(graph: Graph, input: Any, current_node: Node = None):
    """
    execute_node_recursive executes a node and all the connected nodes recursively
    """
    # The fist time we try to get the initial node from the graph
    if not current_node:
        current_node = graph.get_start_node()
    # current_node = graph.get_start_node()

    if current_node:
        # Execute the current node instruction
        print(f"{current_node.description} (running)")
        result = exec_instruction(instruction={
            'configuration': current_node.configuration,
            'feature': current_node.instruction,
            'input': input,
        })
        print(f"{current_node.description} (finished)")

        print(result)

        # Iterate all the destination nodes
        for edge in graph.get_outgoing_edges(current_node.key):
            destination_node = graph.get_node(edge.destination)
            execute_node_recursive(graph, result, destination_node)


json_string = """
{
    "version": "1.0",
    "description": "Makes a web search and returns the results",
    "nodes": {
        "improve_search": {
            "description": "Improve the query",
            "instruction": "natural_language_openai_chat_gpt",
            "configuration": {
                "max_tokens": 40,
                "temperature": 0.9,
                "model": "gpt-3.5-turbo",
                "api_key": "YOUR-API-KEY",
                "system_role": "Based on the given text create a better search query, use double quotes to search for an exact match in important words, use the language of the user to create the query"
            }
        },
        "search_content": {
            "description": "Search the given information",
            "instruction": "search_engine_ddg",
            "configuration": {
                "max_results": 3,
                "output": "json"
            }
        },
        "obtain_raw_information": {
            "description": "Gathering information from the given links",
            "instruction": "web_scrapping_bs",
            "configuration": {
                "raw": true
            }
        },
        "create_summary": {
            "description": "Make a summary of the given results",
            "instruction": "natural_language_openai_chat_gpt", 
            "configuration": {
                "max_tokens": 3000,
                "temperature": 0.2,
                "model": "gpt-3.5-turbo",
                "api_key": "YOUR-API-KEY",
                "system_role": "Create a post for medium with markdown format, ignore the links that are not relevant, use the language of the user to create the post"
            }
        }
    },
    "edges": [
        {
            "source": "start",
            "destination": "improve_search"
        },
        {
            "source": "improve_search",
            "destination": "search_content"
        }, 
        {
            "source": "search_content",
            "destination": "obtain_raw_information"
        },
        {
            "source": "obtain_raw_information",
            "destination": "create_summary"
        }
    ]
}
"""

# Create the Graph instance from the JSON string
graph_from_json = create_graph_from_json(json_string)

execute_node_recursive(
    graph_from_json, "how to cook an egg")
