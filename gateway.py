import socket as sk
import sys
import time

sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
surveys = {}
cloudBufferSize = 1024
deviceBufferSize = 4096
gateway_ip = '10.10.10.1'

def sendToCloud():
    header = gateway_ip
    for elem in surveys.keys():
        header = header + '%' + elem + '-' + surveys[elem]
    try:
        clientsocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        clientsocket.connect(('localhost',8080))
        startingTime = time.time()
    except Exception as data:
        print (Exception,":",data)
        print ("Connessione Fallita\r\n")
        sys.exit(0)
    clientsocket.send(header.encode())
    response = clientsocket.recv(cloudBufferSize)
    print (response)
    print ("Dimensione del Buffer di trasmissione: %d" %cloudBufferSize)
    print ("Tempo impiegato per trasmettere il pacchetto al cloud: %g secondi" %(time.time() - startingTime))
    clientsocket.close()
   
def formatData(received):
    formatted = received.split("-")
    print ('Messaggio ricevuto dal Device (splittato): ', received)
    surveys[formatted[0]] = received[received.index("-")+1:]
    print('Surveys: ', surveys)
    return "ACK"
    
server_address = ('localhost', 10000) 
print ('\n\r %s, porta %s' % server_address)
sock.bind(server_address)
 
while True:
    print('\n\rIn attesa di un messaggio...')
    print("Dimensione del Buffer di trasmissione: %d" %deviceBufferSize)
    data, address = sock.recvfrom(deviceBufferSize)
    data1 = formatData(data.decode('utf8'))
    if data:
        sent = sock.sendto(data1.encode(), address)
    if len(surveys) == 4:
        print("Ho ricevuto i dati da tutti e quattro i dispositivi, invio al Cloud...")
        sendToCloud()
        surveys.clear()
         


    