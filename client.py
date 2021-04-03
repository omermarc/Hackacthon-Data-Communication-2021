from socket import *
import scapy
import struct
import msvcrt
import time


BUFFER_SIZE = 2048


def startUdpSocket(port):
    """
    Create UDP socket and receive message
    """
    global BUFFER_SIZE
    UDPclientSocket = socket(AF_INET, SOCK_DGRAM)
    UDPclientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    UDPclientSocket.bind(('', port))
    print("Client started, listening for offer requests... ")
    msg_from_server, serverAddress = UDPclientSocket.recvfrom(BUFFER_SIZE)
    msg = struct.unpack('Ibh', msg_from_server)
    if msg[0] != 0xfeedbeef or msg[1] != 0x2:
        print('unvalid message received from server: ' + str(msg))
        return False
    print('Received offer from ' + serverAddress[0] + ', attempting to connect on port ' + str(msg[2]))
    port = msg[2]
    UDPclientSocket.close()
    return (serverAddress[0], port)


def createTcpSocket(server_ip, port, team_name):
    """
    create TCP socket
    """
    global BUFFER_SIZE
    TCPclientSocket = socket(AF_INET, SOCK_STREAM)
    TCPclientSocket.connect(('localhost', port))  # CHANGE TO server_ip TO RUN LOCALLY
    TCPclientSocket.send((team_name +  '\n').encode())
    message = TCPclientSocket.recv(BUFFER_SIZE).decode()
    print(message)
    return TCPclientSocket


def collectChars(socket):
    """
    collect keyboard inputs and send it to the server
    """
    global BUFFER_SIZE
    limit = time.time() + 10
    while time.time() < limit:
        if msvcrt.kbhit():
            c = msvcrt.getch()
            socket.send(c)
    winners = socket.recv(BUFFER_SIZE)
    print(winners.decode())


team_name = 'smelly_cat'
udpPort = 13117

while True:
    time.sleep(0.5)
    serverAns = startUdpSocket(udpPort)
    if serverAns != False:
        serverIp = serverAns[0]
        tcpServerPort = serverAns[1]
        tcpSocket = createTcpSocket(serverIp, tcpServerPort, team_name)
        collectChars(tcpSocket)
