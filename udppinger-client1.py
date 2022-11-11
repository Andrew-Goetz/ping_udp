from socket import *
import time
import datetime

start_time = time.perf_counter()
sock = socket(AF_INET, SOCK_DGRAM)
sock.settimeout(1)
counter = 0

# This program will send a UDP packet to the server every 3 seconds.
# and wait for a resonse. If no response is received within 3 seconds the packet times out.
while True:
    curtime = datetime.datetime.now()

    # End after two minutes
    if (time.perf_counter() - start_time) > 120:
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
    except timeout:
        print("Request timed out.")
    time.sleep(3)


print("Done Pinging")
