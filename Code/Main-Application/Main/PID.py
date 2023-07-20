from multiprocessing import shared_memory
import numpy as np
import multiprocessing
import Config
import time

PrevT = time.time()

U_x = 0
U_y = 0

integral_x = 0
integral_y = 0

Feedback_x = 0
Feedback_y = 0

PrevError_x = 0
PrevError_y = 0
RtD = (3.14/180)
Run = True

lock = multiprocessing.Lock()
shm = shared_memory.SharedMemory(name=shared_data.name)
shm_array = np.ndarray(Config.Shm_array.shape, dtype=np.float16, buffer=shm.buf)

lock.acquire()
Pid_p_x = shm_array[10]
Pid_d_x = shm_array[11]
Pid_i_x = shm_array[12]

Pid_p_y = shm_array[10]
Pid_d_y = shm_array[11]
Pid_i_y = shm_array[12]
lock.release()

while Run:

    CurrT = time.time()
    dt = CurrT - PrevT
    PrevT = CurrT
    if dt == 0:
        HZ = 9999.99
    else:
        HZ = round(1 / dt, 2)

    lock.acquire()
    Target_x_p = shm_array[0]
    Target_y_p = shm_array[1]
    Feedback_x_p = shm_array[4]
    Feedback_y_p = shm_array[5]
    shm_array[8] = round(U_x, 4)
    shm_array[9] = round(U_y, 4)
    shm_array[18] = HZ
    # print(shm_array[4])
    lock.release()



    #--------------------------------------------------------------- Pid x
    Error_x = Feedback_x_p - Target_x_p

    DeDt_x = (Error_x-PrevError_x)/dt
    integral_x = integral_x + Error_x*dt

    PrevError_x = Error_x

    U_x = Pid_p_x*Error_x + Pid_d_x*DeDt_x + Pid_i_x*integral_x
    #--------------------------------------------------------------- Pid y
    Error_y = Feedback_y_p - Target_y_p

    DeDt_y = (Error_y - PrevError_y) / dt
    integral_y = integral_y + Error_y * dt
    PrevError_y = Error_y

    U_y = Pid_p_y * Error_y + Pid_d_x * DeDt_y + Pid_i_y*integral_y

    print(Pid_p_x*Error_x, Pid_d_x*DeDt_x)

    time.sleep(0.01)
