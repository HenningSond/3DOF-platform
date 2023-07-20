import time
import pickle
import platform

if platform.system() == 'Linux':
    print('import Mpc_Linux')
    from MPC_code_Linux_05.cpg_solver import cpg_solve
elif platform.system() == 'Windows':
    from MPC_code.cpg_solver import cpg_solve

from multiprocessing import shared_memory
import numpy as np
import multiprocessing
import Config
import datetime

u_traj = np.array([0, 0])

if platform.system() == 'Linux':
    print('open Mpc_Linux')
    with open('MPC_code_Linux_05/problem.pickle', 'rb') as f:
        problem = pickle.load(f)
elif platform.system() == 'Windows':
    with open('MPC_code/problem.pickle', 'rb') as f:
        problem = pickle.load(f)

lock = multiprocessing.Lock()
shm = shared_memory.SharedMemory(name=shared_data.name)
shm_array = np.ndarray(Config.Shm_array.shape, dtype=np.float16, buffer=shm.buf)


# Assign Parameters for MPC
Apar = np.array([[0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 1.0], [0.0, 0.0, 0.0, 0.0]])
Bpar = np.array([[0.0, 0.0], [7000.0, 0.0], [0.0, 0.0], [0.0, 7000.0]])

problem.param_dict['A'].value = Apar
problem.param_dict['B'].value = Bpar


x_pos_prev = 0
y_pos_prev = 0
x_vel = 0
y_vel = 0
t3 = 0


PrevT = -0.001

lock.acquire()
MPC_Q_xp = shm_array[15]
MPC_Q_xv = shm_array[16]
MPC_R_Vin = shm_array[17]
lock.release()

MPC_q = np.diag([MPC_Q_xp, MPC_Q_xv, MPC_Q_xp, MPC_Q_xv])
MPC_r = np.diag([MPC_R_Vin, MPC_R_Vin])

problem.param_dict['Qsqrt'].value = MPC_q
problem.param_dict['Rsqrt'].value = MPC_r
SnapShotRunnig = False
SnapTaken = False
WriteSnap = False
TimeAdded = False
path = 'SavedData/Snap/'
sine_out = 0
while True:

    CurrT = time.time()
    dt = CurrT - PrevT
    PrevT = CurrT
    if dt == 0:
        Hz = 9999.99
    else:
        Hz = round(1/dt, 2)
    #print(dt)

    lock.acquire()
    #sine = shm_array[2]
    #shm_array[3] = sine_out
    x_pos           = shm_array[4]
    y_pos           = shm_array[5]
    x_vel           = shm_array[6]
    y_vel           = shm_array[7]
    s_r             = np.array([[shm_array[0]], [0], [shm_array[1]], [0]])
    shm_array[8]    = round(u_traj[0], 4)
    shm_array[9]    = round(u_traj[1], 4)
    shm_array[18]   = Hz
    MPC_SnapShot    = shm_array[19]

    lock.release()

    s_states = np.array([[x_pos], [x_vel], [y_pos], [y_vel]])

    s_error = (s_r - s_states)# Initial state

    problem.param_dict['s_error'].value = s_error
    problem.register_solve('CPG', cpg_solve)
    problem.solve(method='CPG')
    angle_list = problem.var_dict['U'].value
    state_list = problem.var_dict['S'].value
    u_traj = angle_list[:, 1]
    #sine_out = sine
    # ----------------------------------------------------- Take a snapshot of the predict
    if MPC_SnapShot > 0.0 and not SnapShotRunnig:
        StartTime = time.time()
        FB_U_x = []
        FB_P_x = []
        FB_V_x = []
        FB_U_y = []
        FB_P_y = []
        FB_V_y = []
        TimeList = []
        SnapShotRunnig = True

    if SnapShotRunnig:
        RunTime = time.time() - StartTime
        if RunTime > 1:
            if not SnapTaken:
                Predicted_U_x = angle_list[0, :]
                Predicted_S_P_x = state_list[0, :]
                Predicted_S_V_x = state_list[1, :]
                Predicted_U_y = angle_list[1, :]
                Predicted_S_P_y = state_list[2, :]
                Predicted_S_V_y = state_list[3, :]
                SnapTaken = True
            FB_U_x.append(u_traj[0])
            FB_P_x.append(s_error[0])
            FB_V_x.append(s_error[1])

            FB_U_y.append(u_traj[1])
            FB_P_y.append(s_error[2])
            FB_V_y.append(s_error[3])
            TimeList.append(RunTime-1)

        if RunTime > 2:
            SnapShotRunnig = False
            WriteSnap = True
            FileCreated = False
            n_predict = 0
            n_feedback = 0

    if WriteSnap:
        if not FileCreated:
            now = datetime.datetime.now()
            start_Record_time = time.time()
            timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
            filename_Predicted_x = f"{path} MPC SnapShot Predicted x {timestamp}.txt"
            filename_Predicted_y = f"{path} MPC SnapShot Predicted y {timestamp}.txt"
            filename_FB_x = f"{path} MPC SnapShot True x {timestamp}.txt"
            filename_FB_y = f"{path} MPC SnapShot True y {timestamp}.txt"
            FileCreated = True

        if (len(Predicted_U_x) > n_predict):
            with open(filename_Predicted_x, "a") as file_1:
                data1 = f'{Predicted_U_x[n_predict]} {Predicted_S_P_x[n_predict]} {Predicted_S_V_x[n_predict]}'
                file_1.write(data1 + '\n')

            with open(filename_Predicted_y, "a") as file_2:
                data2 = f'{Predicted_U_y[n_predict]} {Predicted_S_P_y[n_predict]} {Predicted_S_V_y[n_predict]}'
                file_2.write(data2 + '\n')

            n_predict += 1


        if (len(FB_U_x) > n_feedback):
            with open(filename_FB_x, "a") as file_3:
                data3 = f'{FB_U_x[n_feedback]} {FB_P_x[n_feedback]} {FB_V_x[n_feedback]} {TimeList[n_feedback]}'
                file_3.write(data3 + '\n')

            with open(filename_FB_y, "a") as file_4:
                data4 = f'{FB_U_y[n_feedback]} {FB_P_y[n_feedback]} {FB_V_y[n_feedback]} {TimeList[n_feedback]}'
                file_4.write(data4 + '\n')
            n_feedback += 1

        else:
            file_1.close()
            file_2.close()
            file_3.close()
            file_4.close()
            WriteSnap = False













