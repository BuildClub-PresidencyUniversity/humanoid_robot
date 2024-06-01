#include <WiFi.h>
#include <WiFiUdp.h>

// Replace with your network credentials
const char* ssid = "LocalNetwork";
const char* password = "sukarna jana";

// Define the LED pin
const int ledPin = 2;
#define tpin 5
#define spin 18

// Create a WiFiUDP object
WiFiUDP udp;

// Define the port for UDP communication
const int udpPort = 12345;

// Buffer to hold incoming data
char incomingPacket[255];

void setup() {
  // Start the Serial communication to send messages to the computer
  Serial.begin(115200);    // Serial Monitor
  delay(10);


  pinMode(tpin, OUTPUT);
  pinMode(spin, OUTPUT);
  // Initialize the LED pin
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW); // Turn off LED (HIGH is OFF for built-in LED on ESP32)

  connectToWiFi();

  // Start UDP
  udp.begin(udpPort);
  Serial.printf("Now listening on UDP port %d\n", udpPort);

  // Print initial free heap memory
  Serial.printf("Initial free heap: %d bytes\n", ESP.getFreeHeap());
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Disconnected from WiFi. Reconnecting...");
    connectToWiFi();
  }

  // Check if there are any incoming UDP packets
  int packetSize = udp.parsePacket();
  if (packetSize) {
    // Read the packet into the buffer
    int len = udp.read(incomingPacket, sizeof(incomingPacket) - 1);
    if (len > 0) {
      incomingPacket[len] = 0; // Null-terminate the string
    }
    DebugMonitoring(String(incomingPacket));

    // Send the received message back to the client
    udp.beginPacket(udp.remoteIP(), udp.remotePort());
    udp.write((uint8_t*)incomingPacket, len);
    udp.endPacket();

  }

  // Print free heap memory periodically
  static unsigned long lastHeapLogTime = 0;
  if (millis() - lastHeapLogTime > 5000) {
    //Serial.printf( ESP.getFreeHeap());
    lastHeapLogTime = millis();
  }

}

void DebugMonitoring(String message) {
 // Serial.println("Received message from UDP:");
  Serial.println(message);
  if(message == "t")
  {
    digitalWrite(tpin, HIGH);
    digitalWrite(spin, LOW);

  }
  else if (message == "s")
  {
    digitalWrite(spin, HIGH);
    digitalWrite(tpin, LOW);

  }
  else 
  {
    digitalWrite(tpin, LOW);
    digitalWrite(spin, LOW);
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