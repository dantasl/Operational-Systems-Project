import socket
import logging
import datetime
from time import sleep


class ClientSocket(object):
    """
    This class represents the Socket of the client side.

    ...

    Attributes
    ----------
    sock : socket
        instance of the Python socket module

    Methods
    -------
    send_command(command)
        Sends to the server an instruction given by the user
    check_status()
        Keeps checking every 1 minute if the server send the status report
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
        self.sock.connect((host, port))
        # Configuring log file
        logging.basicConfig(filename='statusHouse.log', level=logging.DEBUG)

    def send_command(self, command):
        """Send a command to the socket server.

        After sending the command to the server, this function will receive
        the server response and print it to the user.

        Parameters
        ----------
        command : bytes
            The command spoken by the user.
        """

        self.sock.sendall(command)
        data = self.sock.recv(1024)
        print('Received: ', repr(data))
    
    def check_status(self):
        """Receive status of the "house" from the server.

        Every 60 seconds this function will receive the data sent by the server
        containing information about the house status (if lights on a room are
        turned on or off) and will write this into a log file called statusHouse.log
        """

        while True:
            sleep(60)
            now = datetime.datetime.now()
            data = self.sock.recv(1024)
            if data:
                logging.info("{}/{}/{} - {}:{}:{} -> {}".format(
                    now.day, now.month, now.year, now.hour,
                    now.minute, now.second, repr(data)
                ))
