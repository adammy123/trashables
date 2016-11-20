int distance;

int usRead(int echo, int trig){
  long duration, distance;
  
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig,HIGH);
  delayMicroseconds(10);
  digitalWrite(trig,LOW);
  duration = pulseIn(echo, HIGH);
  distance = (duration/2)/29.1;
  
  Serial.print (distance);
  Serial.println (" cm");
  
  return distance;
}

void setup() {
  // put your setup code here, to run once:
  pinMode(7, OUTPUT);
  pinMode(6, INPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  distance = usRead(6, 7);
  delay(1000);
}
