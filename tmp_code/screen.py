import tkinter as tk
import picamera
from PIL import Image, ImageTk

import time
state= 1
pic_number = 0
camera = picamera.PiCamera()
def camera_start():
    global state
    state += 1 
    camera.resolution=(800, 400)
    camera.start_preview(fullscreen=False, window=(0, 0, 800, 400))
def camera_capture():
    global pic_number
    pic_number += 1
    camera.capture('/home/pi/Desktop/image_' + str(pic_number) + '.jpg')
    camera.stop_preview()
    root.destroy()
def OCR_OK():
    #move to next state
    label2 = tk.Label(button_frame, text ="move to next state", font = 30)
    label2.grid(row =0, column = 0)
    global state
    state +=1
    root.destroy()
def OCR_reject():
    global state
    state = 1
    global pic_number
    pic_number -= 1
    root.destroy()
def Entire_continue():
    global state
    state = 4
    root.destroy()
def Entire_reject():
    global state
    state = 4
    global pic_number
    pic_number -= 1
    root.destroy()
def Entire_finish():
    global state
    state = 1
    root.destroy()
def close_window():
    root.destroy()
    camera.stop_preview()
    camera.close()
    quit()
def Wait():
    global state
    state +=1
    root.destroy()
def make_button(state):         
    if state == 1:
        camera_start()
        button1 = tk.Button(button_frame, text = "Expiration Date Capture", width=20, padx = 20, pady = 10, command = camera_capture,font=15)
        button1.grid(row = 0, column = 0, padx = 5, pady = 3)
    elif state == 2:
        # show image
        image1 = Image.open('/home/pi/Desktop/image_' + str(pic_number) + '.jpg')
        size= (800, 318)
        image1.thumbnail(size)        
        image = ImageTk.PhotoImage(image1)
        label = tk.Label(window_frame, image = image)
        label.image = image
        label.pack(side = "top")
        # show text
        label2 = tk.Label(button_frame, text ="Waiting...", font = 30)
        label2.grid(row =0, column = 0)
        button1 = tk.Button(button_frame, text = "Wait", width=20, padx = 20, pady = 10, command = Wait,font=15)
        button1.grid(row = 0, column = 1, padx = 5, pady = 3)
    elif state == 3:
        txt = "OCR_result"
        label2 = tk.Label(window_frame, text = txt, font = 100)
        label2.grid(row =0, column = 0, pady =150)
        button1 = tk.Button(button_frame, text = "OK", width=20, padx = 20, pady = 10, command = OCR_OK,font=15)
        button1.grid(row = 0, column = 0, padx = 5, pady = 3)
           
        button2 = tk.Button(button_frame, text = "Reject", width=20, padx = 20, pady = 10, command = OCR_reject,font=15)
        button2.grid(row = 0, column = 1, padx = 5, pady = 3)
    elif state == 4:
        camera_start()
        button1 = tk.Button(button_frame, text = "Full Photo Capture", width=20, padx = 20, pady = 10, command = camera_capture,font=15)
        button1.grid(row = 0, column = 0, padx = 5, pady = 3)
    elif state == 5:
        # show image
        image1 = Image.open('/home/pi/Desktop/image_' + str(pic_number) + '.jpg')
        size= (800, 318)
        image1.thumbnail(size)        
        image = ImageTk.PhotoImage(image1)
        label = tk.Label(window_frame, image = image)
        label.image = image
        label.pack(side = "top")
        button1 = tk.Button(button_frame, text = "Continue", width=20, padx = 20, pady = 10, command = Entire_continue,font=15)
        button1.grid(row = 0, column = 0, padx = 5, pady = 3)         
        button2 = tk.Button(button_frame, text = "Reject", width=20, padx = 20, pady = 10, command = Entire_reject,font=15)
        button2.grid(row = 0, column = 1, padx = 5, pady = 3)
        button3 = tk.Button(button_frame, text = "Finish", width=20, padx = 20, pady = 10, command = Entire_finish,font=15)
        button3.grid(row = 0, column = 2, padx = 5, pady = 3)

while(1) :
    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack(pady = 0, padx = 0)
    window_frame = tk.Frame(frame, width= 800, height=318)
    window_frame.grid(row = 0, column = 0, padx= 0, pady = 16)
    

    button_frame =tk.Frame(frame, width= 800, height=50)
    button_frame.grid(row = 1, column = 0, padx= 0, pady = 5) 
    root.geometry("800x480+0+0")
    if state == 1:
        root.title("OCR")
        make_button(state)
        # Display size = 800x480, + x + y // left up (0,0)
    elif state == 2:
        root.title("Waiting...")
        make_button(state)
    elif state == 3:
        root.title("OCR Result")
        make_button(state)
    elif state == 4:
        root.title("Entire View")
        make_button(state)
    elif state == 5:
        root.title("Entire View Result")
        make_button(state)
    root.protocol("WM_DELETE_WINDOW", close_window)
    root.mainloop()
    print(state)
    print(2)

