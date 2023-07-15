import streamlit as st
import requests 
import pandas as pd
from streamlit_option_menu import option_menu
import json
from streamlit_lottie import st_lottie

st.set_page_config(
    page_title="Employee App",
    page_icon="👤",
)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style/style.css")

st.title('User Panel')

selected = option_menu(
    menu_title=None,
    options=['Get information', 'Change password'],
    icons=['people', 'gear'],
    menu_icon='cast',
    default_index=0,
    orientation='horizontal',
)

col1, col2 = st.columns([0.7,0.3])
div1, div2 = st.columns([0.4,0.6])

with col1:
    if selected == 'Get information':

        if st.button('User information'):
            # Check if the token exists in the session state
            if 'token' in st.session_state:
                # Get the token
                token = st.session_state['token']
                
                # Include the token in the headers for authentication
                headers = {
                    'Authorization': f'Bearer {token}',
                }

                # Send a GET request with the headers to the endpoint
                response = requests.get("http://localhost:8000/user/", headers=headers)

                # Check the status of the request
                if response.status_code == 200:
                    # If the response is successful, display the data
                    data = [response.json()]  # Put the dictionary into a list
                    df = pd.DataFrame(data)
                    df = df.drop(['hashed_password', 'id', 'is_active'], axis=1)
                    st.dataframe(df)

                else:
                    st.warning("Failed to get data")
            else:
                st.error('Not logged in')

with col1:
    with div1:
        if selected == 'Change password':
            password = st.text_input('Password', type='password')
            new_password = st.text_input('New password', type='password')

            if st.button('Change password'):
                # Check if the token exists in the session state
                if 'token' in st.session_state:
                    # Get the token
                    token = st.session_state['token']

                    data = {
                            'password': password,
                            'new_password': new_password,
                            }
                    
                    # Include the token in the headers for authentication
                    headers = {
                        'Authorization': f'Bearer {token}',
                    }

                    # Send a GET request with the headers to the endpoint
                    response = requests.put("http://localhost:8000/user/password", headers=headers, json=data)

                    # Check the status of the request
                    if response.status_code == 204:
                        # If the response is successful, display the data
                        st.success("Password change successfull.")

                    else:
                        st.warning("Password change failed")
                else:
                    st.error('Not logged in')