import asyncio
import websockets
import os

async def status(websocket, path):
    while True:
        # Read the status from the file
        try:
            with open(os.path.join(os.path.dirname(__file__), '..', 'expression.txt'), 'r') as file:
                status = file.read().strip()
        except FileNotFoundError:
            status = "File not found"

        await websocket.send(status)
        await asyncio.sleep(1)  # Send status every second

start_server = websockets.serve(status, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
