from socket import *
import select
import time
import datetime

sock = socket(AF_INET, SOCK_DGRAM)
sock.setblocking(0)
counter = 1

while True:
    start = time.perf_counter()
    curtime = datetime.datetime.now()
    message = "Ping " + str(counter) + " " + str(curtime.strftime('%H:%M:%S'))

    print(f"Sending message {message}")
    counter += 1
    
    sock.sendto(str.encode(message), ("127.0.0.1", 12000))
    
    ready = select.select([sock], [], [], 120)
    if not ready[0]:
        print("Request timed out.")
        time.sleep(3)
        continue
    
    received = sock.recv(1024)
    end = time.perf_counter()
    
    print(f"Recieved message {received.decode()}. RTT={end-start:.5f}s")

    time.sleep(3)
