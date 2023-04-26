from typing import TypedDict, Literal


class ChatGPTConfiguration(TypedDict):
    '''Configuration for the chat gpt prompt operator'''
    api_key: str
    system_role: str
    # for now only gpt-3.5-turbo will be available
    model: Literal["gpt-3.5-turbo"]
    # 0 - 1
    temperature: int
    # 2,048
    max_tokens: int
