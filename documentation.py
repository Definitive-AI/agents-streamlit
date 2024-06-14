import streamlit as st
import requests
import time

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
    text = st.markdown('Generator SessionID:\n' + session_id)

st.title("Agent Generator - Process Documentation")
st.subheader('Upload process documentation to generate Agents')


url = ""
headers = {"Authorization": f"{defai_api_key}"}

# Upload file
uploaded_file = st.file_uploader("Select Process Documentation to upload")

if uploaded_file is not None:
    # Make API call to upload the file
    data = {'defai_api_key': defai_api_key, "session_id": session_id}  
    files = {"file": uploaded_file}
    response = requests.post(url=url + "/api/upload", headers=headers, data=data, files=files)
    file_id = response.json()["file_id"]
    st.success(f"File uploaded successfully. File ID: {file_id}")

    # Check file status every 10 seconds
    status = "processing"
    while status != "complete":
        time.sleep(10)
        status_response = requests.get(url=url + f"/api/status/{file_id}", headers=headers)
        status = status_response.json()["status"]
        st.info(f"File status: {status}")

    # Enable download button when status is complete
    if status == "complete":
        st.success("File processing completed.")
        download_url = url + f"/api/download/{file_id}"
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