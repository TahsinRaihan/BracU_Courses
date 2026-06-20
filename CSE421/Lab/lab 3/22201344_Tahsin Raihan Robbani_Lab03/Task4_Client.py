import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

hours_worked = float(input("Enter the number of hours worked: "))

client_socket.send(str(hours_worked).encode())

salary = client_socket.recv(1024).decode()

print("Calculated Salary:", salary)

client_socket.close()
