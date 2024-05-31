Let's create a Flask application that uses your `GeminiChatbot` class to handle incoming questions and return responses in JSON format. We'll include the necessary Docker configuration to ensure everything runs smoothly in a containerized environment.


### `requirements.txt`
Include all the dependencies needed for your project. Example:
```
Flask==2.0.1
python-dotenv==0.19.0
google-generativeai
requests
```

### `Dockerfile`
```Dockerfile
# Use a Python 3.10 image
FROM python:3.10.12

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy specific files to the container
COPY .env .
COPY offline_ai.py .
COPY hostedAI.py .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "hostedAI.py"]
```

### `.env`
Make sure to create a `.env` file with your Google API key.
```
GOOGLE_API_KEY=your_google_api_key_here
```

### Building and Running the Docker Container
1. Build the Docker image:
   ```sh
   docker build -t gemini-chatbot .
   ```

2. Run the Docker container:
   ```sh
   docker run -d -p 5000:5000 --name gemini-chatbot-container gemini-chatbot
   ```

### Testing the Flask App
You can test the Flask app by sending a POST request to `http://<host_ip>:5000/chat` with a JSON body. Example using `curl`:
```sh
curl -X POST http://<host_ip>:5000/chat -H "Content-Type: application/json" -d '{"input_text": "Do You know about lord Sri Krishna"}'
```

This setup will allow you to run your Flask-based chatbot globally using Docker, with all necessary dependencies and configurations.

The compilation errors you're encountering are related to missing or incorrect function calls in the ESPAsyncWebServer library. The issues seem to stem from changes in the mbedtls library and the ESP-IDF (Espressif IoT Development Framework) that the ESP32 uses. Specifically, some functions in the mbedtls library have been renamed, and the ets_printf function is missing.

To fix these issues, we need to update the ESPAsyncWebServer library source code. Here's how you can do it:

1. **Update the function names in WebAuthentication.cpp:**
   Replace the old mbedtls function names with the new ones:
   - mbedtls_md5_starts_ret -> mbedtls_md5_starts
   - mbedtls_md5_update_ret -> mbedtls_md5_update
   - mbedtls_md5_finish_ret -> mbedtls_md5_finish

2. **Remove or replace ets_printf in AsyncEventSource.cpp and AsyncWebSocket.cpp:**
   Since ets_printf is not available, you can replace it with Serial.printf if you need to print debug messages.

Here's how you can modify the specific parts of the library files:

### 1. Modifying WebAuthentication.cpp:

```cpp
#include "mbedtls/md5.h"

// Original function
bool getMD5(uint8_t* data, uint16_t len, char* outputBuffer) {
    mbedtls_md5_context _ctx;
    mbedtls_md5_init(&_ctx);
    mbedtls_md5_starts(&_ctx);  // Updated function name
    mbedtls_md5_update(&_ctx, data, len);  // Updated function name
    uint8_t _buf[16];
    mbedtls_md5_finish(&_ctx, _buf);  // Updated function name
    mbedtls_md5_free(&_ctx);
    for (uint8_t i = 0; i < 16; i++) {
        sprintf(outputBuffer + (i * 2), "%02x", _buf[i]);
    }
    return true;
}
```

### 2. Modifying AsyncEventSource.cpp:

```cpp
void AsyncEventSourceClient::_queueMessage(AsyncEventSourceMessage* dataMessage) {
    if (_messageQueue.length() > 32) {
        Serial.printf("ERROR: Too many messages queued\n");  // Replaced ets_printf with Serial.printf
        delete dataMessage;
        return;
    }
    _messageQueue.add(dataMessage);
}
```

### 3. Modifying AsyncWebSocket.cpp:

```cpp
void AsyncWebSocketClient::_queueMessage(AsyncWebSocketMessage* dataMessage) {
    if (_messageQueue.length() > 32) {
        Serial.printf("ERROR: Too many messages queued\n");  // Replaced ets_printf with Serial.printf
        delete dataMessage;
        return;
    }
    _messageQueue.add(dataMessage);
}
```

After making these changes, save the modified files. Now, try compiling your code again. This should resolve the errors related to missing function declarations and the ets_printf issue.

### Complete main.cpp file for reference:

```cpp
#include <WiFi.h>
#include <WiFiUdp.h>

// Replace with your network credentials
const char* ssid = "LocalNetwork";
const char* password = "sukarna jana";

// Define the LED pin
const int ledPin = 2;

// Create a WiFiUDP object
WiFiUDP udp;

// Define the port for UDP communication
const int udpPort = 12345;

// Buffer to hold incoming data
char incomingPacket[255];

void setup() {
  // Start the Serial communication to send messages to the computer
  Serial.begin(115200);
  delay(10);

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

    // Print RSSI
    int rssi = WiFi.RSSI();
    Serial.println("RSSI: " + String(rssi) + " dBm");
  }

  // Print free heap memory periodically
  static unsigned long lastHeapLogTime = 0;
  if (millis() - lastHeapLogTime > 5000) {
    //Serial.printf( ESP.getFreeHeap());
    lastHeapLogTime = millis();
  }
}

void DebugMonitoring(String message) {
  Serial.println("Received message from UDP:");
  Serial.println(message);
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
```

This code sets up a WebSocket server on the ESP32, allowing it to control the built-in LED based on WebSocket connections and data received.