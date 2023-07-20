import Config
import time
from multiprocessing import shared_memory
import numpy as np
import multiprocessing

global shm
global shm_array

PrevT = time.time()

U_x = 0
U_y = 0

SS_k1_x = Config.SS_k1_x
SS_k2_x = Config.SS_k2_x

SS_k1_y = Config.SS_k1_y
SS_k2_y = Config.SS_k2_y

Feedback_x_p = 0
Feedback_y_p = 0
PrevFeedback_x_p = 0
PrevFeedback_y_p = 0

x_v_Error = 0
y_v_Error = 0
Run = True

lock = multiprocessing.Lock()
shm = shared_memory.SharedMemory(name=shared_data.name)
shm_array = np.ndarray(Config.Shm_array.shape, dtype=np.float16, buffer=shm.buf)

lock.acquire()
SS_k1_x = shm_array[13]
SS_k2_x = shm_array[14]

SS_k1_y = shm_array[13]
SS_k2_y = shm_array[14]

lock.release()

while Run:
    CurrT = time.time()
    dt = CurrT - PrevT
    PrevT = CurrT
    if dt == 0:
        Hz = 9999.99
    else:
        Hz = round(1 / dt, 2)
    lock.acquire()
    Target_x_p      = shm_array[0]
    Target_y_p      = shm_array[1]
    Target_x_v      = shm_array[2]
    Target_y_v      = shm_array[3]
    Feedback_x_p    = shm_array[4]
    Feedback_y_p    = shm_array [5]
    x_v_Error       = shm_array[6]
    y_v_Error       = shm_array[7]
    shm_array[8]    = round(U_x, 4)
    shm_array[9]    = round(U_y, 4)
    shm_array[18] = Hz

    lock.release()

    x_p_Error =  Feedback_x_p - Target_x_p
    U_x = (x_p_Error * SS_k1_x + (x_v_Error - Target_x_v )* SS_k2_x)

    y_p_Error =  Feedback_y_p - Target_y_p
    U_y = (y_p_Error * SS_k1_y + (y_v_Error - Target_y_v) * SS_k2_y)

    PrevFeedback_x_p = Feedback_x_p
    PrevFeedback_y_p = Feedback_y_p

    time.sleep(0.001)
    #print(shm_array, U_x)

