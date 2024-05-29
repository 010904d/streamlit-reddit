import firebase_admin
from firebase_admin import credentials, auth
from streamlit_card import card
import streamlit as st

# Check if Firebase app is already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("streamlit-reddit-a547a-b5c61d9f5bda.json")  
    firebase_admin.initialize_app(cred)

# Define session state class
class SessionState:
    def __init__(self):
        self.active_card = None

# Create a session state object
session_state = SessionState()

def main():
    st.title("Welcome to CodersCo 🥸")

    # Create a layout with two columns
    col1, col2 = st.columns(2)

    # Card for login in the first column
    with col1:
        login_clicked = card(
            title="Login",
            text="Click here to login",
            key="login_card"
        )

    # Card for signup in the second column
    with col2:
        signup_clicked = card(
            title="Sign Up",
            text="Click here to sign up",
            key="signup_card"
        )

    # Determine which card is clicked
    if login_clicked:
        session_state.active_card = "login"
    elif signup_clicked:
        session_state.active_card = "signup"

    # Show login or signup functionality based on active card
    if session_state.active_card == "login":
        login()
    elif session_state.active_card == "signup":
        signup()

def login():
    st.subheader("Login")
    email = st.text_input('Email Address', key="login_email")
    password = st.text_input('Password', type='password', key="login_password")
    if st.button('Login'):
        # Authenticate user
        try:
            user = auth.get_user_by_email(email)
            st.success('Logged in successfully!')
            st.write('User ID:', user.uid)
        except auth.UserNotFoundError:
            st.error('No user found with this email. Please sign up.')
            session_state.active_card = "signup"
        except Exception as e:
            st.error('Login failed: ' + str(e))


def signup():
    st.subheader("Sign Up")
    email = st.text_input('Email Address', key="signup_email")
    password = st.text_input('Password', type='password', key="signup_password")
    username = st.text_input('Enter your unique username', key="signup_username")
    if st.button('Create my account'):
        try:
            # Check if user with email already exists
            auth.get_user_by_email(email)
            # If user exists, prompt to login
            st.error('An account with this email already exists. Please login.')
            session_state.active_card = "login"
        except auth.UserNotFoundError:
            # If user doesn't exist, create new account
            try:
                user = auth.create_user(email=email, password=password)
                st.success('Account created successfully!')
                st.write('User ID:', user.uid)
                st.markdown('Please login using your email and password')
                st.balloons()
            except Exception as e:
                st.error('Signup failed: ' + str(e))
        except Exception as e:
            st.error('Signup failed: ' + str(e))


if __name__ == "__main__":
    main()






