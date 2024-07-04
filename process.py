import streamlit as st
import requests
import time
from io import BytesIO
import os
from st_pages import add_indentation

add_indentation()

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
# st.title("Agent Generator")
st.header('Process Documentation')
st.subheader('Upload process documentation to generate Agents')


url = st.secrets["DEFAI_URL"]
headers = {"Authorization": f"{defai_api_key}"}

# Upload file
uploaded_file = st.file_uploader("Select Process Documentation to upload")

placeholder = st.empty()

if uploaded_file is not None:

    headers1 = {"Authorization": f"{defai_api_key}", "sessionid": session_id, "anthapikey": anth_api_key}   
    if uploaded_file is not None:
        files = {"file": uploaded_file}
        data = {'upload_file': uploaded_file.name}
        chat_response = requests.post(url=url + "/api/upload", headers=headers1, data=data, files=files)
        assistant_response = chat_response.json()["response"]

        st.success(f"File uploaded successfully: " + assistant_response)

        if assistant_response == "Processing":
            # Check file status every 10 seconds
            status = "processing"
            while status != "complete":
                time.sleep(30)
                placeholder.empty()
                status_response = requests.get(url=url + f"/api/status/{session_id}", headers=headers)
                status = status_response.json()["status"]
                placeholder.info(f"File status: {status}")
                

            # Enable download button when status is complete
            if status == "complete":
                st.success("File processing completed.")
                download_url = url + f"/api/download/{session_id}"
                st.download_button(
                    label="Download Processed File",
                    data=requests.get(url=download_url,headers=headers).content,
                    file_name=f"processed_{uploaded_file.name}",
                    mime="application/octet-stream",
                )
        


# Chat system
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Enter your message"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Make API call to get assistant response
    chat_response = requests.post(url + "/api/chat", headers=headers, json={"prompt": prompt, "session_id": session_id, "anth_api_key": anth_api_key, "defai_api_key": defai_api_key})
    assistant_response = chat_response.json()["response"]

    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)