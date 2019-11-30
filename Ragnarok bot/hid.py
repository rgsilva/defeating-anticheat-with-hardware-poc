#!/usr/bin/env python3

import time
import math
import socket

######################################################################################
#
# Byte 0: xxxxxLMR
# Byte 1: least significant bits of X
# Byte 2: most significant bits of X
# Byte 3: least significant bits of Y
# Byte 4: most significant bits of Y
#
######################################################################################

class UdpHid:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  def convert(self, value):
    pairs = list(divmod(abs(value), 1<<8))
    if value < 0 and value < 256:
      pairs[0] = 255
      pairs[1] = 256 - pairs[1]
    return bytearray((pairs[1], pairs[0]))


  def expand_buttons(self, values):
    (left, middle, right) = values
    buttons = bytearray(1)
    if left:
      buttons[0] |= 0b00000001
    if middle:
      buttons[0] |= 0b00000010
    if right:
      buttons[0] |= 0b00000100
    return buttons


  def write(self, buttons, x, y):
    ba_buttons = self.expand_buttons(buttons)
    ba_x = self.convert(x)
    ba_y = self.convert(y)
    data = ba_buttons + ba_x + ba_y
    #print("X =", x, "Y =", y, "Size =", len(data), "Data =", list(data), data)
    self.socket.sendto(data, (self.host, self.port))
