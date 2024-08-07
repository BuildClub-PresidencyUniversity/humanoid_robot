#include <WiFi.h>
#include <WiFiUdp.h>
#include <Adafruit_PWMServoDriver.h>

// WiFi credentials
const char* ssid = "LocalNetwork";
const char* password = "sukarna jana";

// UDP
WiFiUDP udp;
const int udpPort = 12345;
char incomingPacket[255];

// Adafruit PCA9685
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

unsigned long eyePreviousMillis = 0;
const int eyeInterval = 1000;
bool eyeState = false;
unsigned long nextEyeMoveTime = 0;
unsigned long eyeMoveIntervalMin = 2000;
unsigned long eyeMoveIntervalMax = 5000;

// Flags
bool keepSpeaking = false;

// Function Prototypes
void connectToWiFi();
void scheduleNextEyeMove();
void handleInputs();
void moveNeckRight();
void moveNeckLeft();
void moveNeckCenter();
void speak();
void stopSpeaking();
void eye();
void DebugMonitoring(String message);
void sendAcknowledgment(const char* message);

void setup() {
  // Serial
  Serial.begin(115200);
  delay(10);

  // WiFi
  connectToWiFi();

  // UDP
  udp.begin(udpPort);
  Serial.printf("Now listening on UDP port %d\n", udpPort);

  // Servo control
  Serial.println("PCA9685 Servo control");
  pwm.begin();
  pwm.setPWMFreq(60);

  scheduleNextEyeMove();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Disconnected from WiFi. Reconnecting...");
    connectToWiFi();
  }

  // Handle UDP packets
  int packetSize = udp.parsePacket();
  if (packetSize) {
    int len = udp.read(incomingPacket, sizeof(incomingPacket) - 1);
    if (len > 0) {
      incomingPacket[len] = 0; // Null-terminate the string
    }
    DebugMonitoring(String(incomingPacket));
  }

  // Continuous speaking if the flag is set
  if (keepSpeaking) {
    speak();
  }

  // Call eye() function randomly after handleInputs()
  if (millis() >= nextEyeMoveTime) {
    eye();
    scheduleNextEyeMove();
  }
}

void connectToWiFi() {
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi. IP address: " + WiFi.localIP().toString());
}

void scheduleNextEyeMove() {
  nextEyeMoveTime = millis() + random(eyeMoveIntervalMin, eyeMoveIntervalMax);
}

void moveNeckRight() {
  pwm.setPWM(2, 0, 120);
  delay(500);
}

void moveNeckLeft() {
  pwm.setPWM(2, 0, 500);
  delay(500);
}

void moveNeckCenter() {
  pwm.setPWM(2, 0, 285);
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

void stopSpeaking() {
  pwm.setPWM(1, 0, 220); // Open
}

void eye() {
  unsigned long currentMillis = millis();
  
  if (currentMillis - eyePreviousMillis >= eyeInterval) {
    eyePreviousMillis = currentMillis;
    
    if (eyeState == false) {
      pwm.setPWM(0, 0, 660);
      eyeState = true;
    } else {
      pwm.setPWM(0, 0, 115);
      eyeState = false;
    }
  }
}

void DebugMonitoring(String message) {
  Serial.println(message);
  if (message == "t") {
    keepSpeaking = true;
    Serial.println("Talking");
    sendAcknowledgment("Talking");
  } else if (message == "s") {
    keepSpeaking = false;
    stopSpeaking();
    Serial.println("Stopped");
    sendAcknowledgment("Stopped");
  } else if (message == "c") {
    moveNeckCenter();
    Serial.println("Center");
    sendAcknowledgment("Center");
  } else if (message == "r") {
    moveNeckRight();
    Serial.println("Right");
    sendAcknowledgment("Right");
  } else if (message == "l") {
    moveNeckLeft();
    Serial.println("Left");
    sendAcknowledgment("Left");
  }
}

void sendAcknowledgment(const char* message) {
  udp.beginPacket(udp.remoteIP(), udp.remotePort());
  udp.write((uint8_t*)message, strlen(message));
  udp.endPacket();
}