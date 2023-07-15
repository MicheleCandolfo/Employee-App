import streamlit as st
import time
import numpy as np
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


col1, col2, col3 = st.columns([0.3,0.4,0.3])

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_coding = load_lottiefile("images/login.json")  # replace link to local lottie file

with col2:
    st_lottie(
        lottie_coding,
        speed=1,
        reverse=False,
        loop=True,
        quality="high", # medium ; high # canvas
        height=None,
        width=None,
        key=None,
    )
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        # Send a post request to the token endpoint
        response = requests.post(f"http://localhost:8000/auth/token", 
                                    data={'username': username, 'password': password})
        
        # Check the status of the request
        if response.status_code == 200:
            # If the response is successful, store the token in a session state
            token_response = response.json()
            st.session_state['token'] = token_response['access_token']
            st.success('Logged in successfully')
            
            # You can redirect to the dashboard or something here using st.session_state
            # if 'dashboard' not in st.session_state:
            #     st.session_state['dashboard'] = dashboard_func
            
        else:
            st.warning("Invalid username or password")