import threading
import voice
from client_socket import ClientSocket


def voice_command(clientsocket):
    """Show available commands and send user choice to the server.

    This function will (until terminated by the user) show the available
    set of commands provided by the application. It then will call another
    function to listen and treat the user audio input. After this, it will
    check the response for errors and listen again in case it find any of them.
    Then, this function will print the audio command translated to text and will
    send this data to the server.

    Parameters
    ----------
    clientsocket : ClientSocket
        Instance of the class that handles socket connections on the client side.
    """

    while True:
        try:
            text = input("\nHit ENTER for a new command.\nCTRL + C to quit.\n")
            if text == "":
                # Showing first instructions
                print(voice.get_options())

                # Listening from microphone
                sentence = voice.listen_sentence_from_mic(voice.recognizer, voice.microphone)

                # Checking for errors
                while sentence["error"]:
                    print("ERROR: {}".format(sentence["error"]))
                    print("Say something: ")
                    sentence = voice.listen_sentence_from_mic(voice.recognizer, voice.microphone)

                # Print sentence
                print("Your command was: {}".format(sentence["transcription"]))

                # Sending command via socket
                clientsocket.send_command(sentence["transcription"].encode())
        except (KeyboardInterrupt, SystemExit):
            print("\n\nYou've finished this program. Thanks for using it. ;)")
            break


if __name__ == "__main__":
    host = "10.7.119.20"
    port = 6000

    # Creates an instance of the class that handles sockets
    client_socket = ClientSocket(host, port)

    # Creating thread to send instructions to the server
    voice_command_thread = threading.Thread(target=voice_command, args=(client_socket,))

    # Creating thread to check the status sent by the server
    checking_thread = threading.Thread(target=client_socket.check_status)

    # Starting all threads
    voice_command_thread.start()
    checking_thread.start()
