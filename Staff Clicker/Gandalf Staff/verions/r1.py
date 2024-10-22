import socket
import pyautogui

# Server configuration
HOST = ''  # Empty string means all available interfaces
PORT = 12345

# Set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)  # Listen for incoming connections

print(f'Server listening on port {PORT}...')

try:
    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print(f'Connected by {client_address}')

        with client_socket:
            while True:
                # Receive data from the client
                data = client_socket.recv(1024)
                if not data:
                    # No more data from the client
                    break
                message = data.decode('utf-8').strip()
                print(f'Received: {message}')

                # Simulate keypress based on the message
                if message == 'RIGHT':
                    pyautogui.press('right')
                elif message == 'LEFT':
                    pyautogui.press('left')
                elif message == 'RANDOM':
                    pyautogui.press('f10')
                else:
                    print(f'Unknown command: {message}')

except KeyboardInterrupt:
    print('Server shutting down...')
finally:
    server_socket.close()
