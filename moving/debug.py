import asyncio
import websockets

async def send_message(uri):
    async with websockets.connect(uri) as websocket:
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

            # Send the message to the ESP32
            print(f"Sending: {message}")
            await websocket.send(message)

            # Receive the response from the ESP32
            response = await websocket.recv()
            print(f"Received: {response}")

def main():
    # Prompt the user for the ESP32 IP address
    esp32_ip = input("Enter the IP address of your ESP32: ")
    websocket_uri = f"ws://{esp32_ip}/ws"

    # Run the send_message function
    asyncio.get_event_loop().run_until_complete(send_message(websocket_uri))

if __name__ == "__main__":
    main()
