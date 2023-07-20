import numpy as np

Control_Mode = 'No controllmode selected'
Input_Mode    = ''

Shm_array = np.zeros(25, dtype=np.float16)

exit_flag = False

Log = []
Log_Rev = []
Start = False
Running = False

Record_Data = False
Record_Data_Running = False
Data_Names = 'TX TY FBX FBY FBVX FBVY TUX TUY FBUX FBUY Time'
Hz_Names = 'BackEnd_Hz SharedMem_Hz UartCom_Hz Cam_Hz Controller_Hz'
Sine_Name = 'sine sine_controller fb1 fb2 fb3 BackEnd_Hz Controller_Hz Time'

Camera_Start = False
Camera_Runnig = False
Camera_show_Frame = 0
Camera_show_Mask = 0
Camera_Pause = -5.67

Target_Pos_x   = 0
Target_Pos_y   = 0
Target_Vel_x = 0
Target_Vel_y = 0
Feedback_pos = 0

Start_Serial_Com = False
Serial_Com_Running = False

Start_I2C_Com = False
I2C_Com_Running = False

Paus_New_Arduino_Values = False
Calibrate_Arduino = -5.65

cam_x = 0.0
cam_x_vel = 0.0
cam_y = 0.0
cam_y_vel = 0.0
No_Ball = 0.0

Stepper1_Target = 0
Stepper1_Feedback = 0
Stepper2_Target = 0
Stepper2_Feedback = 0
Stepper3_Target = 0
Stepper3_Feedback = 0

U_rad_x = 0
U_rad_y = 0

U_x_v_fb = 0.0
U_y_v_fb = 0.0

#--------------------- PID parameter

PID_P_x = 0.0015
PID_D_x = 0.0000
PID_I_x = 0

PID_P_y = 0.0015
PID_D_y = 0.0000
PID_I_y = 0

Pid_delay_time = 0.01

#---------------------------- State Space

SS_k1_x = 0.0012
SS_k2_x = 0.0006

SS_k1_y = 0.0012
SS_k2_y = 0.0006

SS_delay_time = 0.01

#-------------------------------- MPC

MPC_SnapShot = -5.67

MPC_Q_xp = 1.73
MPC_Q_xv = 0.55
MPC_R_Vin = 310

#MPC_q = np.diag([MPC_Q_xp, MPC_Q_xv, MPC_Q_xp, MPC_Q_xv])
#MPC_r = np.diag([MPC_R_Vin, MPC_R_Vin])

#---------------------------------------------------------------- Hz

BackEnd_Hz    = 0.0
SharedMem_Hz  = 0.0
UartCom_Hz    = 0.0

Cam_Hz        = 0.0
Controller_Hz = 0.0

sine = 0.0
sine_controller = 0.0
sine_fb = 0.0
