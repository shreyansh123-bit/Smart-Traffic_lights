#include <Servo.h>

// Create servo objects
Servo rightservo;
Servo leftservo;

// Constants for servo positions
const int OPEN = 10;
const int CLOSE = 95;

#define LEFT_MOTOR_PIN 9
#define RIGHT_MOTOR_PIN 6
// Constants for LED states
#define OFF 1
#define ON 0

// Pin assignments

#define RED_LEFT_PIN 8
#define GREEN_LEFT_PIN 7
const int RED_RIGHT_PIN =4;
const int GREEN_RIGHT_PIN = 3;
#define INDICATOR_PIN 13

// Function to turn on left green light and move servos
void leftGreenLight() {
  digitalWrite(GREEN_LEFT_PIN, ON);
  digitalWrite(RED_LEFT_PIN, OFF);
  digitalWrite(GREEN_RIGHT_PIN, OFF);  // Turn off green right light
  digitalWrite(RED_RIGHT_PIN, ON);     // Turn on red right light
  rightservo.write(CLOSE);
  leftservo.write(CLOSE);
  digitalWrite(INDICATOR_PIN, LOW);    // Turn off indicator
}

// Function to turn on right green light and move servos
void rightGreenLight() {
  digitalWrite(GREEN_RIGHT_PIN, ON);   // Turn on green right light
  digitalWrite(RED_RIGHT_PIN, OFF);    // Turn off red right light
  digitalWrite(GREEN_LEFT_PIN, OFF);
  digitalWrite(RED_LEFT_PIN, ON);
  rightservo.write(OPEN);
  leftservo.write(OPEN);
  digitalWrite(INDICATOR_PIN, HIGH);   // Turn on indicator
}

// Setup function to initialize pin modes and servo positions
void setup() {
  pinMode(GREEN_LEFT_PIN, OUTPUT);
  pinMode(RED_LEFT_PIN, OUTPUT);
  pinMode(GREEN_RIGHT_PIN, OUTPUT);
  pinMode(RED_RIGHT_PIN, OUTPUT);

  pinMode(12, OUTPUT); 
  pinMode(8,OUTPUT);
  pinMode(5,OUTPUT);

  digitalWrite(8,HIGH);
  digitalWrite(5,LOW);
  digitalWrite(12, HIGH);

  rightservo.attach(RIGHT_MOTOR_PIN);
  leftservo.attach(LEFT_MOTOR_PIN);

  rightservo.write(CLOSE); // Initialize servos to a known position
  leftservo.write(CLOSE);  // Initialize servos to a known position

  Serial.begin(9600);
  pinMode(INDICATOR_PIN, OUTPUT);

  Serial.println("Setup complete");
}

// Loop function to read serial input and control lights and servos
void loop() {
  if (Serial.available() > 0) {
    char incoming = Serial.read(); // Read the incoming byte
    Serial.print("Received: ");
    Serial.println(incoming);
    if (incoming == '1') {
      rightGreenLight();
    } else if (incoming == '0') {
      leftGreenLight();
    }
  }
}
