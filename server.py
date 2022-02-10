import socket
import os


SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000
public_dir = "public"
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

while True:
    
        client_connection, client_address = server_socket.accept()

        # Get the client request
        request = client_connection.recv(1024).decode()
        route = request.split('\n\r')[0].split(' ')[1]
        
        match route:
            case "/":
                content = "main page"
            case "/about":
                content = "this is about me"
            case _:
                public_files = [file for file in os.listdir(f"./{public_dir}")]
                if route.replace("/","") in public_files:
                    f = open(f"./public/{route}", 'r')
                    content = f.read()
                    f.close()
                else:
                    content = "page not found"

        
        # Send HTTP response
        response = f'HTTP/1.0 /a OK\n\n{content}'

        client_connection.sendall(response.encode())
        client_connection.close()

