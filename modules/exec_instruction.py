import importlib.util
from typing import TypedDict
from mappers.beautiful_soup_mappers import map_to_beautiful_soup_input
from mappers.chat_gpt_mappers import map_to_chat_gpt_input
from mappers.duck_duck_go_mappers import map_to_duck_duck_go_input

modules = {
    'search_engine_ddg': {
        'module_path': 'modules/search_engine/duck_duck_go/domain/duck_duck_go_logic.py',
        'function_name': 'search_ddg',
        'mapper': lambda input: map_to_duck_duck_go_input(input)
    },
    'natural_language_openai_chat_gpt': {
        'module_path': 'modules/natural_language/openia_chat_gpt/domain/chat_gpt_logic.py',
        'function_name': 'chat_gpt_prompt',
        'mapper': lambda input: map_to_chat_gpt_input(input)
    },
    'web_scrapping_bs': {
        'module_path': 'modules/web_scrapping/beautiful_soup/domain/beautiful_soup_logic.py',
        'function_name': 'scrap_pages',
        'mapper': lambda input: map_to_beautiful_soup_input(input)
    },
    # 'web_scrapping_bs_extract_articles': {
    #     'module_path': 'modules/web_scrapping/beautiful_soup/beautiful_soup.py',
    #     'function_name': 'extract_articles'
    # },
    # 'text_to_speech_google_tts': {
    #     'module_path': 'modules/text_to_speech/google_tts/google_tts.py',
    #     'function_name': 'text_to_speech'
    # },

}


class InstructionData(TypedDict):
    '''Define the data structure for the instruction'''
    feature: str
    input: TypedDict
    configuration: TypedDict


def exec_instruction(instruction: InstructionData):
    # specify the path to the module
    module_definition = modules[instruction['feature']]

    if (module_definition == None):
        return

    # load the module dynamically
    spec = importlib.util.spec_from_file_location(
        instruction['feature'], module_definition['module_path'])
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    input = module_definition['mapper'](
        instruction['input']) if 'mapper' in module_definition else instruction['input']

    # use the module
    return getattr(module, module_definition['function_name'])(instruction['configuration'], input)


if __name__ == "__main__":
    result = exec_instruction(instruction={
        'feature': 'search_engine_ddg',
        'input': {'query': 'python'},
        'configuration': {'max_results': 10, 'output': 'json'}
    })

    result = exec_instruction(instruction={
        'feature': 'natural_language_openai_chat_gpt',
        'input': {'content': str(result)},
        'configuration': {'max_tokens': 100, 'temperature': 0.9, 'model': 'gpt-3.5-turbo', 'api_key': 'YOUR-API-KEY', 'system_role': 'You are a python expert and you are going to make a summary of the given links'}
    })

    print(result)
