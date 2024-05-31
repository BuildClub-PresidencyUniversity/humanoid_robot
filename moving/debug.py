import socket

def send_message(esp32_ip, esp32_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2.0)  # Set timeout for blocking operations

    while True:
        # Prompt the user for input
        message = input("Enter a message to send to the ESP32 (or type 'exit' to quit): ")

        if message.lower() == 'exit':
            print("Exiting...")
            break

        # Check if the message is empty
        if not message.strip():
            print("Message cannot be empty. Please enter a valid message.")
            continue

        try:
            # Send the message to the ESP32
            print(f"Sending: {message}")
            sock.sendto(message.encode(), (esp32_ip, esp32_port))

            # Receive the response from the ESP32
            response, _ = sock.recvfrom(1024)
            print(f"Received: {response.decode()}")
        except socket.timeout:
            print("Error: Request timed out.")
        except Exception as e:
            print(f"Error: Failed to send data to ESP32 server: {e}")

def main():
    # Prompt the user for the ESP32 IP address
    esp32_ip = input("Enter the IP address of your ESP32: ")
    esp32_port = 12345  # Use the same port number as in your ESP32 code

    # Run the send_message function
    send_message(esp32_ip, esp32_port)

if __name__ == "__main__":
    main()
