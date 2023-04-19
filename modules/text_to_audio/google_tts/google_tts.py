from typing import TypedDict
from gtts import gTTS
import os
from io import BytesIO
import pyglet


class Configuration(TypedDict):
    '''Configuration for the Google TTS operator'''
    language: str


class Input(TypedDict):
    '''Input for the Google TTS operator'''
    text: str


def google_tts_operator(configuration: Configuration, input: Input) -> bytes:
    result = BytesIO()
    # Create a gTTS object with the text and language
    tts = gTTS(text=input['text'], lang=configuration['language'], slow=False)

    tts.write_to_fp(result)

    result.seek(0)

    return result.getvalue()


if __name__ == "__main__":
    configuration = {
        "language": "en"
    }
    input = {
        "text": "Hello world! dolphine :D"
    }
    result = google_tts_operator(configuration, input)

    # Save the bytes to a file
    with open("output.mp3", "wb") as f:
        f.write(result)

    # Play the audio file (platform-dependent)
    if os.name == "posix":
        # For Linux and macOS
        os.system("mpg321 output.mp3")
    else:
        # For Windows
        os.system("start output.mp3")
