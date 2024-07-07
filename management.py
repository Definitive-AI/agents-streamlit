import streamlit as st
import requests
import time
import os
from io import BytesIO
import pandas as pd
from st_pages import add_indentation
import tokencost
from tokencost import calculate_cost_by_tokens

st.set_page_config(layout="wide")

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

st.markdown("<h1 style='text-align: center; color: #212750;'>Agent Management</h1>", unsafe_allow_html=True)
st.header("")
st.subheader('Enter an API Key to view generated Agents')

url = st.secrets["DEFAI_URL"]

st.markdown("---")

def delete(session_id):
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

def stop(session_id):
    #headers = {"Authorization": f"Bearer {defai_api_key}"}
    headers = {"Authorization": f"{defai_api_key}"}
    try:
        download_url = f"/api/stop/{session_id}"
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

def download(session_id):
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

def calculate(in1,out1):
    t1 = calculate_cost_by_tokens(in1,"claude-3-5-sonnet-20240620","input")
    t2 = calculate_cost_by_tokens(out1,"claude-3-5-sonnet-20240620","output")
    t3 = round(t1+t2, 2)
    return str(t3)

if defai_api_key != "":
    headers = {"Authorization": f"{defai_api_key}"}
    download_url = f"/api/sessions"
    download_response = requests.get(url + download_url, headers=headers)
    data = download_response.json()
    if "status" not in data:
        fields = ["Session ID", "Agents Name", "Generation Status", "Input Tokens", "Output Tokens", "Time"]
        
        transformed_data = [dict(zip(fields, row)) for row in data]
        df = pd.DataFrame(data,columns=fields)
        #st.dataframe(df, use_container_width=True)
        df['Time'] = pd.to_datetime(df['Time'], unit='s')

        col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11 = st.columns([1,1,2,2,2,2,2,2,1,1,1])

        col1.write("ID") 
        col2.write("Session ID") 
        col3.write("Agents Name") 
        col4.write("Generation Status") 
        col5.write("Input Tokens") 
        col6.write("Output Tokens") 
        col7.write("Cost") 
        col8.write("Start Time") 
        col9.write("Download Agents") 
        col10.write("Stop Generating Agents") 
        col11.write("Delete Agents") 

        df = df.reset_index()  # make sure indexes pair with number of rows
        x = 1
        for t1, row in df.iterrows():
            try:
                cost = calculate(row['Input Tokens'],row['Output Tokens'])
                col1.write(str(x))  # index
                col2.write(row['Session ID'])  # email
                if row['Agents Name'] != "":
                    col3.write(row['Agents Name'])  # unique ID
                else:
                    col3.write("-")
                col4.write(row['Generation Status']) 
                col5.write(str(row['Input Tokens'])) 
                col6.write(str(row['Output Tokens']))
                col7.write("$" + cost)   
                col8.write(str(row['Time'])) 
                

                button_down = col9.empty()  # create a placeholder
                download1 = button_down.button("Download", key="Download" + str(x),use_container_width=True) #, on_click=download(row['Session ID']))
                button_stop = col10.empty()  # create a placeholder
                stop1 = button_stop.button("Stop", key="Generate" + str(x),use_container_width=True) #, on_click=stop(row['Session ID']))
                button_phold = col11.empty()  # create a placeholder
                delete1 = button_phold.button("Delete", key="Delete" + str(x),use_container_width=True) #, on_click=delete(row['Session ID']))     
                if delete1:
                    col4.write("Deleted")
                    delete(row['Session ID'])
                    button_phold.empty()  #  remove button
                if download1:
                    download(row['Session ID'])
                if stop1:
                    stop(row['Session ID'])
                x += 1
            except:
                ()

st.markdown("---")

reload = st.button("Refresh")
if reload:
    st.rerun()