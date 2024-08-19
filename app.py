# import streamlit as st
# import os
# import subprocess
# from streamlit_option_menu import option_menu


# # Set page config
# st.set_page_config(page_title="Devika AI", layout="wide")

# # Custom CSS
# st.markdown("""
# <style>
#     .stApp {
#         background-color: #f0f2f6;
#     }
#     .stSelectbox {
#         padding-top: 0px;
#     }
#     .stSelectbox > div > div > div {
#         background-color: white;
#     }
#     .status-indicator {
#         height: 10px;
#         width: 10px;
#         background-color: #1eb25c;
#         border-radius: 50%;
#         display: inline-block;
#         margin-right: 5px;
#     }
#     .panel {
#         background-color: white;
#         border-radius: 10px;
#         padding: 10px;
#         margin-bottom: 10px;
#         box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
#     }
#     .main-content {
#         margin-bottom: 60px;
#     }
#     .terminal-output {
#         background-color: black;
#         color: white;
#         font-family: monospace;
#         padding: 10px;
#         border-radius: 5px;
#         height: 200px;
#         overflow-y: auto;
#     }
#     .code-viewer {
#         background-color: #f8f8f8;
#         font-family: monospace;
#         padding: 10px;
#         border-radius: 5px;
#         height: 200px;
#         overflow-y: auto;
#     }
# </style>
# """, unsafe_allow_html=True)

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Sidebar
# with st.sidebar:
#     selected = option_menu(
#         menu_title=None,
#         options=["Home", "Settings", "History"],
#         icons=["house", "gear", "clock-history"],
#         menu_icon="cast",
#         default_index=0,
#         styles={
#             "container": {"padding": "0!important", "background-color": "#fafafa"},
#             "icon": {"color": "black", "font-size": "25px"}, 
#             "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
#             "nav-link-selected": {"background-color": "#ff4b4b"},
#         }
#     )
    
#     st.selectbox("Select Project", ["Project 1", "Project 2", "Project 3"])
#     st.markdown('<span class="status-indicator"></span> Internet', unsafe_allow_html=True)
#     st.write("Token Usage: 0")
#     st.selectbox("Select Search Engine", ["Engine 1", "Engine 2"])
#     st.selectbox("Select Model", ["Model 1", "Model 2"])

# # Main content
# st.markdown('<div class="main-content">', unsafe_allow_html=True)
# col1, col2 = st.columns([2, 2])

# with col1:
#     with st.container():
#         st.markdown('<div class="panel">', unsafe_allow_html=True)
#         st.markdown('<h3>devika/liteweb</h3>', unsafe_allow_html=True)
#         st.markdown('<p>💡 TIP: You can include a Git URL in your prompt to clone a repo!</p>', unsafe_allow_html=True)
        
#         # Chat interface
#         if "messages" not in st.session_state:
#             st.session_state.messages = []

#         for message in st.session_state.messages:
#             with st.chat_message(message["role"]):
#                 st.markdown(message["content"])

#         prompt = st.chat_input("Enter your message:", key="chat_input")
#         if st.button("Send", key="send_button"):
#             if prompt:
#                 st.session_state.messages.append({"role": "user", "content": prompt})
#                 with st.chat_message("user"):
#                     st.markdown(prompt)
#         st.markdown('</div>', unsafe_allow_html=True)            

# with col2:
#     # Code viewer
#     with st.container():
#         st.markdown('<div class="panel">', unsafe_allow_html=True)
#         st.markdown('<h3>Code Viewer</h3>', unsafe_allow_html=True)
#         uploaded_file = st.file_uploader("Choose a file", type=['py', 'txt', 'json', 'yaml', 'yml'])
#         if uploaded_file is not None:
#             content = uploaded_file.getvalue().decode("utf-8")
#             st.code(content, language='python')
#         else:
#             st.write("No file selected.")
#         st.markdown('</div>', unsafe_allow_html=True)

#     # Terminal
#     with st.container():
#         st.markdown('<div class="panel">', unsafe_allow_html=True)
#         st.markdown('<h3>Terminal</h3>', unsafe_allow_html=True)
#         if 'terminal_output' not in st.session_state:
#             st.session_state.terminal_output = []

