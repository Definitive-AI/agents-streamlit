import streamlit as st
import requests
import time
import os
import pandas as pd
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
st.subheader('Enter a API Key to view created Agents')

url = st.secrets["DEFAI_URL"]



if defai_api_key != "":
    headers = {"Authorization": f"{defai_api_key}"}
    download_url = f"/api/sessions"
    download_response = requests.get(url + download_url, headers=headers)
    data = download_response.json()
    if "status" not in data:
        columns = ["Session ID", "Agents Name", "Creation Status", "Input Tokens", "Output Tokens", "Start Time"]
        transformed_data = [dict(zip(columns, row)) for row in data]
        df = pd.DataFrame(transformed_data)
        
        # Convert the "Time" column from integer to datetime
        df['Time'] = pd.to_datetime(df['Start Time'], unit='s')
        st.dataframe(df, use_container_width=True)

    session_id = st.text_input("Enter Session ID to Delete Agents")

    if session_id:
        #headers = {"Authorization": f"Bearer {defai_api_key}"}
        headers = {"Authorization": f"{defai_api_key}"}
        try:
            download_url = f"/api/delete/{session_id}"
            download_response = requests.get(url + download_url, headers=headers)
            download_response.raise_for_status()
            response = download_response.json()["response"]
            if response == "Complete":
                st.info("Agents Deleted")
        except requests.exceptions.RequestException as e:
            st.error(f"Error retrieving file: {str(e)}")
        except KeyError:
            st.error("Invalid response format. 'file_id' not found in the response.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.info("Please enter a Session ID to delete the agents.")