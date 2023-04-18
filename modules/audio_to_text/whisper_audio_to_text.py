from whisper import load_model
import hashlib
from datetime import timedelta
import os
from typing import TypedDict, Literal

# whisper is working wheel , todo: use https://github.com/MrEdwards007/WhisperTaskAcceleration/blob/main/WhisperTaskAcceleration.py


class Configuration(TypedDict):
    '''Configuration for the whisper audio to subtitle operator'''
    modelType: str
    language: str
    temperature: float


class Input(TypedDict):
    '''Input for the whisper audio to subtitle operator'''
    audio: str


def whisper_audio_to_text(configuration: Configuration, input: Input):
    model = load_model(configuration['modelType'])

    result = model.transcribe(
        input['audio'],
        language=configuration['language'],
        temperature=configuration['temperature'],
        fp16=False
    )

    return result.text


def whisper_audio_to_subtitle(configuration: Configuration, input: Input):
    model = load_model(configuration['modelType'])

    result = model.transcribe(
        input['audio'],
        language=configuration['language'],
        temperature=configuration['temperature'],
        word_timestamps=True,
        fp16=False,
        verbose=True,
    )

    strContent = ""

    for segment in result["segments"]:
        startTime = str(0) + \
            str(timedelta(seconds=int(segment['start']))) + ',000'
        endTime = str(0) + \
            str(timedelta(seconds=int(segment['end']))) + ',000'
        text = segment['text']
        segmentId = segment['id'] + 1
        newContent = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"
        strContent += newContent

    return strContent


if __name__ == "__main__":
    # load audio and pad/trim it to fit 30 seconds
    configuration = {
        "modelType": "medium",
        "language": "es",
        "temperature": 0.5
    }
    input = {
        "audio": "C:\DEV\delfin\snap.mp4"
    }
    result = whisper_audio_to_subtitle(configuration, input)

    print(result)
