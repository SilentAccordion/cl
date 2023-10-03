import asyncio
import websockets

import requests               # To get the pages
from bs4 import BeautifulSoup # and to process them

from time import sleep      # Allowing us to pause between pulls
from random import random   # And allowing that pause to be random

# import textwrap             # Useful for our wrapped output

import os
import os.path



import time

def generate_filename_from_url(url) :
    
    # Put code here from scraping exercise
    # return("")
    
    # initial attempt to just grab actual file name from link
    # return(url.split('/')[-1]+'.txt')
    
    if not url :
        return None
    
    # drop the http or https
    name = url.replace("https","").replace("http","")

    # Replace useless chareacters with UNDERSCORE
    name = name.replace("://","").replace(".","_").replace("/","_")
    
    # remove last underscore
    last_underscore_spot = name.rfind("_")
    
    name = name[:last_underscore_spot] + name[(last_underscore_spot+1):]

    # tack on .txt
    name = "data/" + name + ".txt"
    
    return(name)


def fetch(url, output_file_name):

    # print(output_file_name)
    
    if os.path.isfile(output_file_name):
        print("skipping: "+output_file_name)
        with open(output_file_name,'r') as infile :
            return infile.read()
    # pull the page 
    r = requests.get(url)
    
    # write out the page to a file with the appropriate name
    with open(output_file_name,'w') as outfile :
        # for piece in textwrap.wrap(r.text) :
            # outfile.write(piece+'\n')
        outfile.write(r.text)

    # sleep(wait_time)
    return r.text
 
async def task():
    while True:
        async with websockets.connect('ws://localhost:8000') as websocket:
            await websocket.send("hello")
            response = await websocket.recv()
        print(response)

        url = response
        print("processing task")

        output_file_name = generate_filename_from_url(url)
        
        # Read file, from cache or remote if needed
        text = fetch(url, output_file_name)
        
        print("finished processing task")

        async with websockets.connect('ws://localhost:8080') as websocket:
            await websocket.send(url)
            response = await websocket.recv()
        print(response)
        time.sleep(10)
 
asyncio.get_event_loop().run_until_complete(task())
