#include "FastAccelStepper.h"
#include "AVRStepperPins.h"

#define SW_1         10
#define SW_2         11
#define SW_3         12

#define Pul_1        6
#define Dir_1        51

#define Pul_2        7
#define Dir_2        52

#define Pul_3        8
#define Dir_3        53

int sensorVal_1 = LOW;
int sensorVal_2 = LOW; 
int sensorVal_3 = LOW; 

int Old_SW1 = LOW;
int Old_SW2 = LOW;
int Old_SW3 = LOW;

float Calibrate_signal = -5.65;

float Target_1 = 0.0;
float Target_2 = 0.0;
float Target_3 = 0.0;

int Target_1_s = 0;
int Target_2_s = 0;
int Target_3_s = 0;

int Current_1_is = 0;
int Current_2_is = 0;
int Current_3_is = 0;

int Pos_1_s = int(-165*0.78)*2; // 800s
int Pos_2_s = int(-165*0.78)*2; // 800s
int Pos_3_s = int(-165*0.78)*2; // 800s

float DegToStep = 1600/360;

float Current_1_d = 0.0;
float Current_2_d = 0.0;
float Current_3_d = 0.0;
float values[5];

FastAccelStepperEngine engine = FastAccelStepperEngine();
FastAccelStepper *stepper_1 = NULL;
FastAccelStepper *stepper_2 = NULL;
FastAccelStepper *stepper_3 = NULL;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  pinMode(SW_1      , INPUT);
  pinMode(SW_2      , INPUT);
  pinMode(SW_3      , INPUT);

  engine.init();
  stepper_1 = engine.stepperConnectToPin(Pul_1);
  stepper_2 = engine.stepperConnectToPin(Pul_2);
  stepper_3 = engine.stepperConnectToPin(Pul_3);
  stepper_1->setDirectionPin(Dir_1, false);
  stepper_2->setDirectionPin(Dir_2, false);
  stepper_3->setDirectionPin(Dir_3, false);
    
  stepper_1->setSpeedInHz(2600);       // 500 steps/s
  stepper_1->setAcceleration(10000);    // 100 steps/s²

  stepper_2->setSpeedInHz(2600);       // 500 steps/s
  stepper_2->setAcceleration(10000);    // 100 steps/s²

  stepper_3->setSpeedInHz(2600);       // 500 steps/s
  stepper_3->setAcceleration(10000);    // 100 steps/s²
  Calibrate();
}
//----------------------------------------------------- loop
void loop() {
  UsbCom();

  if (Calibrate_signal >= 0){
    Calibrate();
  }
  sensorVal_1 = digitalRead(SW_1);
  sensorVal_2 = digitalRead(SW_2);
  sensorVal_3 = digitalRead(SW_3);

  if ((sensorVal_1)&& !(Old_SW1)){
       stepper_1->forceStopAndNewPosition(Pos_1_s);    
  }
  if ((sensorVal_2)&& !(Old_SW2)){
       stepper_2->forceStopAndNewPosition(Pos_2_s);
      
  }
  if ((sensorVal_3)&& !(Old_SW3)){
       stepper_3->forceStopAndNewPosition(Pos_3_s);   
  }

  Current_1_is = stepper_1->getCurrentPosition();
  Current_2_is = stepper_2->getCurrentPosition();
  Current_3_is = stepper_3->getCurrentPosition();
  Current_1_d = Current_1_is/DegToStep;
  Current_2_d = Current_2_is/DegToStep;
  Current_3_d = Current_3_is/DegToStep;

  Target_1_s = int(Target_1*DegToStep);
  Target_2_s = int(Target_2*DegToStep);
  Target_3_s = int(Target_3*DegToStep);

  stepper_1->moveTo(Target_1_s);
  stepper_2->moveTo(Target_2_s);
  stepper_3->moveTo(Target_3_s); 

  Old_SW1 = sensorVal_1;
  Old_SW2 = sensorVal_2;
  Old_SW3 = sensorVal_3; 
}

void UsbCom(){
  if (Serial.available() >= 16) { // Wait for 12 bytes (3 floats)
    
    Serial.readBytes((char*)values, 16);
    Target_1 = values[0];
    Target_2 = values[1];
    Target_3 = values[2];
    Calibrate_signal = values[3];
    Serial.print(Current_1_d);
    Serial.print(" ");
    Serial.print(Current_2_d);
    Serial.print(" ");
    Serial.print(Current_3_d);
    Serial.print(" ");
    Serial.println(Calibrate_signal);
    
  }
}

void Calibrate(){
  bool Start = HIGH;
  while (Start){
    UsbCom();
    sensorVal_1 = digitalRead(SW_1);
    sensorVal_2 = digitalRead(SW_2);
    sensorVal_3 = digitalRead(SW_3);

    if (sensorVal_1 and sensorVal_2 and sensorVal_3){
      Start = LOW;
      break;
    }
    if (!sensorVal_1){
      stepper_1->move(-1);
    }else{
      stepper_1->forceStop();
    }

    if (!sensorVal_2){
      stepper_2->move(-1);
    }else{
      stepper_2->forceStop();
    }

    if (!sensorVal_3){
      stepper_3->move(-1);
    }else{
      stepper_3->forceStop();
    }
  
  delay(5);
  }
  stepper_1->forceStopAndNewPosition(Pos_1_s);
  stepper_2->forceStopAndNewPosition(Pos_2_s);
  stepper_3->forceStopAndNewPosition(Pos_3_s);
  Target_1_s = 0;
  Target_2_s = 0;
  Target_3_s = 0;
  Calibrate_signal = -5.65;
  delay(1000);
}
