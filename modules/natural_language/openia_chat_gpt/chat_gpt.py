from typing import TypedDict, Literal
import openai


class Configuration(TypedDict):
    '''Configuration for the chat gpt prompt operator'''
    api_key: str
    system_role: str
    # for now only gpt-3.5-turbo will be available
    model: Literal["gpt-3.5-turbo"]
    # 0 - 1
    temperature: int
    # 2,048
    max_tokens: int


class Input(TypedDict):
    '''Input for the chat gpt prompt operator'''
    content: str


def chat_gpt_prompt(configuration: Configuration, input: Input):
    ''' Chat gpt prompt operator '''
    openai.api_key = configuration["api_key"]

    messages = [
        {"role": "system", "content": configuration["system_role"]},
    ]

    messages.append({"role": "user", "content": input["content"]})

    completion = openai.ChatCompletion.create(
        model=configuration["model"],
        messages=messages,
        temperature=configuration["temperature"],
        max_tokens=configuration["max_tokens"]
    )

    chat_response = completion.choices[0].message.content
    print(chat_response)
    return chat_response


if __name__ == "__main__":
    content = "Hello world"
    result = chat_gpt_prompt({
        "api_key": "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",
        "system_role": "Your role is to create a translation of the given text to spanish, dont repeat the work , just the translation",
        "model": "gpt-3.5-turbo",
        "temperature": 0,
        "max_tokens": 10},
        {"content": content})
    print("content: ", content, "result: ", result)
