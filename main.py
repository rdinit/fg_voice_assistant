from utils import SocketConnector, JsonConnctor
from t154ru import Addon
import json

settings = json.load(open('settings.json'))


addon = Addon()

voice_connector = SocketConnector(settings['voice_ip'], settings['voice_out'], settings['voice_in'])
sim_connector = SocketConnector(settings['fg_ip'], settings['fg_out'], settings['fg_in'], in_protocol=addon.INPUT_PROTOCOL, out_protocol=addon.OUTPUT_PROTOCOL)
json_sim_connector = JsonConnctor(settings['fg_ip'], settings['fg_phi'])


voice_connector.send_text('Hello')
while True:
    voice_text = voice_connector.recieve_str()
    addon.update_voice(voice_text)
    addon.update(sim_connector.recieve())[1]
    json_sim_connector.send(addon.get_props2post())
    text = addon.get_text()
    if text != '':
        print(text)
        voice_connector.send_text(text)


#
# import subprocess
# subprocess.run("python3 voice_interface.py & python3 main.py", shell=True)
#