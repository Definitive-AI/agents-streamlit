from pathlib import Path

import streamlit as st
from st_pages import Page, show_pages, add_page_title, Section

#add_page_title() 

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
}
</style>
""")

show_pages(
    [
        Page("main.py", "Definitive AI"),
        Section("Generators", "🧙‍♂️"),
        Page("documentation.py", "Process Documentation"),
        Page("interview.py", "Interview"),
        Section("Storage", "💾"),
        Page("file.py", "Download"),
    ]
)

st.markdown("""<img src="https://raw.githubusercontent.com/Definitive-AI-Testing/agents-streamlit/master/.streamlit/Logo.png" height="200" />""", unsafe_allow_html=True) 


st.markdown("---")

with st.expander("Sign up here"):
    st.markdown("""
    
    <a href="https://definitive-ai.com/"><img src="https://raw.githubusercontent.com/Definitive-AI-Testing/agents-streamlit/master/.streamlit/sign-up.jpg" height="50" /></a>

""", unsafe_allow_html=True)

st.markdown("""
### 📓 Guide

To get a Definitive AI API Key, just sign up above.            

[Anthropic API Key Guide](https://docs.anthropic.com/en/docs/getting-access-to-claude)


### ❔ Asking for help in Discord

The best way to get support is to use [Definitive AI Discord](https://datatalks.club/slack.html). Join the [`#Definitive AI`](https://app.slack.com/client/T01ATQK62F8/C01FABYF2RG) channel.

To make discussions in Discord more organized:

* Follow [these recommendations](asking-questions.md) when asking for help
* Read the [Definitive AI community guidelines](https://datatalks.club/slack/guidelines.html)

""", unsafe_allow_html=True)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
