import random

from time import sleep
from os import listdir
from os.path import isfile, join
from PIL import Image

from finder import Finder
from hid import UdpHid

import numpy as np
from PIL import ImageGrab

TARGET_HOST = "000.000.000.000"
TARGET_PORT = 60123

def direction(value):
  return +1 if value < 0 else -1


def spread(values, size):
  skip = int(size/len(values))
  newvalues = []
  values_i = 0
  for i in range(0, size):
    if i % skip == 0:
      newvalues.append(values[values_i] if values_i < len(values) else values[len(values) - 1])
      values_i += 1
    else:
      newvalues.append(newvalues[i-1])
  return newvalues


def same_size(x, y):
  if len(x) == len(y):
    return (x, y)
  elif len(x) > len(y):
    return (x, spread(y, len(x)))
  else:
    return (spread(x, len(y)), y)


def skip(values, skip):
  newvalues = []
  for i in range(0, len(values)):
    if i % (skip+1) == 0:
      newvalues.append(values[i])
  return newvalues

########################################################

WIDTH = 1920 * 2
HEIGHT = 1080
MAXVAL = 32767
SKIP = 5

MOB_PATHS = [
  "images/poring/",
  "images/lunatic/",
  "images/drops/",
]

MOBS = []
for mob_path in MOB_PATHS:
  MOBS += list(join(mob_path, f) for f in listdir(mob_path) if isfile(join(mob_path, f)))
print("Mobs loaded:", MOBS)

mouse = UdpHid(TARGET_HOST, TARGET_PORT)
mob_finders = list((mob, Finder(mob)) for mob in MOBS)


xstep = (MAXVAL/WIDTH)
ystep = (MAXVAL/HEIGHT)
print("X step:", xstep, "Y step:", ystep)


def move_to(mob_finder, cur, pos):
  global mouse

  print("Moving cursor position")
  mob_width = mob_finder.width if mob_finder is not None else 0
  mob_height = mob_finder.height if mob_finder is not None else 0
  xrange = list(range(cur[0], pos[0] + int(mob_width/2), direction(cur[0] - pos[0])))
  yrange = list(range(cur[1], pos[1] + int(mob_height/2), direction(cur[1] - pos[1])))
  if len(xrange) == 0 or len(yrange) == 0:
    return
  (xrange, yrange) = same_size(xrange, yrange)
  (xrange, yrange) = (skip(xrange, SKIP), skip(yrange, SKIP))
  for i in range(0, len(xrange)):
    mouse.write((False, False, False), int(xrange[i] * xstep), int(yrange[i] * ystep))
  for i in range(0, 2):
    print("Clicking", i)
    mouse.write((True, False, False), int(xrange[(len(xrange) - 1)] * xstep) , int(yrange[(len(yrange) - 1)] * ystep))
    sleep(0.150)
    mouse.write((False, False, False), int(xrange[(len(xrange) - 1)] * xstep) , int(yrange[(len(yrange) - 1)] * ystep))
    sleep(0.150)


def take_screenshot():
  return np.array(ImageGrab.grab(bbox=(0, 0, 1024, 768)))


def run():
  global mob_finders

  screenshot = take_screenshot()

  results = []
  for (mob, mob_finder) in mob_finders:
    print("Search mob:", mob)
    (confidence, pos) = mob_finder.find(screenshot)
    if confidence is None:
      print("  Mob not found:", mob)
      continue
    print("  Mob position:", pos)
    results.append((confidence, pos, mob))

  if len(results) == 0:
    print("No mobs found")
    return False

  best_result = sorted(results, key = lambda x: x[0], reverse=True)[0]
  print("Best result:", best_result)

  cur = mob_finder.cursor()
  print("Cursor position:", cur)
  move_to(mob_finder, cur, best_result[1])
  return True

  
while True:
  found = run()
  print("")
  if found:
    sleep(2.0)
  else:
    sleep(0.5)