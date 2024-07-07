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


st.markdown("<h1 style='text-align: center; color: #212750;'>Agent Generator</h1>", unsafe_allow_html=True)
st.header("Form")
st.subheader('Fill in form to generate Agents')

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

url = st.secrets["DEFAI_URL"]

with st.sidebar:
    anth_api_key = st.text_input("Anthropic API Key", key="anth_api_key", type="password")
    if 'defai_api_key' not in st.session_state:
        defai_api_key = st.text_input("Definitive API Key", key="defai_api_key", type="password")
        st.session_state['defai_api_key'] = defai_api_key
    else:
        defai_api_key = st.text_input("Definitive API Key",  value=st.session_state['defai_api_key'], key="defai_api_key", type="password")
        
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

placeholder = st.empty()
process_description = st.text_area("Briefly describe the process")
process_trigger = st.text_area("Identify what starts or triggers this process")
process_goal = st.text_area("Identify the process's end result or goal")
process_steps = st.text_area("Outline the main steps in this process")
step_information = st.text_area("Determine the information or materials needed for each step")
process_tools = st.text_area("List the systems or tools used in this process")
process_roles = st.text_area("Describe who is involved in this process and their roles")
process_challenges = st.text_area("Identify any particularly challenging parts of the process")
process_improvements = st.text_area("Discuss ideas on how this process could be improved")
additional_aspects = st.text_area("Cover any important aspects of the process not yet mentioned")

# Button to combine the answers
if st.button("Generate Agents for Process") and defai_api_key != "" and anth_api_key != "":
    combined_answer = f"Process Description:\n{process_description}\n\n" \
                      f"Process Trigger:\n{process_trigger}\n\n" \
                      f"Process Goal:\n{process_goal}\n\n" \
                      f"Process Steps:\n{process_steps}\n\n" \
                      f"Step Information:\n{step_information}\n\n" \
                      f"Process Tools:\n{process_tools}\n\n" \
                      f"Process Roles:\n{process_roles}\n\n" \
                      f"Process Challenges:\n{process_challenges}\n\n" \
                      f"Process Improvements:\n{process_improvements}\n\n" \
                      f"Additional Aspects:\n{additional_aspects}"


    headers = {"Authorization": f"{defai_api_key}", "sessionid": session_id, "anthapikey": anth_api_key}   

    chat_response = requests.post(url=url + "/api/upload_form", headers=headers, json={"prompt": combined_answer})
    assistant_response = chat_response.json()["response"]

    st.success(f"File uploaded successfully: " + assistant_response)

    if assistant_response == "Processing" or assistant_response == "Already Processing":
        # Check file status every 10 seconds
        status = "processing"
        i = 0
        while status != "Complete" or i < 60:
            time.sleep(60)
            placeholder.empty()
            status_response = requests.get(url=url + f"/api/status/{session_id}", headers=headers)
            status = status_response.json()["status"]
            placeholder.info(f"File status: {status}")
            i += 1
            

