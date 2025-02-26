import streamlit as st
from auth.google_auth import GoogleAuth
from auth.password_auth import PasswordAuth

def render_auth():
    st.title("Welcome to Policy Manager")

    # Initialize authentication handlers
    google_auth = GoogleAuth()
    password_auth = PasswordAuth()

    # Login tabs
    auth_type = st.radio("Choose authentication method:", ["Email/Password", "Google"])

    if auth_type == "Email/Password":
        tab1, tab2, tab3 = st.tabs(["Login", "Register", "Reset Password"])

        with tab1:  # Login
            with st.form("login_form"):
                username_or_email = st.text_input("Username or Email")
                password = st.text_input("Password", type="password")

                if st.form_submit_button("Login"):
                    if username_or_email and password:
                        try:
                            user = password_auth.authenticate_user(username_or_email, password)
                            if user:
                                st.session_state.user = user
                                st.rerun()
                            else:
                                st.error("Invalid credentials")
                        except Exception as e:
                            st.error(str(e))
                    else:
                        st.error("Please fill in all fields")

        with tab2:  # Register
            with st.form("register_form"):
                reg_email = st.text_input("Email")
                reg_username = st.text_input("Username")
                st.info("Username must be 3-20 characters, using only letters, numbers, and underscores")
                reg_password = st.text_input("Password", type="password")

                if st.form_submit_button("Register"):
                    if reg_email and reg_username and reg_password:
                        try:
                            user = password_auth.create_user(
                                email=reg_email,
                                username=reg_username,
                                password=reg_password
                            )
                            st.success("Registration successful! Please login.")
                        except Exception as e:
                            st.error(str(e))
                    else:
                        st.error("Please fill in all fields")

        with tab3:  # Reset Password
            if "reset_step" not in st.session_state:
                st.session_state.reset_step = "request"

            if st.session_state.reset_step == "request":
                with st.form("reset_request_form"):
                    reset_email = st.text_input("Enter your email")
                    if st.form_submit_button("Request Password Reset"):
                        if reset_email:
                            try:
                                token = password_auth.generate_reset_token(reset_email)
                                if token:
                                    # In a real application, send this via email
                                    st.success(f"Reset link sent to your email. For demo, use this token: {token}")
                                    st.session_state.reset_step = "reset"
                                else:
                                    st.error("Email not found")
                            except Exception as e:
                                st.error(str(e))

            elif st.session_state.reset_step == "reset":
                with st.form("reset_password_form"):
                    reset_token = st.text_input("Enter reset token")
                    new_password = st.text_input("New password", type="password")
                    if st.form_submit_button("Reset Password"):
                        if reset_token and new_password:
                            try:
                                if password_auth.reset_password(reset_token, new_password):
                                    st.success("Password reset successful! Please login.")
                                    st.session_state.reset_step = "request"
                                else:
                                    st.error("Invalid or expired token")
                            except Exception as e:
                                st.error(str(e))

                if st.button("Back to reset request"):
                    st.session_state.reset_step = "request"

    else:  # Google authentication
        if st.button("Sign in with Google"):
            try:
                # Here you would implement the OAuth flow
                # For demo purposes, we'll use a mock Google sign-in
                google_info = {
                    'email': 'demo@gmail.com',
                    'sub': '123456789'
                }
                user = google_auth.get_or_create_user(google_info)
                st.session_state.user = user
                st.rerun()
            except Exception as e:
                st.error(f"Google Sign-in failed: {str(e)}")