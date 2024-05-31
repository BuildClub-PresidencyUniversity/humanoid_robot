import socket

class RobotUDPClient:
    def __init__(self, esp32_ip, esp32_port=12345):
        self.esp32_ip = esp32_ip
        self.esp32_port = esp32_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(2.0)  # Set timeout for blocking operations

    def send_data(self, data):
        try:
            # Send data to the ESP32
            self.sock.sendto(data.encode(), (self.esp32_ip, self.esp32_port))
            
            # Receive response from the ESP32
            response, _ = self.sock.recvfrom(1024)
            return response.decode()
        except socket.timeout:
            print("Error: Request timed out.")
            return None
        except Exception as e:
            print(f"Error: Failed to send data to ESP32 server: {e}")
            return None

# Example usage
def main():
    # Replace 'esp32_ip' with the actual IP address of your ESP32
    esp32_ip = "192.168.137.111"

    # Initialize the RobotUDPClient
    esp32_client = RobotUDPClient(esp32_ip)

    # Dummy data to send
    data_to_send = "Hello Robot"

    # Send data to the ESP32
    response = esp32_client.send_data(data_to_send)

    if response:
        print("Response from ESP32:", response)
    else:
        print("Failed to receive response from ESP32. Exiting...")

if __name__ == "__main__":
    main()
