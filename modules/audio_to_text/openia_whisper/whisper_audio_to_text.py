from whisper import load_model
from datetime import timedelta
import tempfile
from typing import TypedDict

# print("numpy version:", numpy.__version__)
# print("pandas version:", pandas.__version__)
# print("requests version:", requests.__version__)

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

    file_path = "C:\DEV\delfin\Snapinsta.app_video_10000000_3458621627742288_9212203214280848790_n.mp4"

    with open(file_path, 'rb') as audio_file:
        file_data = audio_file.read()

    # Create a temporary file and write the audio data to it
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_audio_file:
        temp_audio_file.write(file_data)
        temp_path = temp_audio_file.name

    input_data = {
        "audio": temp_path
    }
    result = whisper_audio_to_subtitle(configuration, input_data)

    print(result)
