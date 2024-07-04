import requests
import time
import os
import streamlit as st

url = st.secrets["DEFAI_URL"]
download_url = url + f"/api/ping"
download_response = requests.get(download_url)
print(download_response.json())


    # if len(st.session_state.messages) != 0 and anth_api_key != "" and defai_api_key != "" :
    #     if uploaded_file is not None:
    #         # Make API call to upload the file
    #         st.session_state.messages.append({"role": "user", "content": "Uploaded screenshot"})
    #         with st.chat_message("user"):
    #             st.markdown("Uploaded screenshot")

    #         data = {"session_id": session_id}    
    #         #data=data, 
    #         files = {"file": uploaded_file}
    #         #"sessionid": session_id
    #         headers = {"Authorization": f"{defai_api_key}", "sessionid": session_id}
    #         chat_response = requests.post(url=url + "/api/screenshot", headers=headers, files=files)
    #         # st.success(f"Screenshot uploaded successfully")    
    #         uploaded_file = None
    #         try:
    #             assistant_response = chat_response.json()["response"]     
    #             #assistant_response = str(chat_response.json())
    #             st.session_state.messages.append({"role": "assistant", "content": assistant_response})               
    #             # with st.chat_message("assistant"):
    #             #     st.markdown(assistant_response)
    #         except Exception as exn:
    #             print(exn)