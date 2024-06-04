#include <Arduino.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

unsigned long eyePreviousMillis = 0;
const int eyeInterval = 1000; // Interval between eye movements in milliseconds
bool eyeState = false;

unsigned long nextEyeMoveTime = 0;
unsigned long eyeMoveIntervalMin = 2000; // Minimum time between eye movements in milliseconds
unsigned long eyeMoveIntervalMax = 5000; // Maximum time between eye movements in milliseconds

#define one 2
#define two 3
#define three 4
#define four 5
#define tpin 6
#define spin 7

void setup() {
  Serial.begin(115200);
  delay(10);

  Serial.println("PCA9685 Servo control");
  pwm.begin();
  pwm.setPWMFreq(60);

  pinMode(one, INPUT);
  pinMode(two, INPUT);
  pinMode(three, INPUT);
  pinMode(four, INPUT);
  pinMode(tpin, INPUT);
  pinMode(spin, INPUT);

  scheduleNextEyeMove();
}

void loop() {
  handleInputs();
  //eye();
  // If tpin is HIGH, keep speaking until spin gets HIGH or tpin goes LOW
  if (digitalRead(tpin) == HIGH) {
    while (digitalRead(tpin) == HIGH && digitalRead(spin) == LOW) {
      speak();
      eye(); // Call eye function in the loop while speaking
    }
  }
  // Call eye() function randomly after handleInputs()
  if (millis() >= nextEyeMoveTime) {
    eye();
    scheduleNextEyeMove();
  }
}

void scheduleNextEyeMove() {
  nextEyeMoveTime = millis() + random(eyeMoveIntervalMin, eyeMoveIntervalMax);
}

void handleInputs() {
  int oneState = digitalRead(one);
  int twoState = digitalRead(two);
  int threeState = digitalRead(three);
  int fourState = digitalRead(four);

  if (oneState == HIGH) {
    moveNeckRight();
  }

  if (twoState == HIGH) {
    moveNeckLeft();
  }

  if (threeState == HIGH) {
    moveNeckCenter();
  }

  if (fourState == HIGH) {
    speak();
  }
}

void moveNeckRight() {
  pwm.setPWM(2, 0, 120); // Adjust the PWM value as needed
  delay(500);
}

void moveNeckLeft() {
  pwm.setPWM(2, 0, 500); // Adjust the PWM value as needed
  delay(500);
}

void moveNeckCenter() {
  pwm.setPWM(2, 0, 285); // Adjust the PWM value as needed
  delay(500);
}

void speak() {
  pwm.setPWM(1, 0, 220); // Close
  delay(150);
  pwm.setPWM(1, 0, 260); // Open
  delay(150);
  pwm.setPWM(1, 0, 220); // Close
  delay(150);
  pwm.setPWM(1, 0, 260); // Open
  delay(150);
  pwm.setPWM(1, 0, 220); // Close
  delay(150);
}

void eye() {
  unsigned long currentMillis = millis();
  
  if (currentMillis - eyePreviousMillis >= eyeInterval) {
    eyePreviousMillis = currentMillis;
    
    if (eyeState == false) {
      pwm.setPWM(0, 0, 660); // Adjust the PWM value as needed
      eyeState = true;
    } else {
      pwm.setPWM(0, 0, 115); // Adjust the PWM value as needed
      eyeState = false;
    }
  }
}