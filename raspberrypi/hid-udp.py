import socket
import sys

UDP_IP = "0.0.0.0"
UDP_PORT = 60123

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

dev = open(sys.argv[1], "wb")
while True:
  data, addr = sock.recvfrom(128)
  print("RECV", addr, data)
  dev.write(data)
  dev.flush()
