import asyncio
 
import websockets
 
# create handler for each connection
 
async def assign_task(websocket, path):
 
    data = await websocket.recv()

    url = "https://boston.craigslist.org/nwb/ctd/d/salem-2011-honda-civic-coupe-automatic/7672601386.html"

    reply = f"{url}!"

    await websocket.send(reply)

async def complete_task(websocket, path):
 
    data = await websocket.recv()
 
    reply = f"TASK:  {data}!"

    print(reply)
 
    await websocket.send(reply)
 
 
 
start_server = websockets.serve(assign_task, "localhost", 8000)

task_server = websockets.serve(complete_task, "localhost", 8080)

# start_server = websockets.serve(handler, "localhost", 8000)
 
 
 
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_until_complete(task_server)
 
asyncio.get_event_loop().run_forever()