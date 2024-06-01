#include <Arduino.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

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
}

void loop() {
  handleInputs();

  // If tpin is HIGH, keep speaking until spin gets HIGH or tpin goes LOW
  if (digitalRead(tpin) == HIGH) {
    while (digitalRead(tpin) == HIGH && digitalRead(spin) == LOW) {
      speak();
    }
  }
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
