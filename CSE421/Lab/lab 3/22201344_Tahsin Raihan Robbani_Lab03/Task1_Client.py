import socket
import platform

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

ip_address = socket.gethostbyname(socket.gethostname())
device_name = platform.node()

message = f"{ip_address} {device_name}"
client_socket.send(message.encode())

client_socket.close()
