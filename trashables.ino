#include<Servo.h>
#include<SPI.h>
#define servoPin 8
#define echoPin 6
#define trigPin 7
#define bin_distance 18
#define filled 5
<<<<<<< HEAD
#define echoPinDepth 3
#define trigPinDepth 4
#define LED 13
#define echoPinDepthRe 10
#define trigPinDepthRe 11
=======
#define echoPinDepth 4
#define trigPinDepth 5
#define LED 9
>>>>>>> origin/master

int flag;
int distance;
int depth;
<<<<<<< HEAD
int depthRe;
=======
>>>>>>> origin/master
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
  // put your setup code here, to run once:
  servo.attach(servoPin);
  servo.write(90);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(trigPinDepth, OUTPUT);
  pinMode(echoPinDepth, INPUT);
<<<<<<< HEAD
  pinMode(trigPinDepthRe, OUTPUT);
  pinMode(echoPinDepthRe, INPUT);
=======
>>>>>>> origin/master
  pinMode(LED, OUTPUT);
  //Serial.println("begin bridge");
  //Bridge.begin();
  Serial.begin(9600);
  //while(!Serial);
  //Serial.println("setup done!");
  delay(1000);
}

void loop() {
  distance = usRead(echoPin, trigPin);
  if (distance < bin_distance){
    Serial.println("python");
    while(Serial.available() <= 0);
    while(Serial.available()>0){
      flag = Serial.parseInt();
      if (flag == 0){
        left();
      }
      else{
        right();
      }
    }
    delay(5000);
    depth = usRead(echoPinDepth, trigPinDepth);
    if (depth < filled){
      Serial.println("full");
      digitalWrite(LED, HIGH);
    }
    else{
      digitalWrite(LED, LOW);
    }
<<<<<<< HEAD
    depthRe = usRead(echoPinDepthRe, trigPinDepthRe);
    if (depthRe < filled){
      Serial.println("fullre");
      digitalWrite(LED, HIGH);
    }
    else if (depth >= filled){
      digitalWrite(LED, LOW);
    }
=======
>>>>>>> origin/master
  }
  delay(1000);
}
