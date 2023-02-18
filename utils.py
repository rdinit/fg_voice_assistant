import socket
import struct
import requests

class SocketConnector():
    protocol = ''
    def __init__(self, ip, input_port, output_port, in_protocol='', out_protocol='', buffer_size=1024) -> None:
        self.input_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.input_socket.bind(('', input_port))
        self.input_socket.settimeout(0.002)

        self.output_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.output_socket.connect((ip,output_port))

        self.in_protocol = in_protocol
        self.out_protocol = out_protocol
    
    def send_text(self, data) -> None:
        new_data = bytes(str(data), 'utf-8')
        self.output_socket.send(new_data)
    
    def recieve_str(self):
        try:
            data,_ = self.input_socket.recvfrom(1024)
            return str(data, encoding='utf-8')
        except TimeoutError:
            return ''
    
    def send(self, data) -> None:
        new_data = struct.pack(self.out_protocol, *data)
        self.output_socket.send(new_data)
    
    def recieve(self):
        try:
            data,_ = self.input_socket.recvfrom(1024)
            return struct.unpack(self.in_protocol, data)
        except TimeoutError:
            return None

class JsonConnctor():
    url = ''
    '''
    Example:
    JsonConnctor.send([{'name': '/controls/gear/gear-down', 'value': 0}])
    '''
    def __init__(self,ip,port):
        self.url = f'http://{ip}:{port}/json/'
    
    def send(self, props:dict):
        try:
            requests.post(self.url, json={"children":props}, timeout=0.5)
        except requests.exceptions.ConnectTimeout:
            pass