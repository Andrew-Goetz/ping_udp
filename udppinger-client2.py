from socket import *
import select
import time
import datetime
import sys

start_time = time.perf_counter()
sock = socket(AF_INET, SOCK_DGRAM)
sock.settimeout(1)
counter = 0

loss_counter = 0

rttList = []

try:
   while True:
    curtime = datetime.datetime.now()

    # End after two minutes
    if (time.perf_counter() - start_time) > 12:
        break

    counter += 1
    message = f"Ping {counter} {curtime.strftime('%H:%M:%S')}"
    print(f"Sending \"{message}\"")
    
    # Start - Send packet
    start = time.perf_counter()
    sock.sendto(message.encode('utf-8'), ("127.0.0.1", 12000))
    
    # Wait for response
    try:
        data, server = sock.recvfrom(1024)
        response = data.decode('utf-8')

        end = time.perf_counter()
        print(f"Received \"{response}\" in {end - start:0.4f} seconds")
        rttList.append(end - start)
    except timeout:
        print("Request timed out.")
        loss_counter += 1
    time.sleep(3)

except KeyboardInterrupt:
    pass

minimum = min(rttList) if len(rttList) > 0 else 0
maximum = max(rttList) if len(rttList) > 0 else 0
total = len(rttList)

loss_rate = (loss_counter/(counter)) * 100

avg = sum(rttList)/len(rttList) if len(rttList) > 0 else 0

print(f"rtt min/max/total/loss_rate/avg: {minimum:.4f}s/{maximum:.4f}s/{total}/{loss_rate:.1f}%/{avg:.4f}s")
sys.exit()
