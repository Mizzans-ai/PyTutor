import streamlit as st
import sqlite3

def login():
    st.title("Login")
    user_id = st.text_input("User ID")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        if len(user_id) < 3:
            st.error("User ID must be at least 3 characters long.")
        elif len(password) < 4:
            st.error("Password must be at least 4 characters long.")
        else:
            with sqlite3.connect('testing.db', check_same_thread=False) as conn:
                c = conn.cursor()
                c.execute("SELECT * FROM testing WHERE id=? AND password=?", (user_id, password))
                user = c.fetchone()
                if user:
                    st.session_state['user_id'] = user_id
                    st.session_state['module_progress'] = user[2]
                    st.success("Logged in successfully!")
                    st.session_state['page'] = "home"  # Set the page to home after login
                    st.rerun()  # Correct rerun call
                else:
                    st.error("Invalid credentials")

def signup():
    st.title("Sign Up")
    user_id = st.text_input("New User ID")
    password = st.text_input("New Password", type='password')
    if st.button("Sign Up"):
        if len(user_id) < 3:
            st.error("User ID must be at least 3 characters long.")
        elif len(password) < 4:
            st.error("Password must be at least 4 characters long.")
        else:
            with sqlite3.connect('testing.db', check_same_thread=False) as conn:
                c = conn.cursor()
                c.execute("INSERT INTO testing (id, password, module_progress) VALUES (?, ?, ?)", (user_id, password, 1))
                conn.commit()
            st.success("User registered successfully!")
            st.session_state['page'] = "login"  # Redirect to login page
            if 'rerun' not in st.session_state:
                st.session_state.rerun = False

            if st.session_state.rerun:
                st.session_state.rerun = False
                st.rerun()  # Correct rerun call
