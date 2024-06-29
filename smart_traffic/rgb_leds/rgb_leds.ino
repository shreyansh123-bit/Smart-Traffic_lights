const int Left_street_green = 8;
const int Right_street_green = 4;

void setup() {
    pinMode(8,OUTPUT);
    pinMode(4,OUTPUT);
}

void loop() {
    digitalWrite(Left_street_green,0);
    digitalWrite(Right_street_green,1);
  delay(1000);
  digitalWrite(Left_street_green,1);
    digitalWrite(Right_street_green,0);
}
