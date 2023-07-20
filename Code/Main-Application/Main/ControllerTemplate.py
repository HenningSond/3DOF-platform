import Config
import time
from multiprocessing import shared_memory
import numpy as np
import multiprocessing

PrevT = time.time()

U_x = 0
U_y = 0

Run = True
lock = multiprocessing.Lock()
shm = shared_memory.SharedMemory(name=shared_data.name)
shm_array = np.ndarray(Config.Shm_array.shape, dtype=np.float16, buffer=shm.buf)

while Run:
    #--------------------------------------------------- HZ
    CurrT = time.time()
    dt = CurrT - PrevT
    PrevT = CurrT
    if dt == 0:
        HZ = 9999.99
    else:
        HZ = 1 / dt
    # print(HZ)
    #----------------------------------------------

    lock.acquire()
    Target_x_p = shm_array[0]
    Target_y_p = shm_array[1]
    shm_array[2] = round(U_x, 4)
    shm_array[3] = round(U_y, 4)
    print(shm_array)
    lock.release()