#         for output in st.session_state.terminal_output:
#             st.text(output)

#         command = st.text_input("Enter command:")
#         if st.button("Run", key="run_command"):
#             if command:
#                 try:
#                     result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
#                     st.session_state.terminal_output.append(f"$ {command}")
#                     st.session_state.terminal_output.append(result.stdout)
#                 except subprocess.CalledProcessError as e:
#                     st.session_state.terminal_output.append(f"$ {command}")
#                     st.session_state.terminal_output.append(f"Error: {e.stderr}")
#         st.markdown('</div>', unsafe_allow_html=True)

# st.markdown('</div>', unsafe_allow_html=True)

# # Hide Streamlit's default footer
# hide_streamlit_style = """
# <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# </style>
# """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

import streamlit as st
from streamlit_option_menu import option_menu
import subprocess

# Set page config
st.set_page_config(page_title="Devika AI", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #f0f2f6;
    }
    .stSelectbox {
        padding-top: 0px;
    }
    .stSelectbox > div > div > div {
        background-color: white;
    }
    .status-indicator {
        height: 10px;
        width: 10px;
        background-color: #1eb25c;
        border-radius: 50%;
        display: inline-block;
        margin-right: 5px;
    }
    .panel {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
    }
    .main-content {
        margin-bottom: 60px;
    }
    .terminal-output, .code-viewer {
        background-color: #f8f8f8;
        font-family: monospace;
        padding: 10px;
        border-radius: 5px;
        height: 200px;
        overflow-y: auto;
    }
    .sidebar .nav-link {
        font-size: 0.8rem !important;
    }
    .sidebar .nav-link-selected {
        font-size: 0.8rem !important;
    }
    .stButton > button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Home", "Settings", "History"],
        icons=["house", "gear", "clock-history"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "black", "font-size": "16px"}, 
            "nav-link": {"font-size": "12px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#ff4b4b"},
        }
    )

# Top bar
col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
with col1:
    st.selectbox("Select Project", ["Project 1", "Project 2", "Project 3"])
with col2:
    st.markdown('<span class="status-indicator"></span> Internet', unsafe_allow_html=True)
with col3:
    st.write("Token Usage: 0")
with col4:
    st.selectbox("Select Search Engine", ["Engine 1", "Engine 2"])
with col5:
    st.selectbox("Select Model", ["Model 1", "Model 2"])

# Main content
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<h3>devika/liteweb</h3>', unsafe_allow_html=True)
    st.markdown('<p>💡 TIP: You can include a Git URL in your prompt to clone a repo!</p>', unsafe_allow_html=True)
    
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.text_input("Enter your message:", key="chat_input")
    if st.button("Send", key="send_button"):
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Code viewer
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<h3>Code Viewer</h3>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a file", type=['py', 'txt', 'json', 'yaml', 'yml'])
    if uploaded_file is not None:
        content = uploaded_file.getvalue().decode("utf-8")
        st.markdown('<div class="code-viewer">', unsafe_allow_html=True)
        st.code(content, language='python')
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.write("No file selected.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Terminal
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<h3>Terminal</h3>', unsafe_allow_html=True)
    if 'terminal_output' not in st.session_state:
        st.session_state.terminal_output = []

    st.markdown('<div class="terminal-output">', unsafe_allow_html=True)
    for output in st.session_state.terminal_output:
        st.text(output)
    st.markdown('</div>', unsafe_allow_html=True)

    command = st.text_input("Enter command:")
    if st.button("Run", key="run_command"):
        if command:
            try:
                result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
                st.session_state.terminal_output.append(f"$ {command}")
                st.session_state.terminal_output.append(result.stdout)
            except subprocess.CalledProcessError as e:
                st.session_state.terminal_output.append(f"$ {command}")
                st.session_state.terminal_output.append(f"Error: {e.stderr}")
    st.markdown('</div>', unsafe_allow_html=True)

# Hide Streamlit's default footer
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)