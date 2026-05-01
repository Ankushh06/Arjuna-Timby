#include <Servo.h>

int incomingByte = 0;
String inputString = "";
boolean newLineReceived = false;
boolean startBit  = false;

Servo servoX;
Servo servoY;

String motor;
int angle;

void setup(){
  Serial.begin(115200);

  servoX.attach(9);
  servoY.attach(10);

  servoX.write(90);
  servoY.write(90);
}

void loop(){
  readSerial();
}

void readSerial() {
  while (Serial.available())
  {
    incomingByte = Serial.read();

    if (incomingByte == '%') {
      inputString = "";
      startBit = true;
    }

    if (startBit) {
      inputString += (char) incomingByte;
    }

    if (incomingByte == '#') {
      startBit = false;
      newLineReceived = true;
    }

    if (newLineReceived) {
      String received_DATA = inputString.substring(1, inputString.length() - 1);

      motor = received_DATA.substring(0,1);
      angle = received_DATA.substring(1).toInt();

      angle = constrain(angle, 0, 180);

      if (motor == "X") servoX.write(angle);
      if (motor == "Y") servoY.write(angle);

      inputString = "";
      newLineReceived = false;
    }
  }
}