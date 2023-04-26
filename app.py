import json

graph_template_json = """
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


python_object = json.loads(graph_template_json)


# Execution constraints
def execute_graph(graph_data):
    start_node = graph_data["edges"]["start"]
    for edge in graph_data["edges"]:
        if edge["source"] == "start":
            destination_nodes = edge["destinations"]
            for destination in destination_nodes:
                destination_node = graph_data["nodes"][destination]
                execute_node_recursive(destination_node, graph_data)
