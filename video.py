import os
import sys
import json
import streamlit as st
import requests
import asyncio
from typing import Dict
import time
from st_pages import add_indentation
from threading import Thread
from streamlit.runtime import get_instance
from streamlit.runtime.scriptrunner import get_script_run_ctx

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

st.markdown("<h1 style='text-align: center; color: #212750;'>Agent Generator</h1>", unsafe_allow_html=True)
st.header('Video Interview')
st.subheader('Start a call with Eva to generate Agents')

headers = {"Authorization": f"{defai_api_key}", "session_id": session_id, "anth_api_key": anth_api_key}

st.markdown("---")

st.markdown("""<p align="center" style="font-size: 23px;" markdown="1"><b>Coming Soon</b></p>""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2,3])
with col2:
    st.button(":gray-background[Join Meet]", type="primary")