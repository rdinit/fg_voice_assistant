
import socket
from time import sleep
from text_to_num import text2num
import requests
from utils import SocketConnector

# this file not needed
fg_port = 8080
url = 'http://localhost:8081/json/'


def get_data_from_fg():
    #data = requests.get(url + 'position').json()['children']
    #lat,lon,alt = data[1]['value'], data[0]['value'],data[2]['value']
    return float(requests.get(url + 'position/altitude-agl-ft').json()['value'])/3.281
    
#alt = [120 100 оценка 80
cur_speed = 0
def update_speed():
    global cur_speed
    speed = float(requests.get(url + 'velocities/airspeed-kt').json()['value']) * 1.852
    speed_positions = [140, 160, 180, 200, 220]#, рубеж, подъем, безопасная]
    if speed > speed_positions[cur_speed]:
        cur_speed += 1
        return speed_positions[cur_speed-1]
    return ""



if __name__ == "__main__":
    connector = SocketConnector(5702, 5701)

    connector.send_text('привет')
    while True:
        #alt = get_data_from_fg()
        connector.send_text(input())#update_speed())
    print(text2num('сто пятьдесят ывдалор ывадлроывдплр вдаплр вдлопор в', 'ru'))

