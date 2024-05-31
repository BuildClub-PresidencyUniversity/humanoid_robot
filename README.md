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
```

This code sets up a WebSocket server on the ESP32, allowing it to control the built-in LED based on WebSocket connections and data received.