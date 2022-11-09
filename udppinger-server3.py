# We will need the following module to generate randomized lost packets
import random
import time
import sys

# Import socket module
from socket import *

# Prepare a sever socket
# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.setblocking(0)

# Assign IP address and port number to socket
serverSocket.bind(('', 12000))

last_time = time.perf_counter()
cur_time = time.perf_counter()
last_seq = 0
cur_seq = 0
diff = 0

while True:
    # Generate random number in the range of 0 to 10
    rand = random.randint(0, 10)

    # Receive the client packet along with the address it is coming from
    message = None
    address = None
    try:
        message, address = serverSocket.recvfrom(1024)
    except BlockingIOError:
        pass

    # If rand is less is than 4, we consider the packet lost and do not respond
    if rand < 4:
        continue

    # Part 3 code for UDP Heartbeat should be implemented after this line
    s = ""
    if message is not None:
        s = message.decode()
        last_time = cur_time
    cur_time = time.perf_counter()
    diff = cur_time - last_time
    if diff > 30:
        print("Server timed out")
        sys.exit()
    last_seq = cur_seq
    if s != "":
        cur_seq = int(s.split()[1])
        print(f"Recieved {cur_seq}, diff={diff:.5f}s")
    if cur_seq > last_seq+1:
        for i in range(last_seq+1, cur_seq):
            print(f"Packet {i} lost.")

    # Otherwise, capitalize the message from the client
    # The server responds
    if message is not None and address is not None:
        message = message.upper()
        serverSocket.sendto(message, address)

