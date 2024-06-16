import streamlit as st
import requests


def submit_form():
    # Get user input values
    name = st.session_state.name
    email = st.session_state.email
    use_case = st.session_state.use_case
    # Create payload for POST request
    payload = {
        "name": name,
        "email": email,
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

with st.form("registration_form"):
    st.text_input("Name", key="name")
    st.text_input("Email", key="email")
    st.text_area("Use Case", key="use_case")
    st.form_submit_button("Register", on_click=submit_form)

