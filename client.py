import socketio
import asyncio
import os
import git
from aider.coders import Coder
from aider.models import Model

from dotenv import load_dotenv
load_dotenv()

sio = socketio.AsyncClient() # logger=True, engineio_logger=True

Def_API_KEY = os.environ['Def_API_KEY']
ANTHROPIC_API_KEY = os.environ['ANTHROPIC_API_KEY']
server = os.environ['Def_Server'] # 'http://localhost:5000'

@sio.event
def connect():
    print("I'm connected!")

# @sio.event
# def connect_error(data):
#     print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")    

# repo = git.Repo('.', search_parent_directories=True)
# tests_file = os.path.join(git_repo_path, "test.py")
# target_files = [tests_file]
#, repo=repo.working_tree_dir

# llm_model = Model(model="claude-3-5-sonnet-20240620")
# coder:Coder = Coder.create(main_model=llm_model)

# def aider_tool(input: str):
#     if coder is not None:
#         return 
#     else:
#         return "Aider not active"    

#task = sio.start_background_task(my_background_task, 123)

# sio.send({'room': Def_API_KEY})

@sio.on(Def_API_KEY)
async def on_message(data):
    print('1')  

async def send_event(data):
    await sio.send(data)

async def start_server():
    try:
        await sio.connect(server, auth=Def_API_KEY) #{'token': 'my-token'}
        print('my sid is', sio.sid)
        await sio.emit('join', {'room': Def_API_KEY})
        await sio.wait()
    except Exception as exn:
        print(exn)


def send_data(data):
    try:
        asyncio.set_event_loop
        loop = asyncio.get_running_loop()
        task = loop.create_task(send_event(data))
    except:
        asyncio.run(send_event(data))

import threading

def run_asyncio_in_thread():
    try:
        loop = asyncio.get_running_loop()
        task = loop.create_task(start_server())
    except:
        asyncio.run(start_server())

# asyncio.to_thread()
# thread = threading.Thread(target=run_asyncio_in_thread)
# thread.start()        

# if __name__ == '__main__':
#     #asyncio.run(start_server())    
#     from streamlit.web.bootstrap import run

#     real_script = 'aider_gui.py'
#     real_script = 'main.py'
#     run(real_script, False, [], {})    
