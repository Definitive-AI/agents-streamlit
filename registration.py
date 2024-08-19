import streamlit as st
import requests

st.set_page_config(layout="centered")

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

def submit_form():
    # Get user input values
    first_name = st.session_state.first_name
    last_name = st.session_state.last_name
    email = st.session_state.email
    experience = st.session_state.langchain_experience
    use_case = st.session_state.use_case
    # Create payload for POST request
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "experience": experience,
        "use_case": use_case
    }

    url = st.secrets["DEFAI_URL"]
    register_url = url + f"/api/register"
    # Send POST request to the specified URL
    response = requests.post(register_url, json=payload)

    if response.status_code == 200:
        st.success("Registration successful!")
    else:
        st.error("Registration failed. Please try again.")

st.title("User Sign-Up")

langchain_experience_options = [
        "No experience",
        "3-6 Months",
        "6 Months-1 year",
        "1-2 years",
        "2-3 years",
    ]

use_case_options = [
        "Personal projects",
        "Academic research",
        "Business applications",
        "Data analysis",
        "Chatbot development",
        "Knowledge management",
        "Other"
    ]

feedback = [
        "Yes",
        "No"
    ]


with st.form("registration_form"):
    st.text_input("First Name", key="first_name")
    st.text_input("Last Name", key="last_name")
    st.text_input("Email", key="email")
    st.selectbox("Langchain Experience", options=langchain_experience_options, key="langchain_experience")
    st.selectbox("Use Case", options=use_case_options, key="use_case")
    st.selectbox("Do you have time to give feedback and participate in the Discord community?", options=feedback, key="feedback")
    st.form_submit_button("Register", on_click=submit_form)

