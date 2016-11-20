#include<Servo.h>
#define servoPin 8

Servo servo;

void left(){
  servo.write(145);
  delay(2000);
  servo.write(90);
}

void right(){
  servo.write(35);
  delay(2000);
  servo.write(90);
}

void setup() {
  // put your setup code here, to run once:
  servo.attach(servoPin);
  servo.write(90);
  Serial.begin(9600);
  while(!Serial);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("going right...");
  right();
  delay(2000);
  
}
