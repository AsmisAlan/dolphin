from typing import Dict
import openai
from modules.natural_language.openia_chat_gpt.domain.chat_gpt_configuration import ChatGPTConfiguration
from modules.natural_language.openia_chat_gpt.domain.chat_gpt_data import ChatGPTInput, ChatGPTOutput
# langchang
# import LangChain libraries
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.llms import OpenAI  # import OpenAI model
from langchain.prompts import PromptTemplate  # import PromptTemplate


def _create_message(chunk: str, question: str) -> Dict[str, str]:
    """Create a message for the chat completion
    Args:
        chunk (str): The chunk of text to summarize
        question (str): The question to answer
    Returns:
        Dict[str, str]: The message to send to the chat completion
    """
    return {
        "role": "user",
        "content": chunk,
    }


def split_string(s, max_length):
    substrings = []

    # Loop over the string, incrementing by max_length each time.
    for i in range(0, len(s), max_length):
        # Get the substring from s.
        substring = s[i:i+max_length]
        # Append the substring to the list.
        substrings.append(substring)

    # Return the list of substrings.
    return substrings


def chat_gpt_prompt(configuration: ChatGPTConfiguration, input: ChatGPTInput) -> ChatGPTOutput:
    ''' Chat gpt prompt operator '''
    openai.api_key = configuration["api_key"]

    results = []

    for chunk in split_string(input.content, 1500):
        messages = [
            {"role": "system", "content": configuration["system_role"]},
            _create_message(chunk, configuration["system_role"])
        ]

        print("working with chunk: ", chunk)

        completion = openai.ChatCompletion.create(
            model=configuration["model"],
            messages=messages,
            temperature=configuration["temperature"],
            max_tokens=configuration["max_tokens"]
        )

        results.append(completion.choices[0].message.content)

    # messages.append({"role": "user", "content": input.content})

    # TODO check the response completion
    chat_response = "\n".join(results)

    print("chat_response: ", chat_response)

    return ChatGPTOutput(content=chat_response)


if __name__ == "__main__":
    content = "Hello world"
    result = chat_gpt_prompt({
        "api_key": "YOUR-API-KEY",
        "system_role": "Your role is to create a translation of the given text to spanish, dont repeat the work , just the translation",
        "model": "gpt-3.5-turbo",
        "temperature": 0,
        "max_tokens": 10},
        {"content": content})
    print("content: ", content, "result: ", result)
