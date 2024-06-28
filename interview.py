import os
import sys
import streamlit as st
import requests
import asyncio
from typing import Dict
import time
from st_pages import add_indentation
from threading import Thread

st.html("""
<style>
[data-testid=stSidebar] {
        background-color: #212750;
    }
[data-testid="stSidebarContent"] {
    color: white;
    span {
        color: white;
    }
    p {
        color: white;
    }
}
</style>
""")

add_indentation()

def _get_session():
    from streamlit.runtime import get_instance
    from streamlit.runtime.scriptrunner import get_script_run_ctx
    runtime = get_instance()
    session_id = get_script_run_ctx().session_id
    session_info = runtime._session_mgr.get_session_info(session_id)
    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")
    return session_info.session.id

session_id = _get_session()

with st.sidebar:
    anth_api_key = st.text_input("Anthropic API Key", key="anth_api_key", type="password")
    defai_api_key = st.text_input("Definitive API Key", key="defai_api_key", type="password")
    text = st.markdown('Generator SessionID:\n')
    text = st.markdown(session_id)

st.markdown("<h1 style='text-align: center; color: #212750;'>Agent Generator</h1>", unsafe_allow_html=True)
st.header('Interview')
st.subheader('Chat with Eva to generate Agents')

# st.markdown("""## Interview
# ### Chat with Eva to generate Agents
# """)

url = st.secrets["DEFAI_URL"]

headers = {"Authorization": f"{defai_api_key}"}

# Upload file
uploaded_file = st.file_uploader("Choose a screenshot to upload")

def ping():
    check = True
    status = ""
    while check:
        time.sleep(10)
        chat_response = requests.post(url=url + "/api/ping", headers=headers, json={"session_id": session_id, })
        status = chat_response.json()["status"]
        
        if status != "":
            st.info("Progress: " + status, icon="ℹ️")
            if status == "Complete":
                check = False
        
    st.success("File processing completed.")
    download_url = url + f"/api/download/{session_id}"
    st.download_button(
        label="Download Processed File",
        data=requests.get(url=download_url,headers=headers).content,
        file_name=f"processed_{uploaded_file.name}",
        mime="application/octet-stream",
    )

if uploaded_file is not None:
    # Make API call to upload the file

    data = {'defai_api_key': defai_api_key, "session_id": session_id}    
    files = {"file": uploaded_file}
    #"sessionid": session_id
    response = requests.post(url=url + "/api/upload", headers=headers, data=data, files=files)
    st.success(f"Screenshot uploaded successfully")

# Chat system
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

temp = True 
if anth_api_key != "" and defai_api_key != "" and temp:
    chat_response = requests.post(url=url + "/api/chat", headers=headers, json={"prompt": "start the conversation with the user", "session_id": session_id, "anth_api_key": anth_api_key})
    assistant_response = chat_response.json()["response"]     
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})   
    temp = False
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
    t = Thread(target=ping, args=())
    t.start()

async def get_response(prompt):     
    chat_response = requests.post(url=url + "/api/chat", headers=headers, json={"prompt": prompt, "session_id": session_id, "anth_api_key": anth_api_key})
    assistant_response = chat_response.json()["response"]

    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)    

if prompt := st.chat_input("Enter your message"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Make API call to get assistant response

    # async def main():
    #     await get_response(prompt)

    # asyncio.run(main())