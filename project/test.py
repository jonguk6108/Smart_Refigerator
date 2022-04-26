from email.base64mime import body_encode
from re import X
from tkinter import N
import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

import compare
import bounding_box

inner_product_number = bounding_box.bounding_box('inner', 0)
outer_product_number = 3
for i in range(outer_product_number) :
    bounding_box.bounding_box('entire', i)
inner_product_number = bounding_box.bounding_box('inner', 0)

matching_list_inner = [-1 for col in range(inner_product_number)]
matching_list_outer = [-1 for col in range(outer_product_number)]
compare.compare(3, 3, 0.7, matching_list_inner, matching_list_outer)

print("\n\nmatching_list : ")
print(matching_list_inner)
print(matching_list_outer)