import streamlit as st
import requests
import time
import os
from io import BytesIO
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

def download():
    headers = {"Authorization": f"{defai_api_key}"}
    try:
        download_url = f"/api/download/{session_id}"
        download_response = requests.get(url + download_url, headers=headers)
        download_response.raise_for_status()

        if download_response.headers['Content-Type'] == 'application/zip':
            st.download_button(
                label="Download Processed File",
                data=BytesIO(download_response.content),
                file_name=session_id+"_agents.zip",
                mime="application/octet-stream"            )
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


st.markdown("""
            <style>
                div[data-testid="column"] {
                    width: fit-content !important;
                    flex: unset;
                }
                div[data-testid="column"] * {
                    width: fit-content !important;
                }
            </style>
            """, unsafe_allow_html=True)

if defai_api_key != "":
    headers = {"Authorization": f"{defai_api_key}"}
    download_url = f"/api/sessions"
    download_response = requests.get(url + download_url, headers=headers)
    data = download_response.json()
    if "status" not in data:
        fields = ["Session ID", "Agents Name", "Creation Status", "Input Tokens", "Output Tokens", "Time"]
        
        transformed_data = [dict(zip(fields, row)) for row in data]
        df = pd.DataFrame(data,columns=fields)
        #st.dataframe(df, use_container_width=True)
        df['Time'] = pd.to_datetime(df['Time'], unit='s')

        with st.container():
            #cols = st.columns([1,1,1,1,1,1,1,1,1])
            col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1,1,1,1,1,1,1,1,1])
            # for col, field_name in zip(cols, ([""] + fields)):
            #     col.write(field_name)
            col1.write("") 
            col2.write("Session ID") 
            col3.write("Agents Name") 
            col4.write("Creation Status") 
            col5.write("Input Tokens") 
            col6.write("Output Tokens") 
            col7.write("Start Time") 

            for x, email in enumerate(df):
                
                col1.write(x)  # index
                col2.write(df['Session ID'][x])  # email
                col3.write(df['Agents Name'][x])  # unique ID
                col4.write(df['Creation Status'][x])   # email status
                col5.write(df['Input Tokens'][x])  # email
                col6.write(df['Output Tokens'][x])  # unique ID
                col7.write(df['Time'][x])   # email status

                button_phold = col8.empty()  # create a placeholder
                do_action = button_phold.button("Delete", key=x)
                button_down = col9.empty()  # create a placeholder
                down = button_down.button("Download Agents", key=x)
                if do_action:
                    pass # do some action with row's data
                    button_phold.empty()  #  remove button
        #
           
    # session_id = st.text_input("Enter Session ID to Delete Agents")

    # if session_id:
    #     #headers = {"Authorization": f"Bearer {defai_api_key}"}
    #     headers = {"Authorization": f"{defai_api_key}"}
    #     try:
    #         download_url = f"/api/delete/{session_id}"
    #         download_response = requests.get(url + download_url, headers=headers)
    #         download_response.raise_for_status()
    #         response = download_response.json()["response"]
    #         if response == "Complete":
    #             st.info("Agents Deleted")
    #     except requests.exceptions.RequestException as e:
    #         st.error(f"Error retrieving file: {str(e)}")
    #     except KeyError:
    #         st.error("Invalid response format. 'file_id' not found in the response.")
    #     except Exception as e:
    #         st.error(f"An error occurred: {str(e)}")
    # else:
    #     st.info("Please enter a Session ID to delete the agents.")