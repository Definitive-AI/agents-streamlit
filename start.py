import socketio
import asyncio
import os
import git
from git import Repo
import streamlit as st
import subprocess
from client import *

from dotenv import load_dotenv
load_dotenv()

try:
    current_directory = os.getcwd()
    new_repo_name = 'agents'
    new_repo_path = os.path.join(os.path.dirname(current_directory), new_repo_name)
    os.makedirs(new_repo_path, exist_ok=True)
    Repo.init(new_repo_path)
except Exception as exn:
    print(exn)

Def_API_KEY = os.environ['Def_API_KEY']
ANTHROPIC_API_KEY = os.environ['ANTHROPIC_API_KEY']
SERVER = os.environ['Def_Server'] # 'http://localhost:5000'

# st.secrets["Def_API_KEY"] == Def_API_KEY
# st.secrets["ANTHROPIC_API_KEY"] == ANTHROPIC_API_KEY
# st.secrets["Def_Server"] == server

if __name__ == '__main__':
    from streamlit.web.bootstrap import run

    real_script = 'aider_gui.py'
    #real_script = 'nav.py'
    run(real_script, False, [Def_API_KEY,ANTHROPIC_API_KEY,SERVER], {})    
