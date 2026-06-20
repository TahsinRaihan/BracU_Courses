import socket
import threading

def handle_client(client_socket, client_address):
    print(f"Connection from {client_address}")
    
    message = client_socket.recv(1024).decode()

    vowels = "aeiouAEIOU"
    vowel_count = 0

    for char in message:
        if char in vowels:
            vowel_count += 1

    if vowel_count == 0:
        response = "Not enough vowels"
    elif vowel_count <= 2:
        response = "Enough vowels I guess"
    else:
        response = "Too many vowels"

    client_socket.send(response.encode())

    client_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)

print("Server is waiting for a connection...")

while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
