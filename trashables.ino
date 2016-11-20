#include<Servo.h>
#include<SPI.h>
#define LEDRe 2
#define echoRe 3
#define trigRe 4
#define echoObj 6
#define trigObj 7
#define servoPin 8
#define echoWaste 10
#define trigWaste 11
#define LEDWaste 12

#define filled_distance 5
#define bin_distance 18

int flag;
int distance;
int depthRe;
int depthWaste;
Servo servo;

int usRead(int echo, int trig){
  long duration, distance;
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig,HIGH);
  delayMicroseconds(10);
  digitalWrite(trig,LOW);
  duration = pulseIn(echo, HIGH);
  distance = (duration/2)/29.1;
  return distance;
}


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

  //initialize servo and set to horizontal
  servo.attach(servoPin);
  servo.write(90);

  //initialize LED pins
  pinMode(LEDRe, OUTPUT); 
  pinMode(LEDWaste, OUTPUT);
  digitalWrite(LEDRe, LOW);
  digitalWrite(LEDWaste, LOW);

  //initialize ultrasonic sensor pins
  pinMode(trigRe, OUTPUT);
  pinMode(echoRe, INPUT);
  pinMode(trigObj, OUTPUT);
  pinMode(echoObj, INPUT);
  pinMode(trigWaste, OUTPUT);
  pinMode(echoWaste, INPUT);

  Serial.begin(9600);
  while(!Serial);
}

void loop() {
  //to detect trash being deposited
  distance = usRead(echoObj, trigObj);

  //if there is trash detected
  if (distance < bin_distance){
    Serial.println("python");

    //wait for python to send signal
    while(Serial.available() <= 0);
    
    while(Serial.available()>0){
      //sorts trash according to label assigned by clarifai
      flag = Serial.parseInt();
      if (flag == 0){
        left();
      }
      else{
        right();
      }
    }
    delay(5000);

    //read depth of recycling bin
    depthRe = usRead(echoRe, trigRe);
    if (depthRe < filled_distance){
      Serial.println("fullrecycle");
      digitalWrite(LEDRe, HIGH);
    }
    else{
      digitalWrite(LEDRe, LOW);
    }

    //read depth of waste bin
    depthWaste = usRead(echoWaste, trigWaste);
    if (depthWaste < filled_distance){
      Serial.println("fullwaste");
      digitalWrite(LEDWaste, HIGH);
    }
    else{
      digitalWrite(LEDWaste, LOW);
    }
  }
  delay(1000);
}
