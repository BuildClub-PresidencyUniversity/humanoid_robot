#include <WiFi.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>

// Replace with your network credentials
const char* ssid = "LocalNetwork";
const char* password = "sukarna jana";

// Create an AsyncWebServer object on port 80
AsyncWebServer server(80);

// Create a WebSocket object
AsyncWebSocket ws("/ws");

// Define the LED pin
const int ledPin = LED_BUILTIN;

void onWsEvent(AsyncWebSocket * server, AsyncWebSocketClient * client, AwsEventType type, void * arg, uint8_t * data, size_t len) {
  if (type == WS_EVT_CONNECT) {
    Serial.println("WebSocket client connected");
    digitalWrite(ledPin, LOW); // Turn on LED (LOW is ON for built-in LED on ESP32)
  } else if (type == WS_EVT_DISCONNECT) {
    Serial.println("WebSocket client disconnected");
    digitalWrite(ledPin, HIGH); // Turn off LED (HIGH is OFF for built-in LED on ESP32)
  } else if (type == WS_EVT_DATA) {
    String msg = "";
    for (size_t i = 0; i < len; i++) {
      msg += (char) data[i];
    }
    DebugMonitoring(msg);
    // Echo the message back to the client
    client->text(msg);
  }
}

void setup() {
  // Start the Serial communication to send messages to the computer
  Serial.begin(115200);
  delay(10);

  // Initialize the LED pin
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH); // Turn off LED (HIGH is OFF for built-in LED on ESP32)

  // Connect to Wi-Fi network
  WiFi.begin(ssid, password);

  Serial.print("Connecting to ");
  Serial.print(ssid);
  Serial.println("...");

  // Wait for the Wi-Fi to connect
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // Attach WebSocket event handler
  ws.onEvent(onWsEvent);
  server.addHandler(&ws);

  // Start the server
  server.begin();
  Serial.println("HTTP server started");

  // Print initial free heap memory
  Serial.printf("Initial free heap: %d bytes\n", ESP.getFreeHeap());
}

void loop() {
  // Print free heap memory periodically
  static unsigned long lastHeapLogTime = 0;
  if (millis() - lastHeapLogTime > 5000) {
    Serial.printf("Free heap: %d bytes\n", ESP.getFreeHeap());
    lastHeapLogTime = millis();
  }
}

void DebugMonitoring(String message) {
  Serial.println("Received message from WebSocket:");
  Serial.println(message);
}