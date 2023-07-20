#! -usr/bin/

from PyQt5.QtWidgets import QApplication
import sys
import numpy as np
from GUI import GUI
import Config as C
import multiprocessing
from multiprocessing import shared_memory
import threading
import subprocess
import time
import serial
import struct
import datetime
import platform
import atexit

lock = multiprocessing.Lock()
shm_array = C.Shm_array
shm = multiprocessing.shared_memory.SharedMemory(create=True, size=shm_array.nbytes)
shm_array = np.ndarray(shm_array.shape, dtype=np.float16, buffer=shm.buf)

start_Record_time = time.time()

RtD = (np.pi/180)

path = 'SavedData/Record/'
filename = ''
#------------------------------------------------------

def run_python_script(script, shm):
    # Execute the script and pass the shared memory object as an argument
    shared_data = {'shared_data': shm}
    exec(open(script).read(), shared_data)

def run_cpp_program(program, shared_data):
    # Execute the program and pass the shared memory object as an argument
    subprocess.run([program, str(shared_data[0]), str(shared_data[1]), str(shared_data[2])])

def BackEnd():
    Running_Flag = True

    PrevT = time.time()

    while Running_Flag:

        CurrT = time.time()
        dt = CurrT - PrevT
        PrevT = CurrT
        if dt == 0:
            C.BackEnd_Hz = 9999.99
        else:
            C.BackEnd_Hz = round(1 / dt,2)
        # ------------------------------------------------------------ Start Controller selected
        if (C.Start) and not (C.Running):

            ControllerCode = C.Control_Mode +'.py'
            if C.Control_Mode == 'No Control Mode selected':
                C.Log.insert(0,'No Controller selected!')
            else:
                C.Log.insert(0,'Starting Controller: ' + ControllerCode)
                p1 = multiprocessing.Process(target=run_python_script, args=(ControllerCode,shm,))
                p1.start()
                C.Running = True

        if not C.Start and C.Running:
            C.Running = False
            C.Log.insert(0,'Stopping Controller')
            p1.terminate()
            C.Stepper1_Target = 0
            C.Stepper2_Target = 0
            C.Stepper3_Target = 0
            lock.acquire()
            shm_array[8] = 0
            shm_array[9] = 0
            lock.release()
        # ------------------------------------------------------------ Start Camera Code
        if (C.Camera_Start and not C.Camera_Runnig):
            C.Log.insert(0,'Starting Camera Code')
            p2 = multiprocessing.Process(target=run_python_script, args=("CameraCode.py", shm,))
            p2.start()
            C.Camera_Runnig = True

        if C.Camera_Runnig and C.cam_x == 1 and C.cam_y == 9 and C.cam_x_vel == 9 and C.cam_y_vel == 9:
            #C.Camera_Runnig = False
            C.Log.insert(0,'No connection to camera')
            lock.acquire()
            shm_array[4] = 0
            shm_array[5] = 0
            shm_array[6] = 0
            shm_array[7] = 0
            lock.release()

        if not C.Camera_Start and C.Camera_Runnig:
            C.Log.insert(0,'Stopping Camera Code')
            p2.terminate()
            C.Camera_Runnig = False

            lock.acquire()
            shm_array[4] = 0
            shm_array[5] = 0
            shm_array[6] = 0
            shm_array[7] = 0
            lock.release()
        # ------------------------------------------------------------ Stop Multithreading code at exit
        if C.exit_flag:
            try:
                Running_Flag = False
                p1.terminate()
            except:
                pass
            try:
                p2.terminate()
            except:
                pass
        # ------------------------------------------------------------ Start Data recording
        if C.Record_Data or C.Record_Data_Running:
            if C.Record_Data and not C.Record_Data_Running:

                now = datetime.datetime.now()
                start_Record_time = time.time()
                timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

                filename = f"{path}Recorded Data for {C.Control_Mode} at {timestamp}.txt"
                #filename = f"{path}Recorded Data for sine delay at {timestamp}.txt"
                with open(filename, "a") as file:
                    file.write(C.Data_Names + '\n')
                    #file.write(C.Hz_Names + '\n')
                    #file.write(C.Sine_Name + '\n')

                C.Record_Data_Running = True
            if C.Record_Data_Running:
                with open(filename, "a") as file:
                    PrintTime =  time.time() - start_Record_time
                    data = f'{C.Target_Pos_x} {C.Target_Pos_y} {C.cam_x} {C.cam_y} {C.cam_x_vel} {C.cam_y_vel}\
 {round(C.U_rad_x/RtD,3)} {round(C.U_rad_y/RtD,3)} {C.U_x_v_fb} {C.U_y_v_fb} {PrintTime}'
                    #data = f'{C.BackEnd_Hz} {C.SharedMem_Hz} {C.UartCom_Hz} {C.Cam_Hz} {C.Controller_Hz}'
                    #data = f'{C.sine} {C.sine_controller} {C.Stepper1_Feedback} {C.Stepper2_Feedback}\
# {C.Stepper3_Feedback} {C.SharedMem_Hz} {C.Controller_Hz} {PrintTime}'
                    file.write(data +'\n')
                    if not C.Record_Data and C.Record_Data_Running:
                        file.close()
                        C.Record_Data_Running = False

        if C.Start_Serial_Com and not C.Serial_Com_Running:
            C.Serial_Com_Running = True

            Serial_Com = threading.Thread(target=USBArduinocom)
            Serial_Com.start()

        if not C.Start_Serial_Com:
            C.Serial_Com_Running = False

        time.sleep(0.01)



