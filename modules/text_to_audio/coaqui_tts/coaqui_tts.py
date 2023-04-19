from typing import TypedDict
from io import BytesIO
import os
from TTS.api import TTS
# def coaquiTTS():
#     def operator(data):
#         # List available 🐸TTS models and choose the first one
#         model_name = TTS.list_models()[0]
#         # Init TTS
#         tts = TTS(model_name)
#         # Run TTS
#         # ❗ Since this model is multi-speaker and multi-lingual, we must set the target speaker and the language
#         # Text to speech with a numpy output
#         wav = tts.tts("This is a test! This is also a test!!",
#                       speaker=tts.speakers[0], language=tts.languages[0])
#         # Text to speech to a file
#         tts.tts_to_file(
#             text=data, speaker=tts.speakers[0], language=tts.languages[0], file_path="output.wav")

#         # Play the audio file (platform-dependent)
#         if os.name == "posix":
#             # For Linux and macOS
#             os.system("mpg321 output.wav")
#         else:
#             # For Windows
#             os.system("start output.wav")

#         return data

#     return operator


class Configuration(TypedDict):
    '''Configuration for the Coqui TTS operator'''
    language: str


class Input(TypedDict):
    '''Input for the Coqui TTS operator'''
    text: str


def coaqui_tts_operator(configuration: Configuration, input: Input) -> bytes:
    result = BytesIO()

    # List available TTS models and choose the first one
    model_name = TTS.list_models()[0]

    # Init TTS
    tts = TTS(model_name)

    # Run TTS
    wav = tts.tts(input['text'], speaker=tts.speakers[0],
                  language=configuration['language'])

    # Concatenate the elements of the wav list into a single byte string
    audio_data = b"".join(wav)

    # Write audio data to BytesIO buffer
    result.write(audio_data)

    # Seek to the beginning of the buffer
    result.seek(0)

    return result.getvalue()


if __name__ == "__main__":
    configuration = {
        "language": "en"
    }
    input = {
        "text": "Hello world! This is Coqui TTS."
    }
    result = coaqui_tts_operator(configuration, input)

    # Save the bytes to a file
    with open("output.wav", "wb") as f:
        f.write(result)

    # Play the audio file (platform-dependent)
    if os.name == "posix":
        # For Linux and macOS
        os.system("mpg321 output.wav")
    else:
        # For Windows
        os.system("start output.wav")
