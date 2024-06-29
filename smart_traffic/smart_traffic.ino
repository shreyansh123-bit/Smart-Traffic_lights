const int greenLightLeft=3;
const int greenLightRight=4;
const int redLightLeft=9;
const int redLightRight=8;

const int on = 0;
const int off = 1;    //assuming light turns on high current

int incomingByte = 0;  // for incoming serial data

void setup() {
  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
  pinMode(greenLightLeft, OUTPUT); // set the LED pin mode
  pinMode(greenLightRight, OUTPUT);
  pinMode(redLightLeft, OUTPUT);
  pinMode(redLightRight, OUTPUT);
  pinMode(13,OUTPUT);
  pinMode(12,OUTPUT);
  digitalWrite(12,1);
}

void loop() {
  // check if data is available to read
  if (Serial.available() > 0) {
    // read the incoming byte
    incomingByte = Serial.read();

    // check if the incoming byte is '1' or '0'
    if (incomingByte == '1') {
      //left => green right=>red
      digitalWrite(greenLightLeft,on);
      digitalWrite(redLightRight,on);
       digitalWrite(greenLightRight,off);
      digitalWrite(redLightLeft,off);

         digitalWrite(13,1);
    } else if (incomingByte == '0') {
      //right => green left=> red
      digitalWrite(greenLightRight,on);
      digitalWrite(redLightLeft,on);
       digitalWrite(greenLightLeft,off);
      digitalWrite(redLightRight,off);
        digitalWrite(13,0);    }
  }
}
