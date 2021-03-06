# Server
import socket
import cv2
import numpy
import time
from datetime import datetime

now = datetime.now()
cascadefile = "haarcascade_frontalface_default.xml"
cascade = cv2.CascadeClassifier(cascadefile)

def detect(gray, decimg):
    faces = cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(decimg, (x, y, w, h), (0, 255, 0), 3)
        print('('+str((x+w)/2)+', '+str(h)+')')
        
    return decimg

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


TCP_IP = ''
TCP_PORT = 8000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((TCP_IP, TCP_PORT))
server_socket.listen()
print('Listening')

conn, addr = server_socket.accept()

cnt=1
while True:
    start = time.time()
    length = recvall(conn, 16)
    stringData = recvall(conn, int(length))
    data = numpy.frombuffer(stringData, dtype='uint8')
    decimg = cv2.imdecode(data, 1)

    gray = cv2.cvtColor(decimg, cv2.COLOR_BGR2GRAY)
    process=detect(gray, decimg)

    cv2.imshow('SERVER', process)
    end = time.time()

    if cnt == 1 :
        hour = now.hour
        minute = now.minute
        second = now.second
        cnt=cnt+1

    
    difftime =  end - start;
    second = difftime + second
    print("time : ", format(difftime,'.6f'), "//",hour,"시 ",minute,"분 "
          ,format(second,'.6f'),"초")

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

server_socket.close()
cv2.destroyAllWindows()
