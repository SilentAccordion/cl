import asyncio
import websockets
 
async def task():
    async with websockets.connect('ws://localhost:8000') as websocket:
        await websocket.send("hello")
        response = await websocket.recv()
    print(response)
    print("processing task")

    async with websockets.connect('ws://localhost:8080') as websocket:
        await websocket.send("Finished task")
        response = await websocket.recv()
    print(response)
 
asyncio.get_event_loop().run_until_complete(task())