sine_controller = 0
def GUISharedMemHandler():
    Last_Target_x = 0
    Last_Target_y = 0
    PrevT = time.time()
    while not C.exit_flag:
        CurrT = time.time()
        dt = CurrT - PrevT
        PrevT = CurrT
        if dt == 0:
            C.SharedMem_Hz = 9999.99
        else:
            C.SharedMem_Hz = round(1 / dt,2)
        #C.sine = 45*np.sin(5*time.time())
        #-------------------------------------------------- shm handler
        lock.acquire()
        shm_array[0] = C.Target_Pos_x
        shm_array[1] = C.Target_Pos_y
        shm_array[2] = C.Target_Vel_x
        shm_array[3] = C.Target_Vel_y
        #shm_array[2] = C.sine
        #C.sine_controller = shm_array[3]

        C.cam_x = shm_array[4]
        C.cam_y = shm_array[5]
        C.cam_x_vel = shm_array[6]
        C.cam_y_vel = shm_array[7]

        C.U_rad_x = shm_array[8]
        C.U_rad_y = shm_array[9]

        shm_array[10] = C.PID_P_x
        shm_array[11] = C.PID_D_x
        shm_array[12] = C.PID_I_x

        shm_array[13] = C.SS_k1_x
        shm_array[14] = C.SS_k2_x

        shm_array[15] = C.MPC_Q_xp
        shm_array[16] = C.MPC_Q_xv
        shm_array[17] = C.MPC_R_Vin
        if C.Start:
            C.Controller_Hz = shm_array[18]
        else:
            C.Controller_Hz = 0
        shm_array[19] = C.MPC_SnapShot

        shm_array[20] = C.No_Ball
        shm_array[21] = C.Camera_show_Frame
        shm_array[22] = C.Camera_show_Mask
        shm_array[23] = C.Camera_Pause
        if C.Camera_Runnig:
            C.Cam_Hz = shm_array[24]
        else:
            C.Cam_Hz = 0
        lock.release()

        #----------------------------------------------------------

        # l = 426.5mm - 123.12, 213,25, (sq(3)*l)/6, l/2
        # l2 = 346.41mm, 99.99, 173.205

        if C.Running:
            #
            t1 = 100*np.sin(C.U_rad_y)*np.cos(C.U_rad_x)
            t2 = 173.2*np.sin(C.U_rad_x)

            z1 = -t1 - t2
            z2 = -t1 + t2
            z3 =  t1

            z1 = LimitAngle(z1)
            z2 = LimitAngle(z2)
            z3 = LimitAngle(z3)

            C.Stepper1_Target = np.arcsin(z3/75)/RtD
            C.Stepper2_Target = np.arcsin(z2/75)/RtD
            C.Stepper3_Target = np.arcsin(z1/75)/RtD

        sin_y_cos_x = (75 * np.sin(C.Stepper1_Feedback * RtD)) / 100
        sin_x = ((75 * np.sin(C.Stepper2_Feedback * RtD)) + 100 * sin_y_cos_x) / 173.2
        C.U_x_v_fb = round(np.arcsin(sin_x) / RtD, 2)

        c = sin_y_cos_x/np.cos(np.arcsin(sin_x))
        if c > 1:
            c = 1
        elif c < -1:
            c = -1
        C.U_y_v_fb = round((np.arcsin(c))/RtD, 2)
        time.sleep(0.005)




def LimitAngle(Value):
    # 62', +50
    if Value > 70:
        Value = 70
    elif Value < -60:
        Value = -60
    return Value



def USBArduinocom():

    PrevT = time.time()
    if platform.system() == 'Windows':
        Com = 'COM3'
    else:
        Com = '/dev/ttyS3'
    try:
        Arduino = serial.Serial(Com, 115200, timeout=1)
    except:
        C.Log.insert(0,'Failed Connection to Arduino')
        return
        pass

    while not C.exit_flag and C.Serial_Com_Running:

        CurrT = time.time()
        dt = CurrT - PrevT
        PrevT = CurrT
        if dt == 0:
            C.UartCom_Hz = 9999.99
        else:
            C.UartCom_Hz = 1 / dt
        # print(dt)


        if C.Paus_New_Arduino_Values:
            data = struct.pack('ffff', 0.0, 0.0, 0.0, float(C.Calibrate_Arduino))
        else:
            data = struct.pack('ffff', C.Stepper1_Target, C.Stepper2_Target, C.Stepper3_Target, float(C.Calibrate_Arduino))
            #data = struct.pack('ffff', C.sine_controller, C.sine_controller, C.sine_controller, float(C.Calibrate_Arduino))

        Arduino.write(data)
        response = Arduino.readline().decode().split()
        try:
            C.Stepper1_Feedback = float(response[0])
            C.Stepper2_Feedback = float(response[1])
            C.Stepper3_Feedback = float(response[2])
        except:
            pass
    C.UartCom_Hz = 0

# ----------------------------- shm clear
def cleanup_shm():
    shm.close()
    shm.unlink()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = GUI()

    ShareMemoryThread = threading.Thread(target=GUISharedMemHandler)
    ShareMemoryThread.start()

    BackendThread = threading.Thread(target=BackEnd)
    BackendThread.start()

    a.showFullScreen()
    #a.show()
    atexit.register(cleanup_shm)

    sys.exit(app.exec_())



