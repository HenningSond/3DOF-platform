
# 07.05.2023 3 DOF gui code
# Verson 1.2
#

import subprocess

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton, QFrame, QDoubleSpinBox, \
    QSpinBox, QTextEdit, QMainWindow, QMessageBox
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QIcon
from PyQt5.QtCore import Qt, QPoint, QRect, QTimer
import Config

import platform
RtD = (3.14/180)

class PID_Config(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(700,350,570,440)
        self.setWindowTitle('PID Config')
        # ----------------------------------------------------------------
        self.font1 = QFont()
        self.font1.setPointSize(16)

        self.font2 = QFont()
        self.font2.setPointSize(12)
        # --------------------------------------------------------- info
        self.Info = QLabel(self)
        self.Info.move(10,5)
        self.Info.setText('Change P, D and I Gains. Save and rerun the PID')
        self.Info.setFont(self.font1)

        self.info2  = QLabel(self)
        self.info2.move(10,335)
        self.info2.setText('NB! all values are multiplied by 10')
        self.info2.setFont(self.font2)
        # --------------------------------------------------------- Set P gain
        self.LableP = QLabel(self)
        self.LableP.move(65,45)
        self.LableP.setText('P Gain')
        self.LableP.setFont(self.font1)

        self.PGain = QDoubleSpinBox(self)
        self.PGain.setObjectName(u"doubleSpinBox")
        self.PGain.setGeometry(QRect(5, 80, 220, 100))
        self.PGain.setStyleSheet("QAbstractSpinBox::up-button { width: 100px; height: 50px; }"
                      "QAbstractSpinBox::down-button { width: 100px; height: 50px; }")
        self.PGain.setDecimals(5)
        self.PGain.setMinimum(0.00000)
        self.PGain.setSingleStep(0.01000)
        # --------------------------------------------------------- Set D gain
        self.LableD = QLabel(self)
        self.LableD.move(360,45)
        self.LableD.setText('D Gain')
        self.LableD.setFont(self.font1)

        self.DGain = QDoubleSpinBox(self)
        self.DGain.setObjectName(u"doubleSpinBox")
        self.DGain.setGeometry(QRect(300, 80, 220, 100))
        self.DGain.setStyleSheet("QAbstractSpinBox::up-button { width: 100px; height: 50px; }"
                      "QAbstractSpinBox::down-button { width: 100px; height: 50px; }")
        self.DGain.setDecimals(5)
        self.DGain.setMinimum(0.00000)
        self.DGain.setSingleStep(0.01000)
        # --------------------------------------------------------- Set I gain
        self.LableI = QLabel(self)
        self.LableI.move(75, 190)
        self.LableI.setText('I Gain')
        self.LableI.setFont(self.font1)

        self.IGain = QDoubleSpinBox(self)
        self.IGain.setObjectName(u"doubleSpinBox")
        self.IGain.setGeometry(QRect(5, 220, 220, 100))
        self.IGain.setStyleSheet("QAbstractSpinBox::up-button { width: 100px; height: 50px; }"
                      "QAbstractSpinBox::down-button { width: 100px; height: 50px; }")
        self.IGain.setDecimals(5)
        self.IGain.setMinimum(0.00000)
        self.IGain.setSingleStep(0.01000)

        #-------------------------------------------------------- Set decimal
        self.LableDe = QLabel(self)
        self.LableDe.move(300, 190)
        self.LableDe.setText('Number of decimals')
        self.LableDe.setFont(self.font1)

        self.Decimal = QSpinBox(self)
        self.Decimal.setObjectName(u"Decimal")
        self.Decimal.setGeometry(QRect(300, 220, 220, 100))
        self.Decimal.setStyleSheet("QAbstractSpinBox::up-button { width: 100px; height: 50px; }"
                      "QAbstractSpinBox::down-button { width: 100px; height: 50px; }")
        self.Decimal.setMinimum(-5)
        self.Decimal.setMaximum(0)
        self.Decimal.setSingleStep(1)
        self.Decimal.setValue(-2)
        self.Decimal.valueChanged.connect(self.updateDecimal)
        #---------------------------------------------------- Save and close
        self.CancelButton = QPushButton('Cancel', self)
        self.CancelButton.setGeometry(2, 355, 275, 80)
        self.CancelButton.clicked.connect(self.Cancel)

        self.SaveButton = QPushButton("Save", self)
        self.SaveButton.setGeometry(287, 355, 283, 80)
        self.SaveButton.clicked.connect(self.Save)



    def Save(self):

        Config.PID_P_x = self.PGain.value()
        Config.PID_D_x = self.DGain.value()
        Config.PID_I_x = self.IGain.value()
        Config.PID_P_y = self.PGain.value()
        Config.PID_D_y = self.DGain.value()
        Config.PID_I_y = self.IGain.value()
        self.hide()

    def Cancel(self):
        self.hide()

    def updateDecimal(self):
        self.PGain.setSingleStep(10 ** (self.Decimal.value()))
        self.DGain.setSingleStep(10 ** (self.Decimal.value()))
        self.IGain.setSingleStep(10 ** (self.Decimal.value()))

#-------------------------------------------------------------------- State space config window
class SS_Config(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(700,350,570,440)
        self.setWindowTitle('State Space Config')
        #----------------------------------------------------------------
        self.font = QFont()
        self.font.setPointSize(16)

        self.font2 = QFont()
        self.font2.setPointSize(12)
        # --------------------------------------------------------- info
        self.Info = QLabel(self)
        self.Info.move(10,5)
        self.Info.setText('Change K1 and K2 Gains. Save and rerun the StateSpace')
        self.Info.setFont(self.font)

        self.info2 = QLabel(self)
        self.info2.move(10, 335)
        self.info2.setText('NB! all values are multiplied by 10')
        self.info2.setFont(self.font2)
        #--------------------------------------------------------- Set K1 value
        self.LableK1 = QLabel(self)
        self.LableK1.move(65,45)
        self.LableK1.setText('K1 Gain')
        self.LableK1.setFont(self.font)

        self.k1Gain = QDoubleSpinBox(self)
        self.k1Gain.setObjectName(u"doubleSpinBox")
        self.k1Gain.setGeometry(QRect(5, 80, 220, 100))
        self.k1Gain.setStyleSheet("QAbstractSpinBox::up-button { width: 100px; height: 50px; }"
                      "QAbstractSpinBox::down-button { width: 100px; height: 50px; }")
        self.k1Gain.setDecimals(5)
        self.k1Gain.setMinimum(0.00000)
        self.k1Gain.setSingleStep(0.01000)
        # --------------------------------------------------------- Set K2 value
        self.LableK1 = QLabel(self)
        self.LableK1.move(360,45)
        self.LableK1.setText('K2 Gain')
        self.LableK1.setFont(self.font)

        self.k2Gain = QDoubleSpinBox(self)
        self.k2Gain.setObjectName(u"doubleSpinBox")
        self.k2Gain.setGeometry(QRect(300, 80, 220, 100))
        self.k2Gain.setStyleSheet("QAbstractSpinBox::up-button { width: 100px; height: 50px; }"
                      "QAbstractSpinBox::down-button { width: 100px; height: 50px; }")
        self.k2Gain.setDecimals(5)
        self.k2Gain.setMinimum(0.00000)
        self.k2Gain.setSingleStep(0.01000)
        #-------------------------------------------------------- Set Decimal
        self.LableK1 = QLabel(self)
        self.LableK1.move(5, 190)
        self.LableK1.setText('Number of decimals')
        self.LableK1.setFont(self.font)

        self.Decimal = QSpinBox(self)
        self.Decimal.setObjectName(u"Decimal")
        self.Decimal.setGeometry(QRect(5, 220, 220, 100))
        self.Decimal.setStyleSheet("QAbstractSpinBox::up-button { width: 100px; height: 50px; }"
                      "QAbstractSpinBox::down-button { width: 100px; height: 50px; }")
        self.Decimal.setMinimum(-5)
        self.Decimal.setMaximum(0)
        self.Decimal.setSingleStep(1)
        self.Decimal.setValue(-2)
        self.Decimal.valueChanged.connect(self.updateDecimal)
        #---------------------------------------------------- Save and close
        self.SaveButton = QPushButton("Save", self)
        self.SaveButton.setGeometry(287,355,283,80)
        self.SaveButton.clicked.connect(self.Save)
        #----------------------------------------------------Cancel
        self.CancelButton = QPushButton("Cancel",self)
        self.CancelButton.setGeometry(2, 355, 275, 80)
        self.CancelButton.clicked.connect(self.Cancel)

    def Save(self):
        Config.SS_k1_x = self.k1Gain.value()*10
        Config.SS_k2_x = self.k2Gain.value()*10
        Config.SS_k1_y = self.k1Gain.value()*10
        Config.SS_k2_y = self.k2Gain.value()*10
        self.hide()

    def Cancel(self):
        self.hide()

    def updateDecimal(self):
        self.k1Gain.setSingleStep(10**(self.Decimal.value()))
        self.k2Gain.setSingleStep(10**(self.Decimal.value()))
#-------------------------------------------------------------------- MPC config window

class MPC_Config(QWidget):
    def __init__(self):
        super().__init__()
        self.Decimal = None
        self.setGeometry(700,350,570,440)
        self.setWindowTitle('MPC Config')

        self.font = QFont()
        self.font.setPointSize(16)

        self.font2 = QFont()
        self.font2.setPointSize(12)
        #--------------------------------------------------------- info
        self.Info = QLabel(self)
        self.Info.move(10,5)
        self.Info.setText('Change the Q and R matrix. Save and rerun the MPC')
        self.Info.setFont(self.font)

        self.Info2 = QLabel(self)
        self.Info2.move(10, 335)
        self.Info2.setText('NB! all values are multiplied by 10')
        self.Info2.setFont(self.font2)

        #--------------------------------------------------------- Set K1 value
        self.LableK1 = QLabel(self)
        self.LableK1.move(65, 45)
        self.LableK1.setText('Q Position')
        self.LableK1.setFont(self.font)

        self.k1Gain = QDoubleSpinBox(self)
        self.k1Gain.setObjectName(u"doubleSpinBox")
        self.k1Gain.setGeometry(QRect(5, 80, 220, 100))
        self.k1Gain.setStyleSheet("QAbstractSpinBox::up-button { width: 100px; height: 50px; }"
                                  "QAbstractSpinBox::down-button { width: 100px; height: 50px; }")
        self.k1Gain.setDecimals(4)
        self.k1Gain.setMinimum(0.00000)
        self.k1Gain.setSingleStep(0.01000)
        # --------------------------------------------------------- Set K2 value
        self.LableK2 = QLabel(self)
        self.LableK2.move(360, 45)
        self.LableK2.setText('Q Velocity')
        self.LableK2.setFont(self.font)

        self.k2Gain = QDoubleSpinBox(self)
        self.k2Gain.setObjectName(u"doubleSpinBox")
        self.k2Gain.setGeometry(QRect(300, 80, 220, 100))
        self.k2Gain.setStyleSheet("QAbstractSpinBox::up-button { width: 100px; height: 50px; }"
                                "QAbstractSpinBox::down-button { width: 100px; height: 50px; }")
        self.k2Gain.setDecimals(4)
        self.k2Gain.setMinimum(0.00000)
        self.k2Gain.setSingleStep(0.01000)
        # --------------------------------------------------------- Set K3 value
        self.LableK3 = QLabel(self)
        self.LableK3.move(75, 190)
        self.LableK3.setText('R Angle')
        self.LableK3.setFont(self.font)

        self.k3Gain = QDoubleSpinBox(self)
        self.k3Gain.setObjectName(u"doubleSpinBox")
        self.k3Gain.setGeometry(QRect(5, 220, 220, 100))
        self.k3Gain.setStyleSheet("QAbstractSpinBox::up-button { width: 100px; height: 50px; }"
                                  "QAbstractSpinBox::down-button { width: 100px; height: 50px; }")
        self.k3Gain.setDecimals(4)
        self.k3Gain.setMinimum(0.00000)
        self.k3Gain.setSingleStep(0.01000)
        #-------------------------------------------------------- Set Decimal
        self.LableDesi = QLabel(self)
        self.LableDesi.move(300, 190)
        self.LableDesi.setText('Number of decimals')
        self.LableDesi.setFont(self.font)

        self.Decimal = QSpinBox(self)
        self.Decimal.setObjectName(u"Decimal")
        self.Decimal.setGeometry(QRect(300, 220, 220, 100))
        self.Decimal.setStyleSheet("QAbstractSpinBox::up-button { width: 100px; height: 50px; }"
                                  "QAbstractSpinBox::down-button { width: 100px; height: 50px; }")
        self.Decimal.setMinimum(-5)
        self.Decimal.setMaximum(0)
        self.Decimal.setSingleStep(1)
        self.Decimal.setValue(-2)
        self.Decimal.valueChanged.connect(self.updateDecimal)
        #---------------------------------------------------- Save and close
        self.SaveButton = QPushButton("Save", self)
        self.SaveButton.setGeometry(287, 355, 283, 80)
        self.SaveButton.clicked.connect(self.Save)
        # ----------------------------------------------------Cancel
        self.CancelButton = QPushButton("Cancel", self)
        self.CancelButton.setGeometry(2, 355, 275, 80)
        self.CancelButton.clicked.connect(self.Cancel)

    def Cancel(self):
        self.hide()

    def Save(self):
        Config.Log.append('New values saved for the MPC')
        Config.MPC_Q_xp = round(self.k1Gain.value()*10, 5)
        Config.MPC_Q_xv = round(self.k2Gain.value()*10, 5)
        Config.MPC_R_Vin = round(self.k3Gain.value()*10, 5)
        self.hide()

    def updateDecimal(self):
        self.k1Gain.setSingleStep(10 ** (self.Decimal.value()))
        self.k2Gain.setSingleStep(10 ** (self.Decimal.value()))
        self.k3Gain.setSingleStep(10 ** (self.Decimal.value()))


#----------------------------------------------------------------------------Main GUI

class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()

        self.PID_config = PID_Config()
        self.ss_config = SS_Config()
        self.MPC_config = MPC_Config()

        self.setWindowTitle("3 DOF")
        self.setGeometry(0,0, 1280, 800)

        self.circle_rect = QRect(QPoint(50, 80), QPoint(750, 750))
        self.Target_ball_pos = None
        self.FB_ball = None
        self.log_string = []
        self.log_string_old = []
        self.font1 = QFont()
        self.font1.setPointSize(9)

        #------------------------------------------------------------------- Update Clock
        timer = QTimer(self)
        timer.timeout.connect(self.UpdateInformativeValues)
        timer.start(550)
        timer1 = QTimer(self)
        timer1.timeout.connect(self.UpdateFBBall)
        timer1.start(100)

        self.ExitButton = QPushButton('Exit', self)
        self.ExitButton.setGeometry(10, 10, 80, 60)
        self.ExitButton.setStyleSheet("background-color: red")
        self.ExitButton.clicked.connect(self.CloseButton)
        #-------------------------------------------------------------------- CPU Tmp

        self.CPUTmpLabel = QLabel("CPU Temp:  Crit at < 110",self)
        self.CPUTmpLabel.setGeometry(780,425,150,22)

        self.CPUTmp1 = QLabel(self)
        self.CPUTmp1.setGeometry(780,450,60,22)
        self.CPUTmp1.setFont(self.font1)
        self.CPUTmp1.setFrameShape(QFrame.Panel)

        self.CPUTmp2 = QLabel(self)
        self.CPUTmp2.setGeometry(850, 450, 60, 22)
        self.CPUTmp2.setFont(self.font1)
        self.CPUTmp2.setFrameShape(QFrame.Panel)
        # ------------------------------------------------------------------- box for buttons
        self.ControlerBox = QFrame(self)
        self.ControlerBox.setGeometry(660,105,580,60)
        self.ControlerBox.setFrameShape(QFrame.StyledPanel)
        self.ControlerBox.setLineWidth(2)

        #------------------------------------------------------------------- Controller selector
        self.ControlModeLable = QLabel(self)
        self.ControlModeLable.setGeometry(660, 85, 180, 20)
        self.ControlModeLable.setText("Controller settings: ")

        self.Controller = QComboBox(self)
        self.Controller.setFont(self.font1)
        self.Controller.addItem("No Control Mode selected")
        self.Controller.addItem("PID")
        self.Controller.addItem("StateSpace")
        self.Controller.addItem("MPC")
        self.Controller.setObjectName(u"comboBox1")
        self.Controller.setGeometry(QRect(670, 110, 190, 50))
        self.Controller.activated[str].connect(self.ControllerSelecter)
        # --------------------------------------------------------------------- Edit controller
        self.EditButton = QPushButton("...", self)
        self.EditButton.setGeometry(870, 110, 40, 50)
        self.EditButton.clicked.connect(self.toggle_window)
        #------------------------------------------------------------------- Input selector

        self.InputMode = QComboBox(self)
        self.InputMode.addItem("No Input selected")
        self.InputMode.addItem("Hunt (not implemented)")
        self.InputMode.addItem("Track (not implemented)")
        self.InputMode.setObjectName(u"comboBox2")
        self.InputMode.setGeometry(QRect(920, 110, 120, 50))
        self.InputMode.activated[str].connect(self.InputtModeSelector)

        # ------------------------------------------------------------------- Start Controller
        self.StartButton = QPushButton("Start", self)
        self.StartButton.setGeometry(1060, 110, 50, 50)
        self.StartButton.setCheckable(True)
        self.StartButton.setStyleSheet("background-color: red")
        self.StartButton.clicked.connect(self.StartButton1)
        self.StartButton.clicked.connect(self.on_button_clicked)

        # ------------------------------------------------------------------- Record data
        self.RecordData = QPushButton('Record Data', self)
        self.RecordData.setGeometry(1130, 110, 100, 50)
        self.RecordData.setCheckable(True)
        self.RecordData.setStyleSheet("background-color: red")
        self.RecordData.clicked.connect(self.on_button_clicked)
        self.RecordData.clicked.connect(self.StartValuesRecord)
        self.RecordData.pressed.connect(self.MPC_Snap_Shot_True)
        self.RecordData.released.connect(self.MPC_Snap_Shot_False)

        # ------------------------------------------------------------------- Box for camera buttons and lable
        self.CameraBoxLable = QLabel(self)
        self.CameraBoxLable.setGeometry(590, 2, 150, 12)
        self.CameraBoxLable.setText('Camera Buttons:')

        self.CameraBox = QFrame(self)
        self.CameraBox.setGeometry(590, 15, 280, 60)
        self.CameraBox.setFrameShape(QFrame.StyledPanel)
        self.CameraBox.setLineWidth(2)

        # --------------------------------------------------------------------- Start Camera
        self.StartCamera = QPushButton(self)
        self.StartCamera.setGeometry(600, 20, 50, 50)
        self.StartCamera.setCheckable(True)
        self.StartCamera.setStyleSheet("background-color: red")
        self.StartCamera.setIcon(QIcon('icons/Camera.svg.png'))
        self.StartCamera.clicked.connect(self.on_button_clicked)
        self.StartCamera.clicked.connect(self.CameraStart)

        self.CamerashowFrame = QPushButton('Frame', self)
        self.CamerashowFrame.setGeometry(670, 20, 50, 50)
        self.CamerashowFrame.setCheckable(True)
        self.CamerashowFrame.setStyleSheet("background-color: red")
        self.CamerashowFrame.clicked.connect(self.on_button_clicked)
        self.CamerashowFrame.clicked.connect(self.CameraShowFrame)

        self.CamerashowMask = QPushButton('Mask', self)
        self.CamerashowMask.setGeometry(740, 20, 50, 50)
        self.CamerashowMask.setCheckable(True)
        self.CamerashowMask.setStyleSheet("background-color: red")
        self.CamerashowMask.clicked.connect(self.on_button_clicked)
        self.CamerashowMask.clicked.connect(self.CameraShowMask)

        self.CameraStopReading = QPushButton(self)
        self.CameraStopReading.setGeometry(810, 20, 50, 50)
        self.CameraStopReading.setCheckable(True)
        self.CameraStopReading.setChecked(True)
        self.CameraStopReading.setStyleSheet("background-color: green")
        self.CameraStopReading.setIcon(QIcon('icons/Play_Pause.svg.png'))
        self.CameraStopReading.clicked.connect(self.on_button_clicked)
        self.CameraStopReading.clicked.connect(self.PauseAndSetCameraValues)

        # ------------------------------------------------------------------- Arduino box and lable

        self.ArduinoBoxLable = QLabel(self)
        self.ArduinoBoxLable.setGeometry(980, 2, 150, 12)
        self.ArduinoBoxLable.setText('Arduino Buttons:')

        self.ArduinoBox = QFrame(self)
        self.ArduinoBox.setGeometry(980, 15, 240, 60)
        self.ArduinoBox.setFrameShape(QFrame.StyledPanel)
        self.ArduinoBox.setLineWidth(2)

        # ------------------------------------------------------------------- Serial
        self.SerialConnect = QPushButton('Serial', self)
        self.SerialConnect.setGeometry(990, 20, 50, 50)
        self.SerialConnect.setCheckable(True)
        self.SerialConnect.setStyleSheet("background-color: red")
        self.SerialConnect.clicked.connect(self.on_button_clicked)
        self.SerialConnect.clicked.connect(self.StartSerialCom)

        # ------------------------------------------------------------------- Pause
        self.PausReadWriteConnect = QPushButton(self)
        self.PausReadWriteConnect.setGeometry(1060, 20, 50, 50)
        self.PausReadWriteConnect.setCheckable(True)
        self.PausReadWriteConnect.setChecked(True)
        self.PausReadWriteConnect.setStyleSheet("background-color: green")
        self.PausReadWriteConnect.setIcon(QIcon('icons/Play_Pause.svg.png'))
        self.PausReadWriteConnect.clicked.connect(self.on_button_clicked)
        self.PausReadWriteConnect.clicked.connect(self.PauseAndSetArduinoValues)

        # ------------------------------------------------------------------- Calibrate

        self.Calibrate = QPushButton('Calibrate', self)
        self.Calibrate.setGeometry(1130, 20, 80, 50)
        self.Calibrate.setCheckable(False)
        self.Calibrate.pressed.connect(self.CalibrateArduino_True)
        self.Calibrate.released.connect(self.CalibrateArduino_False)


        # ------------------------------------------------------------------- Stepper feedback angles

        self.Stepper1_lable = QLabel('Stepper 1', self)
        self.Stepper1_lable.setFont(self.font1)
        self.Stepper1_lable.setGeometry(335, 0, 100, 26)

        self.Stepper1_TargetValue   = QLabel(self)
        self.Stepper1_TargetValue.setFont(self.font1)
        self.Stepper1_TargetValue.setGeometry(335, 22, 160, 26)
        self.Stepper1_TargetValue.setFrameShape(QFrame.Panel)

        self.Stepper1_FeedbackValue = QLabel(self)
        self.Stepper1_FeedbackValue.setFont(self.font1)
        self.Stepper1_FeedbackValue.setGeometry(335, 50, 160, 26)
        self.Stepper1_FeedbackValue.setFrameShape(QFrame.Panel)

        self.Stepper2_lable = QLabel('Stepper 2', self)
        self.Stepper2_lable.setFont(self.font1)
        self.Stepper2_lable.setGeometry(660, 678, 100, 26)

        self.Stepper2_TargetValue = QLabel(self)
        self.Stepper2_TargetValue.setFont(self.font1)
        self.Stepper2_TargetValue.setGeometry(660, 700, 160, 26)
        self.Stepper2_TargetValue.setFrameShape(QFrame.Panel)

        self.Stepper2_FeedbackValue = QLabel(self)
        self.Stepper2_FeedbackValue.setFont(self.font1)
        self.Stepper2_FeedbackValue.setGeometry(660, 728, 160, 26)
        self.Stepper2_FeedbackValue.setFrameShape(QFrame.Panel)

        self.Stepper3_lable = QLabel('Stepper 3', self)
        self.Stepper3_lable.setFont(self.font1)
        self.Stepper3_lable.setGeometry(10, 678, 100, 26)

        self.Stepper3_TargetValue = QLabel(self)
        self.Stepper3_TargetValue.setFont(self.font1)
        self.Stepper3_TargetValue.setGeometry(10, 700, 160, 26)
        self.Stepper3_TargetValue.setFrameShape(QFrame.Panel)

        self.Stepper3_FeedbackValue = QLabel(self)
        self.Stepper3_FeedbackValue.setFont(self.font1)
        self.Stepper3_FeedbackValue.setGeometry(10, 728, 160, 26)
        self.Stepper3_FeedbackValue.setFrameShape(QFrame.Panel)

        # ------------------------------------------------------------------- Information

        self.TargetBoxLable = QLabel(self)
        self.TargetBoxLable.setGeometry(760, 172, 100, 12)
        self.TargetBoxLable.setText('Values: ')

        self.TargetBox = QFrame(self)
        self.TargetBox.setGeometry(760, 190, 500, 155)
        self.TargetBox.setFrameShape(QFrame.StyledPanel)
        self.TargetBox.setLineWidth(2)

        self.PositionX = QLabel(self)
        self.PositionX.setGeometry(765,215,150,20)
        self.PositionX.setText('Position x  : ')

        self.PositionY = QLabel(self)
        self.PositionY.setGeometry(765, 235, 150, 20)
        self.PositionY.setText('Position y  : ')

        self.VelX = QLabel(self)
        self.VelX.setGeometry(765, 255, 150, 20)
        self.VelX.setText('Velocity x  :')

        self.VelY = QLabel(self)
        self.VelY.setGeometry(765, 275, 150, 20)
        self.VelY.setText('Velocity y  :')

        self.AngleX = QLabel(self)
        self.AngleX.setGeometry(765, 295, 150, 20)
        self.AngleX.setText('Angle x     :')

        self.AngleY = QLabel(self)
        self.AngleY.setGeometry(765, 315, 150, 20)
        self.AngleY.setText('Angle y     :')

        #Target Column
        #Title
        self.TargetValues = QLabel(self)
        self.TargetValues.setGeometry(865, 190, 150, 20)
        self.TargetValues.setText('Target Values:')

        self.TargetPosX = QLabel(self)
        self.TargetPosX.setGeometry(895,215,150,20)

        self.TargetPosY = QLabel(self)
        self.TargetPosY.setGeometry(895, 235, 150, 20)

        self.TargetVelocityY = QLabel(self)
        self.TargetVelocityY.setGeometry(895, 255, 150, 20)

        self.TargetVelocityX = QLabel(self)
        self.TargetVelocityX.setGeometry(895, 275, 150, 20)

        self.TargetAngleX = QLabel(self)
        self.TargetAngleX.setGeometry(895, 295, 150, 20)

        self.TargetAngleY = QLabel(self)
        self.TargetAngleY.setGeometry(895, 315, 150, 20)

        #Feedback Column
        #Title
        self.FeedbackValues = QLabel(self)
        self.FeedbackValues.setGeometry(985, 190, 150, 20)
        self.FeedbackValues.setText('Feedback Values:')

        self.FeedbackPosX = QLabel(self)
        self.FeedbackPosX.setGeometry(1020, 215, 150, 20)

        self.FeedbackPosY = QLabel(self)
        self.FeedbackPosY.setGeometry(1020, 235, 150, 20)

        self.FeedbackVelocityY = QLabel(self)
        self.FeedbackVelocityY.setGeometry(1020, 255, 150, 20)

        self.FeedbackVelocityX = QLabel(self)
        self.FeedbackVelocityX.setGeometry(1020, 275, 150, 20)

        self.FeedbackAngleX = QLabel(self)
        self.FeedbackAngleX.setGeometry(1020, 295, 150, 20)

        self.FeedbackAngleY = QLabel(self)
        self.FeedbackAngleY.setGeometry(1020, 315, 150, 20)

        # Error Column
        # Title
        self.ErrorValues = QLabel(self)
        self.ErrorValues.setGeometry(1140, 190, 150, 20)
        self.ErrorValues.setText('Error:')

        self.ErrorPosX = QLabel(self)
        self.ErrorPosX.setGeometry(1155, 215, 150, 20)

        self.ErrorPosY = QLabel(self)
        self.ErrorPosY.setGeometry(1155, 235, 150, 20)

        self.ErrorVelocityY = QLabel(self)
        self.ErrorVelocityY.setGeometry(1155, 255, 150, 20)

        self.ErrorVelocityX = QLabel(self)
        self.ErrorVelocityX.setGeometry(1155, 275, 150, 20)

        self.ErrorAngleX = QLabel(self)
        self.ErrorAngleX.setGeometry(1155, 295, 150, 20)

        self.ErrorAngleY = QLabel(self)
        self.ErrorAngleY.setGeometry(1155, 315, 150, 20)

        #-------------------------------------------------------- Hz
        self.Hzbox = QFrame(self)
        self.Hzbox.setGeometry(760, 375, 500, 30)
        self.Hzbox.setFrameShape(QFrame.StyledPanel)
        self.Hzbox.setLineWidth(2)

        self.HzLable1 = QLabel('GUI Hz', self)
        self.HzLable1.move(790,350)

        self.GUIHz = QLabel(self)
        self.GUIHz.setGeometry(800, 380, 100, 20)

        self.HzLable2 = QLabel('Memory Hz', self)
        self.HzLable2.move(870, 350)

        self.SharedMemHz = QLabel(self)
        self.SharedMemHz.setGeometry(880, 380, 150, 20)

        self.HzLable3 = QLabel('BackEnd Hz', self)
        self.HzLable3.move(950, 350)

        self.BackEndHz = QLabel(self)
        self.BackEndHz.setGeometry(960, 380, 150, 20)

        self.HzLable4 = QLabel('Uart Hz', self)
        self.HzLable4.move(1030, 350)

        self.UartComHz = QLabel(self)
        self.UartComHz.setGeometry(1040, 380, 150, 20)

        self.HzLable5 = QLabel('Camera Hz', self)
        self.HzLable5.move(1100, 350)

        self.CameraHz = QLabel(self)
        self.CameraHz.setGeometry(1120, 380, 150, 20)

        self.HzLable6 = QLabel('Controller Hz', self)
        self.HzLable6.move(1180, 350)

        self.ControllerHz = QLabel(self)
        self.ControllerHz.setGeometry(1200, 380, 150, 20)

        # ------------------------------------------------------------------- Log Box

        self.LogBoxLable = QLabel(self)
        self.LogBoxLable.setGeometry(970,430, 160,20)
        self.LogBoxLable.setText('Information Box:')

        self.LogBox = QTextEdit(self)
        self.LogBox.setGeometry(970, 450, 300, 320)
        # -------------------------------------------------------------------


    def on_button_clicked(self):
        sender = self.sender()
        if sender.isChecked():
            sender.setStyleSheet("background-color: green")
        else:
            sender.setStyleSheet("background-color: red")

    # ------------------------------------------------------------------- Update Informative Values

    def UpdateInformativeValues(self):
        self.Stepper1_TargetValue.setText('Target Angle     : '+ str(round(Config.Stepper1_Target,3)))
        self.Stepper1_FeedbackValue.setText('Feedback Angle : '+ str(round(Config.Stepper1_Feedback,3)))

        self.Stepper2_TargetValue.setText('Target Angle     : ' + str(round(Config.Stepper2_Target,3)))
        self.Stepper2_FeedbackValue.setText('Feedback Angle : ' + str(round(Config.Stepper2_Feedback,3)))

        self.Stepper3_TargetValue.setText('Target Angle     : ' + str(round(Config.Stepper3_Target,3)))
        self.Stepper3_FeedbackValue.setText('Feedback Angle : ' + str(round(Config.Stepper3_Feedback,3)))

        self.TargetPosX.setText(str(Config.Target_Pos_x))
        self.TargetPosY.setText(str(Config.Target_Pos_y))
        self.TargetVelocityY.setText(str(Config.Target_Vel_x))
        self.TargetVelocityX.setText(str(Config.Target_Vel_y))
        self.TargetAngleX.setText(str(round(Config.U_rad_x/RtD, 3)))
        self.TargetAngleY.setText(str(round(Config.U_rad_y/RtD,3)))

        self.FeedbackPosX.setText(str(Config.cam_x))
        self.FeedbackPosY.setText(str(Config.cam_y))
        self.FeedbackVelocityY.setText(str(Config.cam_x_vel))
        self.FeedbackVelocityX.setText(str(Config.cam_y_vel))
        self.FeedbackAngleX.setText(str(Config.U_x_v_fb))
        self.FeedbackAngleY.setText(str(Config.U_y_v_fb))

        self.ErrorPosX.setText(str(round(Config.Target_Pos_x - Config.cam_x,2)))
        self.ErrorPosY.setText(str(round(Config.Target_Pos_y - Config.cam_y,2)))
        self.ErrorVelocityY.setText(str(-Config.cam_x_vel))
        self.ErrorVelocityX.setText(str(-Config.cam_y_vel))
        self.ErrorAngleX.setText(str(round(Config.U_rad_x/RtD - Config.U_x_v_fb,2)))
        self.ErrorAngleY.setText(str(round(Config.U_rad_y/RtD - Config.U_y_v_fb,2)))

        self.GUIHz.setText('X')
        self.SharedMemHz.setText(str(round(Config.SharedMem_Hz,2)))
        self.BackEndHz.setText(str(round(Config.BackEnd_Hz,2)))
        self.UartComHz.setText(str(round(Config.UartCom_Hz,2)))
        self.CameraHz.setText(str(round(Config.Cam_Hz, 1)))
        self.ControllerHz.setText(str(round(Config.Controller_Hz, 1)))
        # ------------------------------------------------------- CPU TMP
        if platform.system() == 'Linux':
            self.output = subprocess.check_output(['sensors'])
            self.temp1 = self.output.split()[5].decode()
            self.temp2 = self.output.split()[14].decode()
            self.CPUTmp1.setText(self.temp1)
            self.CPUTmp2.setText(self.temp2)
        else:
            self.CPUTmp1.setText('only linux')
            self.CPUTmp2.setText('only linux')

        #self.FB_ball = QPoint(400 +(700/400)*Config.cam_x, 400  -(700/400)*Config.cam_y)
        #if self.Target_ball_pos is None:
        #    self.Target_ball_pos =  QPoint(400, 400)
        #self.update()

        self.log_string = '\n'.join(Config.Log)

        if self.log_string != self.log_string_old:
            self.LogBox.setText(self.log_string)

        self.log_string_old = self.log_string

        if not Config.Camera_Runnig:
            self.CamerashowMask.setEnabled(False)
            self.CamerashowMask.setChecked(False)
            self.CamerashowMask.setStyleSheet("background-color: red")
            Config.Camera_show_Mask = 0
            self.CamerashowFrame.setEnabled(False)
            self.CamerashowFrame.setChecked(False)
            self.CamerashowFrame.setStyleSheet("background-color: red")
            Config.Camera_show_Frame = 0
        else:
            self.CamerashowMask.setEnabled(True)
            self.CamerashowFrame.setEnabled(True)



    def StartValuesRecord(self):
        if Config.Record_Data == False:
            Config.Record_Data = True
        else:
            Config.Record_Data = False

    def PauseAndSetArduinoValues(self):
        if Config.Paus_New_Arduino_Values == False:
            Config.Paus_New_Arduino_Values = True
        else:
            Config.Paus_New_Arduino_Values = False
    # ------------------------------------------------------------------- Start button action
    def StartButton1(self):
        if Config.Start == False:
            Config.Start = True
        else:
            Config.Start = False

    # ------------------------------------------------------------------- Camera

    def CameraStart(self):
        if Config.Camera_Start == False:
            Config.Camera_Start = True
        else:
            Config.Camera_Start = False

    def CameraShowFrame(self):
        if Config.Camera_show_Frame == 0:
            Config.Camera_show_Frame = 1
        else:
            Config.Camera_show_Frame = 0

    def CameraShowMask(self):
        if Config.Camera_show_Mask == 0:
            Config.Camera_show_Mask= 1
        else:
            Config.Camera_show_Mask = 0

    def PauseAndSetCameraValues(self):
        if Config.Camera_Pause < 0.0:
            Config.Camera_Pause = 12.34
        else:
            Config.Camera_Pause = -5.67


    #-------------------------------------------------------------------- Start Com
    def StartSerialCom(self):
        if Config.Start_Serial_Com == False:
            Config.Start_Serial_Com = True
        else:
            Config.Start_Serial_Com = False


    def StartI2CCom(self):
        if Config.Start_I2C_Com == False:
            Config.Start_I2C_Com = True
        else:
            Config.Start_I2C_Com = False

    def CalibrateArduino_True(self):
        if Config.Serial_Com_Running and not Config.Running:
            Config.Calibrate_Arduino = 10.56
            Config.Log.append('Calibrate signal')

    def CalibrateArduino_False(self):
        Config.Calibrate_Arduino = -5.65

    def MPC_Snap_Shot_True(self):
        if Config.Running and Config.Control_Mode == 'MPC' and not Config.Record_Data:
            if Config.MPC_SnapShot < 0.0:
                Config.MPC_SnapShot = 10.57
                Config.Log.append('MPC_Snap')

    def MPC_Snap_Shot_False(self):
        Config.MPC_SnapShot = -5.65

    # ------------------------------------------------------------------- Write Control Mode to config file
    def ControllerSelecter(self, text):
        Config.Control_Mode = text

    # ------------------------------------------------------------------- Write Input Mode to config file
    def InputtModeSelector(self, text):
        Config.Input_Mode = text

    def UpdateFBBall(self):
        self.FB_ball = QPoint(400 + (700 / 400) * Config.cam_x, 400 - (700 / 400) * Config.cam_y)
        if self.Target_ball_pos is None:
            self.Target_ball_pos = QPoint(400, 400)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        brush = QColor(0, 0, 0, 0)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawEllipse(self.circle_rect)

        if self.Target_ball_pos:

            brush1 = QColor(255, 0, 0)
            painter.setBrush(brush1)
            painter.drawEllipse(self.Target_ball_pos, 10, 10)
            brush2 = QColor(255, 255, 0)
            painter.setBrush(brush2)
            painter.drawEllipse(self.FB_ball, 5, 5)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.circle_rect.contains(event.pos()):
                Config.Target_Pos_x = round((400/700)*(-400 + event.x()), 1)
                Config.Target_Pos_y = round((400/700)*(400 - event.y()), 1)
                self.Target_ball_pos = event.pos()
                #self.update()

    def mouseMoveEvent(self, event):

        if self.circle_rect.contains(event.pos()):
            Config.Target_Pos_x = round((400/700)*(-400 + event.x()), 1)
            Config.Target_Pos_y = round((400/700)*(400 - event.y()), 1)
            self.Target_ball_pos = event.pos()
            #self.update()



    def EditConfig(self):
        print('ops')
        self.ss_config.show()
        ControllerCode = Config.Control_Mode + 'Config'

    def toggle_window(self):
        if Config.Control_Mode == 'PID':
            if not self.PID_config.isVisible():
                self.PID_config.setWindowFlags(Qt.WindowStaysOnTopHint)
                self.PID_config.show()
                self.PID_config.PGain.setValue(Config.PID_P_x)
                self.PID_config.DGain.setValue(Config.PID_D_x)
                self.PID_config.IGain.setValue(Config.PID_I_x)

        if Config.Control_Mode == 'StateSpace':
            if not self.ss_config.isVisible():
                self.ss_config.setWindowFlags(Qt.WindowStaysOnTopHint)
                self.ss_config.show()
                self.ss_config.k1Gain.setValue(Config.SS_k1_x/10)
                self.ss_config.k2Gain.setValue(Config.SS_k2_x/10)

        if Config.Control_Mode == 'MPC':
            if not self.MPC_config.isVisible():
                self.MPC_config.setWindowFlags(Qt.WindowStaysOnTopHint)
                self.MPC_config.show()
                self.MPC_config.k1Gain.setValue(Config.MPC_Q_xp/10)
                self.MPC_config.k2Gain.setValue(Config.MPC_Q_xv/10)
                self.MPC_config.k3Gain.setValue(Config.MPC_R_Vin/10)

    def CloseButton(self):
        # Display a confirmation dialog before quitting the application
        reply = QMessageBox.question(self, 'Confirm Exit', 'Are you sure you want to exit?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            QApplication.closeAllWindows()

    def closeEvent(self, event):
        # Set a flag to signal the threads to exit
        QApplication.closeAllWindows()
        Config.exit_flag = True



