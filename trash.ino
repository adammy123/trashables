#include<Servo.h>
#include<SPI.h>
#define servoPin 8

int flag;
Servo servo;

void left(){
  servo.write(145);
  delay(1000);
  servo.write(90);
}

void right(){
  servo.write(35);
  delay(1000);
  servo.write(90);
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  servo.attach(servoPin);
  servo.write(90);
}

void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available()>0){
    flag = Serial.parseInt();
    Serial.println(flag);
    if (flag == 0){
      left();
    }
    else{
      right();
    }
    delay(100);
  }
}
