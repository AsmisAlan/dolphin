from typing import TypedDict
from gtts import gTTS
import os


class Configuration(TypedDict):
    '''Configuration for the Google TTS operator'''
    language: str


class Input(TypedDict):
    '''Input for the Google TTS operator'''
    text: str


def google_tts_operator(configuration: Configuration, input: Input) -> str:
    # Create a gTTS object with the text and language
    tts = gTTS(text=input['text'], lang=configuration['language'], slow=False)

    # Save the speech to an audio file (mp3 format)
    tts.save("output.mp3")

    # Play the audio file (platform-dependent)
    if os.name == "posix":
        # For Linux and macOS
        os.system("mpg321 output.mp3")
    else:
        # For Windows
        os.system("start output.mp3")

    return input['text']


if __name__ == "__main__":
    configuration = {
        "language": "en"
    }
    input = {
        "text": "Hello world"
    }
    result = google_tts_operator(configuration, input)
    print("input: ", input, "result: ", result)
