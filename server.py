import asyncio
 
import websockets

import sqlite3
from sqlite3 import Error
 
# create handler for each connection
 
async def assign_task(websocket, path):
 
    data = await websocket.recv()

    sql = "SELECT `url` FROM `links` WHERE `status`='0' ORDER BY RANDOM() LIMIT 1;"
    
    c = conn.cursor()
    c.execute(sql)

    url = c.fetchone()

    if url:
        await websocket.send(url)

async def complete_task(websocket, path):
 
    data = await websocket.recv()

    sql = "UPDATE `links` SET `status`='1' WHERE `url`='"+data+"' LIMIT 1;"
    print(sql)
    
    c = conn.cursor()
    c.execute(sql)
    
    conn.commit()
    
    reply = f"TASK:  {data}!"

    print(reply)
 
    await websocket.send(reply)
 
 
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)
    
    return False


conn = create_connection(r"./db/sqlite.db")

if conn:
 
    start_server = websockets.serve(assign_task, "localhost", 8000)

    task_server = websockets.serve(complete_task, "localhost", 8080)

    # start_server = websockets.serve(handler, "localhost", 8000)
    
    
    
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_until_complete(task_server)
    
    asyncio.get_event_loop().run_forever()