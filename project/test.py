from email.base64mime import body_encode
from re import X
from tkinter import N
import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

import compare
import bounding_box

for i in range(3) :
    bounding_box.bounding_box('entire', i)
bounding_box.bounding_box('inner', 0)

compare.compare(3, 3, 0.7)