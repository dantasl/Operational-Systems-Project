import socket
import threading
import board_assets as assets
from time import sleep

HOST = "192.168.0.24"
PORT = 6001


class VocalServer(object):
    """
    This class represents the server of the Vocal application.

    ...

    Attributes
    ----------
    sock : socket
        instance of the Python socket module

    Methods
    -------
    listen()
        Listen for clients requests and creates threads to handle their requests.
    send_status()
        Sends to the client every 1 minute the status of the house.
    listen_client()
        Receives the commands sent by the user and performs the requested action.
    """

    def __init__(self, host, port):
        """
        Parameters
        ----------
        host : str
            IP address to connect (e.g. "192.168.0.24")
        port : int
            Number of the port to establish connection (e.g. 6000)
        """

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))

    def listen(self):
        """Listen to the maximum of 3 clients and creates threads to handle their requests."""

        self.sock.listen(3)
        while True:
            client, address = self.sock.accept()
            threading.Thread(target=self.listen_client, args=(client,)).start()
            threading.Thread(target=self.send_status, args=(client,)).start()

    def send_status(self, client):
        """Send status of the house to the client every 60 seconds.

        Parameters
        ----------
        client : socket
            Socket instance of a new client.
        """

        while True:
            sleep(60)
            try:
                print("Sending status: {}".format(assets.compose_status()))
                client.send(assets.compose_status().encode())
            except:
                client.close()
                return False    

    def listen_client(self, client):
        """Receives the data from the client.

        Get the data from the client in chunks of 1024 bytes and calls the function
        for decoding the instruction. After this, sends back to the user information
        telling if the command was performed or not.

        Parameters
        ----------
        client : socket
            Socket instance of a new client.
        """

        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    # Set the response to echo back the recieved data 
                    print("Instruction: {}".format(data))
                    if assets.decode_command(data): 
                        client.send(b'COMMAND PERFORMED.')
                    else:
                        client.send(b'ERROR WHILE PERFORMING COMMAND.')
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False


if __name__ == "__main__":
    assets.init_leds()
    VocalServer(HOST, PORT).listen()
