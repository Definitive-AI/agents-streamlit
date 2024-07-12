import os
import sys
import json
from io import BytesIO
import streamlit as st
import requests
import asyncio
from typing import Dict
import time
from st_pages import add_indentation
from threading import Thread
from streamlit.runtime import get_instance
from streamlit.runtime.scriptrunner import get_script_run_ctx

st.set_page_config(layout="centered")

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

    runtime = get_instance()
    session_id = get_script_run_ctx().session_id
    session_info = runtime._session_mgr.get_session_info(session_id)
    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")
    return session_info.session.id

session_id = _get_session()

url = st.secrets["DEFAI_URL"]

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0    

with st.sidebar:
    anth_api_key = st.text_input("Anthropic API Key", key="anth_api_key", type="password")
    defai_api_key = st.text_input("Definitive API Key", key="defai_api_key", type="password")
    text = st.markdown('Generator SessionID:\n')
    text = st.markdown(session_id)

    uploaded_file = st.file_uploader("Choose a screenshot to upload", key=f"uploader_{st.session_state.uploader_key}")

    progress = st.button(label=":blue[Download Current Progress]",type="secondary")
    if progress and defai_api_key != "":
        headers = {"Authorization": f"{defai_api_key}"}
        download_url = f"/api/download/{session_id}"
        download_response = requests.get(url + download_url, headers=headers)        
        try:
            if download_response.headers['Content-Type'] == 'application/zip':
                st.download_button(
                    label="Download Processed File",
                    data=BytesIO(download_response.content),
                    file_name=session_id+"_agents.zip",
                    mime="application/octet-stream",
                )
            elif download_response.headers['Content-Type'] == 'application/json':
                st.error(download_response.json())                         
            else:
                st.error(f"Unexpected MIME type: {download_response.headers['Content-Type']}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error retrieving file: {str(e)}")
        except KeyError:
            st.error("Invalid response format. 'file_id' not found in the response.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


st.markdown("<h1 style='text-align: center; color: #212750;'>Agent Generator</h1>", unsafe_allow_html=True)
st.header('Brainstorming Interview')
st.subheader('Brainstorming with Eva to generate Agents')

headers = {"Authorization": f"{defai_api_key}", "session_id": session_id, "anth_api_key": anth_api_key}


# def ping():
#     check = True
#     status = ""
#     while check:
#         time.sleep(10)
#         chat_response = requests.post(url=url + "/api/ping", headers=headers, json={"session_id": session_id, })
#         status = chat_response.json()["status"]
        
#         if status != "":
#             st.info("Progress: " + status, icon="ℹ️")
#             if status == "Complete":
#                 check = False
        
#     st.success("File processing completed.")
#     download_url = url + f"/api/download/{session_id}"
#     st.download_button(
#         label="Download Processed File",
#         data=requests.get(url=download_url,headers=headers).content,
#         file_name= session_id + "_agents.zip",
#         mime="application/octet-stream",
#     )


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if len(st.session_state.messages) == 0 and anth_api_key != "" and defai_api_key != "" :
    chat_response = requests.post(url=url + "/api/start_brainstorming", headers=headers, json={"prompt": "start the conversation with the user", "session_id": session_id, "anth_api_key": anth_api_key})
    assistant_response = chat_response.json()["response"]     
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})   
    
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

    # t = Thread(target=ping, args=())
    # t.start()

async def get_response(prompt,uploaded_file):  
    headers1 = {"Authorization": f"{defai_api_key}", "sessionid": session_id, "anthapikey": anth_api_key}   
    if uploaded_file is None:
        chat_response = requests.post(url=url + "/api/brainstorming", headers=headers, json={"prompt": prompt,})
        assistant_response = chat_response.json()["response"]
    else:
        files = {"file": uploaded_file}
        st.info("Screenshot upload")
        chat_response = requests.post(url=url + "/api/screenshot", headers=headers1, data={"prompt": prompt}, files=files)
        assistant_response = chat_response.json()["response"]

    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)   

    st.session_state.uploader_key += 1
    st.experimental_rerun()         

if prompt := st.chat_input("Enter your message"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Make API call to get assistant response
    async def main():
        await get_response(prompt,uploaded_file)

    asyncio.run(main())

progress = st.button(label=":blue[Submit Process for Generation]",type="primary")
if progress and defai_api_key != "":
    headers1 = {"Authorization": f"{defai_api_key}", "sessionid": session_id, "anthapikey": anth_api_key}   
    brainstorm_url = f"/api/pdd_brainstorm"
    brainstorm_response = requests.post(brainstorm_url, headers=headers1)      
    st.info(brainstorm_response.content)  
