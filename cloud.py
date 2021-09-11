import socket as sock
import sys 

serverSocket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
server_address = ('localhost',8080)
serverSocket.bind(server_address)
bufferSize = 1024

def splitMessage(message):
    formattedMessage = message.split('%')
    return formattedMessage


serverSocket.listen(1)
print('Il Cloud è in funzione, porta ',8080)

while True:

    print('\nIn attesa dei dati...')
    connectionSocket, addr = serverSocket.accept()
    print('\nConnectin Socket:', connectionSocket)
    print('Address:', addr)

    try:
        print("Dimensione del buffer di trasmissione: %d" %bufferSize)
        message = connectionSocket.recv(bufferSize)
        message = splitMessage(message.decode('utf8'))
        print("Dati ottenuti dai Device:")
        for i in range(1, len(message)):
            print("    Device %s : %s" %(i, message[i]))
        connectionSocket.send("Received".encode())
        connectionSocket.close()
    except Exception as message:
        print(Exception,":",message)
        print("Connessione fallita\r\n")
        sys.exit(0)

