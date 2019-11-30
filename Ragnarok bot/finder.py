import cv2
import numpy as np
import json
import windows
import time

from PIL import ImageGrab
from matplotlib import pyplot as plt

#ALGORITHM = cv2.TM_SQDIFF_NORMED
ALGORITHM = cv2.TM_CCOEFF_NORMED
#ALGORITHM = cv2.TM_CCORR_NORMED

USE_GRAY = False

MIN_CONFIDENCE = {
  cv2.TM_SQDIFF_NORMED: 0.40,
  cv2.TM_CCOEFF_NORMED: 0.70,
  cv2.TM_CCORR_NORMED: 0.55,
}

USE_MIN = ALGORITHM in [cv2.TM_SQDIFF_NORMED]

class Finder:
  def __init__(self, template_path):
    template = cv2.imread(template_path)
    if USE_GRAY:
      template = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)

    self.templates = [template, cv2.flip(template, 1)]

    shape = template.shape[0:2][::-1]
    self.width = shape[0]
    self.height = shape[1]


  def find(self, screenshot=None):
    # Screenshot it.
    if screenshot is not None:
      source = screenshot
    else:
      source = np.array(ImageGrab.grab(bbox=(0, 0, 1024, 768)))
    if USE_GRAY:
      source = cv2.cvtColor(source, cv2.COLOR_RGB2GRAY)

    index = 0
    for template in self.templates:
      # Extract the match and its values
      match = cv2.matchTemplate(source, template, ALGORITHM)
      (minval, maxval, minloc, maxloc) = cv2.minMaxLoc(match)

      # Extract confidence and position
      confidence = minval if USE_MIN else maxval
      pos = minloc if USE_MIN else maxloc
      print("  DEBUG", "index:",index, "confidence:", confidence, "position:", pos)

      if confidence >= MIN_CONFIDENCE[ALGORITHM]:
        #self.show(source, template, match, pos)
        return (confidence, pos)

      index += 1
    return (None, None)
        

  def cursor(self):
    return windows.mouse_pos()


  def show(self, source, template, match, pos):
    top_left = pos
    (w, h) = template.shape[0:2]
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cropped = source[pos[1]:bottom_right[1], pos[0]:bottom_right[0]]
    cv2.imshow("cropped", cropped)
    cv2.waitKey(0)
