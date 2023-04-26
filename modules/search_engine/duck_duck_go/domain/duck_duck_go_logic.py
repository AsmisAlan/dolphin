from duckduckgo_search import ddg

from modules.search_engine.duck_duck_go.domain.duck_duck_go_configuration import DuckDuckGoConfiguration
from modules.search_engine.duck_duck_go.domain.duck_duk_go_data import DuckDuckGoInput, DuckDuckGoOutput


def search_ddg(configuration: DuckDuckGoConfiguration, input: DuckDuckGoInput) -> DuckDuckGoOutput:
    pages = ddg(input.query, max_results=configuration['max_results'],
                output=configuration['output'], download=False)

    output = DuckDuckGoOutput(pages=pages)

    return output


# todo create test cases
if __name__ == "__main__":
    result = search_ddg(
        {'max_results': 10, 'output': 'json'}, {'query': 'python'})

    print("First page:", result.get('pages')[0])
