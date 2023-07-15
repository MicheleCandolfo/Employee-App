import streamlit as st
import requests 
import pandas as pd
from streamlit_option_menu import option_menu


st.set_page_config(
    page_title="Employee App",
    page_icon="👤",
)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style/style.css")

st.title('Admin Panel')

selected = option_menu(
    menu_title=None,
    options=['Get all user', 'Update user', 'Delete user'],
    icons=['people', 'gear', 'trash'],
    menu_icon='cast',
    default_index=0,
    orientation='horizontal',
)

if selected == 'Get all user':
    if st.button('Get all user'):
        # Check if the token exists in the session state
        if 'token' in st.session_state:
            # Get the token
            token = st.session_state['token']
            
            # Include the token in the headers for authentication
            headers = {
                'Authorization': f'Bearer {token}',
            }

            # Send a GET request with the headers to the endpoint
            response = requests.get("http://localhost:8000/admin/users", headers=headers)

            # Check the status of the request
            if response.status_code == 200:
                # If the response is successful, display the data
                data = response.json()
                df = pd.DataFrame(data)
                df = df.drop(['hashed_password'], axis=1)
                st.dataframe(df)
                
            else:
                st.warning("Failed to get data")
        else:
            st.error('Not logged in')

if selected == 'Update user':
    col1, col2, col3 = st.columns([0.33,0.33,0.33])
    with col2:
        user_id = st.text_input('User id')
        first_name= st.text_input('First name')
        last_name = st.text_input('Last name')
        role = st.text_input('Role')

        if st.button('Update user'):
            # Check if the token exists in the session state
            if 'token' in st.session_state:
                # Get the token
                token = st.session_state['token']
                
                data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': role
                    }
                # Include the token in the headers for authentication
                headers = {
                    'Authorization': f'Bearer {token}',
                }

                # Send a GET request with the headers to the endpoint
                response = requests.put(f"http://localhost:8000/admin/users/{user_id}", headers=headers, json=data)

                # Check the status of the request
                if response.status_code == 204:
                    st.success('User updated successfully')
                else:
                    st.warning("Could not update user",icon="⚠️")
            else:
                st.error('Not logged in')

if selected == 'Delete user':
    col1, col2, col3 = st.columns([0.33,0.33,0.33])
    with col3:
        user_id = st.text_input('User id')

        if st.button('Delete user'):
            # Check if the token exists in the session state
            if 'token' in st.session_state:
                # Get the token
                token = st.session_state['token']
                # Include the token in the headers for authentication
                headers = {
                    'Authorization': f'Bearer {token}',
                }

                # Send a GET request with the headers to the endpoint
                response = requests.delete(f"http://localhost:8000/admin/users/{user_id}", headers=headers)
                 # Check the status of the request
                if response.status_code == 204:
                    st.success('User successfully deleted')
                else:
                    st.warning("Could not delete user",icon="⚠️")
            else:
                st.error('Not logged in')