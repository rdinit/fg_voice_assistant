from utils import SocketConnector, JsonConnctor
from t154ru import Addon


addon = Addon()

voice_connector = SocketConnector('127.0.0.1', 5702, 5701)
sim_connector = SocketConnector('127.0.0.1', 5703, 9999, in_protocol=addon.INPUT_PROTOCOL, out_protocol=addon.OUTPUT_PROTOCOL)
json_sim_connector = JsonConnctor('127.0.0.1', 8081)


voice_connector.send_text('Привет')
while True:
    voice_text = voice_connector.recieve_str()
    addon.update_voice(voice_text)
    addon.update(sim_connector.recieve())[1]
    json_sim_connector.send(addon.get_props2post())
    text = addon.get_text()
    if text != '':
        print(text)
        voice_connector.send_text(text)