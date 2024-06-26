import streamlit as st
import requests
import time
import os
from st_pages import add_indentation

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
st.subheader('Enter saved SessionId to access generated Agents')

url = st.secrets["DEFAI_URL"]

session_id = st.text_input("Enter Session ID")

if session_id:
    if not defai_api_key:
        st.warning("Please enter your Definitive API Key in the sidebar.")
    else:
        #headers = {"Authorization": f"Bearer {defai_api_key}"}
        headers = {"Authorization": f"{defai_api_key}"}
        try:
            response = requests.get(f"{url}/api/file/{session_id}", headers=headers)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            file_data = response.json()
            file_id = file_data["file_id"]

            download_url = f"/api/download/{file_id}"
            download_response = requests.get(url + download_url, headers=headers)
            download_response.raise_for_status()

            st.download_button(
                label="Download Processed File",
                data=download_response.content,
                file_name=f"processed_file_{file_id}.zip",
                mime="application/octet-stream",
            )
        except requests.exceptions.RequestException as e:
            st.error(f"Error retrieving file: {str(e)}")
        except KeyError:
            st.error("Invalid response format. 'file_id' not found in the response.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
else:
    st.info("Please enter a Session ID to retrieve the file.")