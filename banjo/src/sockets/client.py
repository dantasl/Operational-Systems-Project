import socket

HOST = '192.168.0.23'  # Standard loopback interface address (localhost)
PORT = 65432           # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    with open("instructions.txt", "r") as f:
        instruction = f.readline().strip()
        while instruction == "":
            instruction = f.readline().strip()
    s.sendall(bytes(instruction, encoding='utf-8'))
    data = s.recv(1024)

print('Server response:', repr(data))
