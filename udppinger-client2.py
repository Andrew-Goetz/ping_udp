from socket import *
import select
import time
import datetime
import sys


sock = socket(AF_INET, SOCK_DGRAM)
sock.setblocking(0)
counter = 1

loss_counter = 0

rttList = []

try:
    while True:
        start = time.perf_counter()
        curtime = datetime.datetime.now()
        message = "Ping " + str(counter) + " " + str(curtime.strftime('%H:%M:%S'))
    
        counter += 1
        print(f"Sending message {message}")
        
        sock.sendto(str.encode(message), ("127.0.0.1", 12000))
        
        ready = select.select([sock], [], [], 120)
        if not ready[0]:
            print("Request timed out.")
            loss_counter += 1
            time.sleep(3)
            continue
        
        received = sock.recv(1024)
        end = time.perf_counter()
        
        print(f"Recieved message {received.decode()}. RTT={end-start:.5f}s")
        rttList.append(end-start)
    
        time.sleep(3)

except KeyboardInterrupt:
    minimum = min(rttList) if len(rttList) > 0 else 0
    maximum = max(rttList) if len(rttList) > 0 else 0
    total = len(rttList)

    loss_rate = (loss_counter/(counter-1)) * 100

    avg = sum(rttList)/len(rttList) if len(rttList) > 0 else 0

    print(f"rtt min/max/total/loss_rate/avg: {minimum:.5f}s/{maximum:.5f}s/{total}/{loss_rate:.2f}%/{avg:.5f}s")
    sys.exit()
