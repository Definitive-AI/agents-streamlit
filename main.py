from pathlib import Path

import streamlit as st
from st_pages import Page, show_pages, add_page_title, Section

add_page_title() 

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

st.markdown("---")

with st.expander("Sign up here"):
    st.markdown("""
    
    <a href="https://definitive-ai.com/"><img src="https://user-images.githubusercontent.com/875246/185755203-17945fd1-6b64-46f2-8377-1011dcb1a444.png" height="50" /></a>

""", unsafe_allow_html=True)

st.markdown("""
### 📓 Guide

To get the most out of this course, you should feel comfortable with coding and command line
and know the basics of SQL. Prior experience with Python will be helpful, but you can pick
Python relatively fast if you have experience with other programming languages.

Prior experience with data engineering is not required.


### ❔ Asking for help in Discord

The best way to get support is to use [DataTalks.Club's Slack](https://datatalks.club/slack.html). Join the [`#course-data-engineering`](https://app.slack.com/client/T01ATQK62F8/C01FABYF2RG) channel.

To make discussions in Slack more organized:

* Follow [these recommendations](asking-questions.md) when asking for help
* Read the [DataTalks.Club community guidelines](https://datatalks.club/slack/guidelines.html)

""", unsafe_allow_html=True)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
