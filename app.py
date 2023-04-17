from typing import List, Callable
from abc import abstractmethod
import requests
import os
import openai
from gtts import gTTS
from TTS.api import TTS


class DolphinStream():

    def __init__(self) -> None:
        super().__init__()

    def pipe(self, operators):
        data = None
        for i, operator in enumerate(operators):
            if i == 0:
                data = operator()  # Call the first function without any input
            else:
                # Call the remaining functions with the previous output as input
                data = operator(data)


def googleTTS():
    def operator(data):
        # Create a gTTS object with the text and language (en: English)
        tts = gTTS(text=data, lang="es", slow=False)

        # Save the speech to an audio file (mp3 format)
        tts.save("output.mp3")

        # Play the audio file (platform-dependent)
        if os.name == "posix":
            # For Linux and macOS
            os.system("mpg321 output.mp3")
        else:
            # For Windows
            os.system("start output.mp3")

        return data

    return operator


def coaquiTTS():
    def operator(data):
        # List available 🐸TTS models and choose the first one
        model_name = TTS.list_models()[0]
        # Init TTS
        tts = TTS(model_name)
        # Run TTS
        # ❗ Since this model is multi-speaker and multi-lingual, we must set the target speaker and the language
        # Text to speech with a numpy output
        wav = tts.tts("This is a test! This is also a test!!",
                      speaker=tts.speakers[0], language=tts.languages[0])
        # Text to speech to a file
        tts.tts_to_file(
            text=data, speaker=tts.speakers[0], language=tts.languages[0], file_path="output.wav")

        # Play the audio file (platform-dependent)
        if os.name == "posix":
            # For Linux and macOS
            os.system("mpg321 output.wav")
        else:
            # For Windows
            os.system("start output.wav")

        return data

    return operator


def tap(callback: Callable):
    def tapOperator(data):
        callback(data)
        return data
    return tapOperator


def fakeChatGptPrompt(apiKey):
    def fromInput(prompt):
        return """
            Las secretarías de Energía y de Comercio de Argentina renovaron el acuerdo de Precios Justos con las empresas YPF, PAE, Raízen y Trafigura por los próximos 4 meses, con el objetivo de "proteger a los consumidores y garantizar la estabilidad en el mercado de combustibles". Se establece una pauta del 4% mensual en los precios de la nafta y el gasoil entre el 15 de abril y el 15 de agosto, con el fin de dar una señal de previsibilidad a consumidores, usuarios y empresas y acompañar la hoja de ruta establecida por el ministro de Economía, Sergio Massa. FAKE
            """
    return fromInput


def chatGptPrompt(apiKey):
    openai.api_key = apiKey

    def fromInput(prompt):
        # Replace 'your_api_key' with your actual API key
        messages = [
            {"role": "system", "content": "tu propocito es resumir el texto en menos de 50 palabras en español"}
        ]

        messages.append({"role": "user", "content": prompt})

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        chat_response = completion.choices[0].message.content
        print(chat_response)
        return chat_response
    return fromInput


def getNews():
    def fromInput():
        return """ 
16.0.0-rc.0 (2023-04-12)
compiler
Commit	Type	Description
9de1e9da8f	fix	incorrectly matching directives on attribute bindings (#49713)
6623810e4d	fix	Produce diagnositc if directive used in host binding is not exported (#49527)
compiler-cli
Commit	Type	Description
ed817e32fe	fix	Catch FatalDiagnosticError during template type checking (#49527)
core
Commit	Type	Description
f8e25864e8	fix	allow async functions in effects (#49783)
84216dabfc	fix	catch errors from source signals outside of .next (#49769)
2f2ef14f9e	fix	resolve InitialRenderPendingTasks promise on complete (#49784)
c7d8d3ee37	fix	toObservable should allow writes to signals in the effect (#49769)
http
Commit	Type	Description
15c91a53ae	fix	delay accessing pendingTasks.whenAllTasksComplete (#49784)
9f0c6d1ed1	fix	ensure new cache state is returned on each request (#49749)
2eb9b8b402	fix	wait for all XHR requests to finish before stabilizing application (#49776)
router
Commit	Type	Description
6193a3d406	fix	fix = not parsed in router segment name (#47332)
Special Thanks
Alan Agius, Alex Rickabaugh, Andrew Kushnir, Andrew Scott, Brandon Roberts, De Wildt, Jessica Janiuk, Joey Perrott, Kristiyan Kostadinov, Matthieu Riegler, Nikola Kološnjaji, Paul Gschwendtner, Pawel Kozlowski and dewildt
            """
    return fromInput


DolphinStream().pipe([
    getNews(),
    # chatGptPrompt('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')
    tap(lambda x: print(f"Entrada: {x}")),
    fakeChatGptPrompt(
        apiKey='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'),
    tap(lambda x: print(f"Salida: {x}")),
    googleTTS()
])
