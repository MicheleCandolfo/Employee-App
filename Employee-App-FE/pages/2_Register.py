import streamlit as st
import requests
from streamlit_lottie import st_lottie
import json

st.set_page_config(
    page_title="Employee App",
    page_icon="👤",
)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style/style.css")


col1, col2, col3 = st.columns([0.33, 0.5, 0.33])


with col2:
# User registration form
    st.title('User Registration')
    username = st.text_input("Username")
    email = st.text_input("Email")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    role = st.text_input("Role")
    password = st.text_input("Password", type='password')


    if st.button('Register'):
        # Prepare data
        data = {"username": username, "email": email, "first_name": first_name, "last_name": last_name, "role": role, "password": password}

        # Make a POST request to the FastAPI server
        response = requests.post("http://localhost:8000/auth/", json=data)

        if response.status_code == 201:
            st.success('Registration successful')
        else:
            st.error('Registration failed. Please try again.')
 
