import socket
import select

HOST = socket.gethostname()
PORT = 8000
socket_list = list()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(3)

socket_list.append(server)

def broadcast(server, client, msg):
    for sock in socket_list:
        if sock != server and sock != client:
            sock.send(msg.encode('utf-8'))
            

while True:
    ready_to_read,ready_to_write,in_error = select.select(socket_list, [], [], 0)
    for sock in ready_to_read:
        if sock == server:
            conn, addr = server.accept()
            socket_list.append(conn)
        else:
            clientMessage = (sock.recv(1024)).decode('utf-8')
            print(clientMessage)
            if clientMessage:
                broadcast(server, sock, clientMessage)
server.close()