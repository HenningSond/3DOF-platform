import cv2
import numpy as np
import time
from multiprocessing import shared_memory
import multiprocessing
import Config as C
import platform

PrevT = time.time()

lock = multiprocessing.Lock()

shm = shared_memory.SharedMemory(name=shared_data.name)
shm_array = np.ndarray(C.Shm_array.shape, dtype=np.float16, buffer=shm.buf)
#shm_array = C.Shm_array
#shm_array = np.zeros(20)

last_values_x = []
last_values_y = []
last_values_v_x = []
last_values_v_y = []



Camera_Pause = -5.67

ang_x = 0
ang_y = 0

# Define the lower and upper bounds of the orange color in HSV format
orange_lower = np.array([0, 88, 85])
orange_upper = np.array([13, 255, 201])
Show_Frame = 0
Show_Mask = 0

Frame = False
Mask = False
gx = 0
gy = 0
gx_vel = 0
gy_vel = 0


gx_prev = 0
gy_prev = 0




gx_vel_prev = 0.0
gy_vel_prev = 0.0

# Initialize the video stream
if platform.system() == 'Linux':
    cap = cv2.VideoCapture(0)
elif platform.system() == 'Windows':
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

#cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
#cap = cv2.VideoCapture(0)


# Set the video resolution to be square, centered on (0,0)
width = 640
height = 480

cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

def average_filter_x(value):
    last_values_x.append(value)
    if len(last_values_x) > 3:
        last_values_x.pop(0)
    return np.average(last_values_x)

def average_filter_y(value):
    last_values_y.append(value)
    if len(last_values_y) > 3:
        last_values_y.pop(0)
    return np.average(last_values_y)




while True:
    # Read a frame from the video stream
    ret, frame1 = cap.read()

    if ret == False:
        lock.acquire()
        shm_array[4] = round(1, 0)
        shm_array[5] = round(9, 0)
        shm_array[6] = round(9, 0)
        shm_array[7] = round(9, 0)
        lock.release()
        break
    # Crop frame to only include platform
    frame2 = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.circle(frame2, (320, 240), 205, (255, 255, 255), -1)
    frame = cv2.bitwise_and(frame2, frame1)

    CurrT = time.time()
    dt = CurrT - PrevT
    PrevT = CurrT
    if dt == 0:
        Hz = 9999.99
    else:
        Hz = 1 / dt

    # Convert the frame from BGR color space to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the image to isolate the orange color
    mask = cv2.inRange(hsv, orange_lower, orange_upper)

    # Find the contours in the mask
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If a contour is found, get its center and draw a circle around it
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, (int(x), int(y)), 2, (0, 255, 255), -1)
            # Scale the coordinate system in terms of the fisheye lens
            lock.acquire()
            ang_x = shm_array[8]
            ang_y = shm_array[9]
            lock.release()

            gx = -(x - width / 2)
            gy = -(y - (height+16) / 2)

            #gx = -(x - width / 2) / np.cos(ang_x * 2)
            #gy = -(y - (height + 16) / 2) / np.cos(ang_y * 2)

            if -1 < (gx - gx_prev) < 1:
                gx = gx_prev

            if -1 < (gy - gy_prev) < 1:
                gy = gy_prev


            #gx = average_filter_x(gx)
            #gy = average_filter_y(gy)

            if gx_prev == gx:
                gx_vel = 0
            else:
                gx_vel = (gx - gx_prev) / dt
            if gy_prev == gy:
                gy_vel = 0
            else:
                gy_vel = (gy - gy_prev) / dt

            gx_prev = gx
            gy_prev = gy
    else:
        gx = 0
        gy = 0
        gx_vel = 0
        gy_vel = 0

    if Camera_Pause > 0.0:
        gx = 0
        gy = 0
        gx_vel = 0
        gy_vel = 0

    lock.acquire()
    shm_array[4] = round(gx, 0)
    shm_array[5] = round(gy, 0)
    shm_array[6] = round(gx_vel, 0)
    shm_array[7] = round(gy_vel, 0)
    Show_Frame   = int(shm_array[21])
    Show_Mask    = int(shm_array[22])
    Camera_Pause =shm_array[23]
    shm_array[24] = Hz
    lock.release()


    if Show_Frame:
        cv2.imshow("frame", frame)
        Frame = True
    elif (not Show_Frame and Frame):
        cv2.destroyWindow("frame")
        Frame = False

    if Show_Mask:
        cv2.imshow("mask", mask)
        Mask = True
    elif (not Show_Mask and Mask):
        cv2.destroyWindow("mask")
        Mask = False

    # Wait for a key press and exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video stream and close all windows
cap.release()
cv2.destroyAllWindows()

