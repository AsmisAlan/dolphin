class ChatGPTInput():
    '''Input for the chat gpt prompt operator'''

    def __init__(self, content: str):
        self.content = content


class ChatGPTOutput():
    '''Input for the chat gpt prompt operator'''

    def __init__(self, content: str):
        self.content = content

    def __str__(self) -> str:
        return self.content
