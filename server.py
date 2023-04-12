import socket
import threading

socketServer = socket.socket()

host = socket.gethostname()
port = 5000

socketServer.bind((host, port))

socketServer.listen(2)

conn1, address1 = socketServer.accept()

# def send():
#     while(data != "exit"):
#         data = input()
#         conn1.send(data.encode())

# def receive():
#     while(data != "exit"):
#         data = conn1.recv(512).decode()
#         print("=> ", data)

# t1 = threading.Thread(target = send)
# t2 = threading.Thread(target = receive)

# t1.start()
# t2.start()

# t1.join()
# t2.join()


conn2, address2 = socketServer.accept()

def send(fromConnection, toConnection):
    while(True):
        data = fromConnection.recv(512).decode()
        toConnection.send(data.encode())

t1 = threading.Thread(target = send, args = (conn1, conn2))
t2 = threading.Thread(target = send, args = (conn2, conn1))

t1.start()
t2.start()

t1.join()
t2.join()

conn1.close()
conn2.close()