import queue
import json

import pyttsx3
import sounddevice as sd
import vosk

from utils import SocketConnector

settings = json.load(open('settings.json'))


voice_engine = pyttsx3.init()
voices = voice_engine.getProperty('voices')

voice_engine.setProperty('voice', voices[settings['voice_id']].id)

device = 0
device_info = sd.query_devices(device, 'input')
samplerate = int(device_info['default_samplerate'])
model = vosk.Model(settings['vosk_path'])

q = queue.Queue()

mic_blocked = False

connector = SocketConnector(settings['main_ip'], settings['voice_in'], settings['voice_out'], buffer_size=settings['voice_buffer_size'])

def callback(indata, frames, time, status):
    if status:
        print(status)
    if not mic_blocked:
        q.put(bytes(indata))


with sd.RawInputStream(samplerate=samplerate, blocksize = 8000, device=device, dtype='int16',
                               channels=1, callback=callback):
    rec = vosk.KaldiRecognizer(model, samplerate)
    while True:
        recieved = connector.recieve_str()
        if recieved != '':
            voice_engine.say(recieved)
            voice_engine.runAndWait()

        data = q.get()
        if rec.AcceptWaveform(data):
            recognized_data = rec.Result()
            recognized_data = json.loads(recognized_data)
            voice_input_str = recognized_data["text"]
            if voice_input_str != "":
                print(voice_input_str)
                mic_blocked = False
                connector.send_text(voice_input_str)
        else:
            pass
