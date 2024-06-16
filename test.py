import requests
import time
import os
import streamlit as st

url = st.secrets["DEFAI_URL"]
download_url = url + f"/api/ping"
download_response = requests.get(download_url)
print(download_response.json())