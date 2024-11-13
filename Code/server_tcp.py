import sys
import socket
import os
from _thread import *

def change_alarm(variable, value):

    if float(value) <= 0:
        return "Invalid value"

    with open("./alarms.txt", "r") as file:
        for line in file:
            data = line.split()

    if variable == "TEMP":
        data[0] = value

    elif variable == "SOUND":
        data[1] = value
    
    elif variable == "LUMINOSITY":
        data[2] = value

    elif variable == "PRESSURE":
        data[3] = value
    
    info = " ".join(data)

    print(info)

    with open("./alarms.txt", "w") as file:
        file.write(info)

def change_source(source):
    with open("./temp_source.txt", "w") as file:
        file.write(str(source))
        


ThreadCount = 0
Client_number = 0

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <host> <port>")
    sys.exit(1)
    
host, port = sys.argv[1], int(sys.argv[2])
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))
    sys.exit(1)
    
print(f'Socket is listening in address {host} and port {port} ...')
ServerSocket.listen(5)

def multi_threaded_client(connection, cli_n):
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(2048)

        received = data.decode('utf-8')

        received = received.split("_")

        if received[0] == "help":
            response = "Possible commands:\n\nZone# (zone1 or zone2 - change the zone from where the temperature is measured)\nT_VAR_VALUE (VAR = [TEMP, SOUND, LUMINOSITY, PRESSURE] - changes the alarm threshold)"
        
        elif received[0] == "T":

            if received[1] in ["TEMP", "SOUND", "LUMINOSITY", "TEMPERATURE"]:
                change_alarm(received[1], received[2])
                response = (f"Value {received[2]} set for {received[1]} alarm")
            
            else:
                response = (f"Invalid argument: {received[1]}. Type help to find the available commands")
        
        elif received[0] == "Zone1":
            change_source(0)
            response = "Source changed"

        elif received[0] == "Zone2":
            change_source(1)
            response = "Source changed"

        else:
            response = f"Invalid argument: {received[0]}. Type help to find the available commands." 

        if not data:
            break
        connection.sendall(str.encode(response))
    print('Bye bye Client ' + str(cli_n) + '!')
    connection.close()

try:
    while True:
        Client, address = ServerSocket.accept()
        Client_number +=1
        print('Connected to Client ' + str(Client_number) + ', calling from: ' + address[0] + ':' + str(address[1]))
        start_new_thread(multi_threaded_client, (Client, Client_number,))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
        
except KeyboardInterrupt:
    print("\nCaught keyboard interrupt, exiting")
finally:
    ServerSocket.close()
