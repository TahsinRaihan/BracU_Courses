import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)

print("Server is waiting for a connection...")

client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address}")

hours_worked = float(client_socket.recv(1024).decode())

if hours_worked <= 40:
    salary = hours_worked * 200
else:
    salary = 8000 + (hours_worked - 40) * 300

salary_message = f"Salary is Tk {int(salary)}"

client_socket.send(salary_message.encode())

client_socket.close()
server_socket.close()
