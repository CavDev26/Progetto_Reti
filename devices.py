import socket
import time
import random
from datetime import datetime

def generateFile(deviceNr):
    file = open("Device_" + str(deviceNr+1) + ".txt", "w+")
    ip = ips[deviceNr]
    date = datetime.now().strftime("%H:%M:%S")
    temperature = random.randint(0, 40)
    humidity = random.randint(45, 90)

    dataList = [date, temperature, humidity]
    for elem in dataList:
        ip = ip + '-' + str(elem)
    file.write(ip)
    return file  

ips = ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4']
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 10000)
bufferSize = 4096
while True:
    time.sleep(10)
    try:
        for i in range(4):
            print('Device ' + str(i+1) + ':')
            startingTime = time.time()  
            file = generateFile(i)
            file.seek(0)
            sent = socket.sendto(file.read().encode(), server_address)
            file.close()
            print("Dimensione del buffer di trasmissine: %d" %bufferSize)
            data, server = socket.recvfrom(bufferSize)
            print('Messaggio ricevuto:  "%s"' % data.decode('utf8'))
            print("La trasmissione ha impiegato %g secondi\n" %(time.time() - startingTime))
        
    except Exception as info :
        print(info)
