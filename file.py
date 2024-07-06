import streamlit as st
import requests
import time
import os
from st_pages import add_indentation
from io import BytesIO

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

with st.sidebar:
    defai_api_key = st.text_input("Definitive API Key", key="defai_api_key", type="password")

st.markdown("<h1 style='text-align: center; color: #212750;'>Agent Generator</h1>", unsafe_allow_html=True)
st.header("Saved Agents")
st.subheader('Enter a SessionId to access generated Agents')

url = st.secrets["DEFAI_URL"]

session_id = st.text_input("Enter Session ID")

def callback_button() -> None:
    global session_id
    session_id = None

if session_id:
    if not defai_api_key:
        st.warning("Please enter your Definitive API Key in the sidebar.")
    else:
        #headers = {"Authorization": f"Bearer {defai_api_key}"}
        ()
else:
    st.info("Please enter a Session ID to retrieve the file.")