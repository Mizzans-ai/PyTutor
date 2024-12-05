import streamlit as st
import sqlite3
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
import pandas as pd
import json
import chatbot
from chatbot import chatbot_interface
from datetime import datetime
from test2 import python_ide
from content2 import (
    display_module,
    display_test,
    project_content,
    get_file_content,
    get_progress,
)
from authentication2 import signup  # Keep the signup function


# Initialize the database
def init_db():
    with sqlite3.connect('testing.db', check_same_thread=False) as conn:
        c = conn.cursor()
        
        # Create 'testing' table if it doesn't exist with all required columns
        c.execute('''
            CREATE TABLE IF NOT EXISTS testing (
                id TEXT PRIMARY KEY,
                password TEXT,
                age INTEGER,
                gender TEXT,
                occupation TEXT,
                education TEXT,
                test_scores TEXT,
                module_progress INTEGER
            )
        ''')

        # Create 'user_sessions' table if it doesn't exist
        c.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                login_time DATETIME NOT NULL,
                logout_time DATETIME,
                duration INTEGER
            )
        ''')

        conn.commit()

# Initialize the database when the script runs
init_db()
# Initialize session state for module_progress
def initialize_session_state():
    if 'module_progress' not in st.session_state:
        st.session_state['module_progress'] = 0



st.markdown("""
    <style>
    /* Set background color */
    .main {
        background-color: navy;  /* Change background color to navy blue */
        color: white;            /* Change text color to white for contrast */
        font-family: 'Roboto', Times new Roman;  /* Use Roboto font for the application */
    }
    /* Animation for the title */
    .title {
        font-family: 'Roboto', Times new Roman;  /* Update to your chosen font */
        color: #4A90E2;                     /* Title color */
        font-weight: bold;
        font-size: 130px;                   /* Update font size to 130 pixels */
        text-align: center;
        margin-bottom: 15px;
        animation: float 3s ease-in-out infinite; /* Floating animation */
    }
    /* Style for the LOGIN heading */
    .login-title {
        font-family: 'Roboto', Times new Roman;  /* Use the same font as the title */
        color: #4A90E2;                     /* Same color as the title */
        font-weight: bold;                  /* Make it bold */
        font-size: 100px;                   /* Adjust font size for login */
        text-align: center;
        margin-bottom: 15px;                /* Add margin for spacing */
        animation: fadeIn 5s ease-in-out;  /* Animation effect */
    }
    /* Floating animation */
    @keyframes float {
        0%, 100% {
            transform: translateY(0px); /* Starting and ending position */
        }
        50% {
            transform: translateY(-10px); /* Move up by 10px at the midpoint */
        }
    }
    /* Fade-in animation */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    /* Add padding */
    .stTextInput, .stButton, .stSidebar, .stRadio {
        margin: 2px 0;
        padding: 1.5px;
    }
    /* Style buttons */
    .stButton > button {
        color: #fff;
        background-color: #5072A7;
        font-weight: bold;
        border: 5px;
        transition: background-color 0.3s ease; /* Button hover effect */
        width: 100%; /* Ensures buttons take the full width of the sidebar */
        padding: 10px; /* Consistent padding for all buttons */
        margin-bottom: 5px; /* Space between buttons */
    }
    .stButton > button:hover {
        background-color: #3D5C99; /* Darker blue on hover */
    }
    /* Sidebar styling */
    .stSidebar {
        background-color: #132257; /* Sidebar color */
        color: #333; /* Sidebar text color */
    }
    /* Additional styling for headers */
    h1, h2, h3 {
        color: #71b9bf; /* Consistent color for headers */
    }
    /* Style stRadio buttons */
    .stRadio > label > div {
        background-color: #132257; /* White background for stRadio buttons */
        color: #fff; /* Text color */
        border-radius: 5px; /* Rounded corners for radio buttons */
        padding: 5px; /* Padding for each radio button */
        margin-bottom: 5px; /* Space between radio buttons */
    }
    /* Style stRadio hover */
    .stRadio > label > div:hover {
        background-color: #132257; /* Light grey background on hover */
    }
    /* Ensure consistency for all buttons in the sidebar */
    .stSidebar button {
        width: 90%; /* Set uniform width */
        padding: 12px; /* Adjust padding to make all buttons the same size */
        text-align: center; /* Center text */
    }
</style>

""", unsafe_allow_html=True)



# Function to initialize session state
def initialize_session_state():
    if 'page' not in st.session_state:
        st.session_state['page'] = "login"



# Function to get user progress
def get_progress(user_id):
    with sqlite3.connect('testing.db') as conn:
        c = conn.cursor()
        # Create the user_sessions table
        c.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            login_time TIMESTAMP NOT NULL,
            logout_time TIMESTAMP,
            duration INTEGER
        )
    ''')
    conn.commit()




    print("user_sessions table created successfully.")
    c.execute("SELECT module_progress FROM testing WHERE id = ?", (user_id,))
    progress = c.fetchone()[0]
    return progress



# CSS styling for the login and signup pages
st.markdown("""
    <style>
        /* Style for the app title and subtitle */
        .title {
            font-size: 5em;
            font-weight: bold;
            color: #4B8BBE;
            text-align: center;
            margin-bottom: 30px;
        }
        .subtitle {
            font-size: 1.5em;
            font-weight: bold;
            color: #FFE873;
            text-align: center;
            margin-bottom: 0.5px;
        }
 
       
        /* Style for the login button */
        .login-btn {
            background-color: #4A90E2;
            color: #4A90E2;
            font-size: 5em;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
            margin-top: 20px;
            width: 100%;
        }
        .login-btn:hover {
            background-color: #3b7bc1;
        }
       
        /* Input fields styling */
        .stTextInput label {
            font-weight: bold;
            color: #555;
        }
    </style>
    """, unsafe_allow_html=True)


# Function to handle sign-up process
def signup():
    st.markdown('<div class="title">AI PyTutor</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Sign Up</div>', unsafe_allow_html=True)
    
    with sqlite3.connect('testing.db', check_same_thread=False) as conn:
        c = conn.cursor()
        
        # Check existing columns in the 'testing' table
        c.execute("PRAGMA table_info(testing)")
        existing_columns = [col[1] for col in c.fetchall()]
        
        # Add columns if they do not already exist
        columns_to_add = [
            ("age", "INTEGER"),
            ("gender", "TEXT"),
            ("occupation", "TEXT"),
            ("education", "TEXT"),
            ("test_scores", "TEXT"),
            ("module_progress", "INTEGER")
        ]
        
        for column, col_type in columns_to_add:
            if column not in existing_columns:
                c.execute(f"ALTER TABLE testing ADD COLUMN {column} {col_type}")
        
        conn.commit()

    # Container for styling the sign-up form box
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)

        user_id = st.text_input("Choose a User ID", placeholder="Choose a unique User ID")
        password = st.text_input("Create a Password", type='password', placeholder="Enter a strong password")
        age = st.number_input("Enter Your Age", min_value=0, step=1)
        gender = st.selectbox("Select Your Gender", options=["Select your Gender", "Male", "Female", "Other"])
        occupation = st.text_input("Enter Your Occupation", placeholder="e.g., Student, Working Professional, etc.")
        education = st.selectbox("Enter Your Education Level", options=["Select your Education Level", "Xth Grade", "XIIth Grade", "Bachelor's", "Master's", "Ph.D"])

        if st.button("Sign Up", key="signup_button"):
            with sqlite3.connect('testing.db') as conn:
                c = conn.cursor()
                c.execute("""
                    INSERT INTO testing (id, password, age, gender, occupation, education, module_progress)
                    VALUES (?, ?, ?, ?, ?, ?, 1)
                """, (user_id, password, age, gender, occupation, education))
                conn.commit()
                st.success("Account created successfully! You can now log in.")
                st.session_state['page'] = "login"
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)  # Close the login-container div


# Define the login function
def login():
    # Display the title and subtitle with custom HTML
    st.markdown('<div class="title">AI PyTutor</div>', unsafe_allow_html=True)  # Title for the app
    st.markdown('<div class="subtitle">Login</div>', unsafe_allow_html=True)  # Subtitle for login



    # Container for styling the login form box
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
       
        # Login form for user ID and password input
        with st.form(key="login_form"):
            user_id = st.text_input("User ID", placeholder="Enter your user ID")
            password = st.text_input("Password", type='password', placeholder="Enter your password")
           
            # Submit button for the login form
            submit_button = st.form_submit_button("Login", use_container_width=True, on_click=None)




        st.markdown('</div>', unsafe_allow_html=True)  # Close the login-container div




    if submit_button:
        # Check login credentials
        with sqlite3.connect('testing.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM testing WHERE id = ? AND password = ?", (user_id, password))
            user = c.fetchone()

            if user:
                st.session_state['user_id'] = user_id
                st.session_state['module_progress'] = user[2]
                st.session_state['page'] = "home"


                # Log the login time in the user_sessions table
                login_time = datetime.now()
                c.execute("INSERT INTO user_sessions (user_id, login_time) VALUES (?, ?)", (user_id, login_time))
                conn.commit()

                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid User ID or Password. Please try again.")



# Logout function
def logout():
    user_id = st.session_state.get('user_id')
    if user_id:
        logout_time = datetime.now()
        with sqlite3.connect('testing.db') as conn:
            c = conn.cursor()
            c.execute("SELECT login_time FROM user_sessions WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id,))
            login_record = c.fetchone()
            if login_record:
                login_time = datetime.fromisoformat(login_record[0])
                duration = (logout_time - login_time).seconds
                c.execute("UPDATE user_sessions SET logout_time = ?, duration = ? WHERE user_id = ? AND login_time = ?",
                          (logout_time, duration, user_id, login_record[0]))
                conn.commit()
        st.session_state.clear()
        st.rerun()



# Function to display the user dashboard 
def display_dashboard():
    st.markdown(
        """
        <style>
            .dashboard-container {
                background-color: #f5f7fa;
                color: #4A90E2;
                padding: 10px;
                border-radius: 5px;
                box-shadow: 2px 4px 8px rgba(4, 8, 12, 0.1);
                margin-bottom: 10px;
            }
            .profile-header {
                font-size: 30px;
                font-weight: bold;
                color: #4A90E2;
                margin-bottom: 15px;
            }
            .section-title {
                font-size: 30px;
                font-weight: bold;
                margin-top: 20px;
                color: #fff;
            }
            .info-box {
                padding: 8px;
                background-color: #002D62;
                color: white;
                border-radius: 15px;
                margin-bottom: 15px;
            }
            .chart-container {
                display: flex;
                font-weight: bold;
                padding: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Welcome to AI PyTutor🤖")
    user_id = st.session_state.get('user_id')
    
    if user_id:
        with sqlite3.connect('testing.db') as conn:
            c = conn.cursor()
            
            # Fetch module progress and test scores
            c.execute("SELECT module_progress, test_scores, age, gender, occupation, education FROM testing WHERE id = ?", (user_id,))
            progress_data = c.fetchone()

            if progress_data:
                completed_modules = progress_data[0] - 1 if progress_data[0] else 0
                test_scores = json.loads(progress_data[1]) if progress_data[1] else []
                age, gender, occupation, education = progress_data[2], progress_data[3], progress_data[4], progress_data[5]
            else:
                completed_modules = 0
                test_scores = []
                age = gender = occupation = education = ""

            # Total number of modules
            total_modules = 19
            remaining_modules = total_modules - completed_modules
            progress_percent = (completed_modules / total_modules) * 100

            # Display user information and module progress
            st.markdown('<div class="section-title">User Information🪪</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-box">User ID: {user_id}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-box">Age: {age}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-box">Gender: {gender}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-box">Occupation: {occupation}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-box">Education: {education}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-box">Modules Completed: {completed_modules} / {total_modules}</div>', unsafe_allow_html=True)
            st.progress(progress_percent / 100)
            st.markdown(f'<div class="info-box">Overall Progress: {progress_percent:.1f}%</div>', unsafe_allow_html=True)

            # Display next recommended module
            next_module = completed_modules + 1 if completed_modules < total_modules else None
            if next_module:
                st.markdown(f'<div class="info-box">Next Module: Module {next_module}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="info-box">All Modules Completed!</div>', unsafe_allow_html=True)

            # Overall Progress Chart
            st.markdown('<div class="chart-container">Track Your Progress📊</div>', unsafe_allow_html=True)
            fig_progress = go.Figure(data=[go.Pie(
                labels=['Completed', 'Remaining'],
                values=[completed_modules, remaining_modules],
                marker=dict(colors=['#4A90E2', '#FFE873']),
                hole=0.3
            )])
            fig_progress.update_layout(
                title_text="Overall Module Completion",
                width=320,  # Adjust the width as desired
                height=320  # Adjust the height as desired
            )
            st.plotly_chart(fig_progress)

            # Fetch and display last 2 login sessions
            c.execute("SELECT login_time, logout_time FROM user_sessions WHERE user_id = ? ORDER BY login_time DESC LIMIT 2", (user_id,))
            recent_sessions = c.fetchall()
            st.markdown('<div class="section-title">Recent Sessions</div>', unsafe_allow_html=True)
            for login, logout in recent_sessions:
                logout_display = datetime.fromisoformat(logout).strftime("%I:%M %p") if logout else "Ongoing"
                login_display = datetime.fromisoformat(login).strftime("%I:%M %p")
                st.markdown(f'<div class="info-box">Login: {login_display}, Logout: {logout_display}</div>', unsafe_allow_html=True)

            # Display streak and achievements
            st.markdown('<div class="section-title">Achievements and Badges🏆</div>', unsafe_allow_html=True)
            if completed_modules >= 1:
                st.markdown('<div class="info-box">🎉 Completed First Module!</div>', unsafe_allow_html=True)
            if completed_modules == total_modules:
                st.markdown('<div class="info-box">🏅 All Modules Completed!</div>', unsafe_allow_html=True)

    else:
        st.write("Please log in to view your dashboard.")

# Main application function
def main():
    initialize_session_state()
    st.markdown(
        """
        <style>
        .floating-chat-button {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            font-size: 24px;
            cursor: pointer;
            z-index: 1000;
        }
        .chatbox {
            position: floating;
            bottom: 20px;
            right: 20px;
            width: 400px;
            z-index: 1000;
        }
        </style>
        """,
        unsafe_allow_html=True
    )






 # Chatbot interface container
    with st.container():
        if 'chat_visible' not in st.session_state:
            st.session_state['chat_visible'] = False


        st.markdown('<div id="chatbox-container" class="chatbox" style="display:none;">', unsafe_allow_html=True)
        with st.expander("Chatbot", expanded=True):
            chatbot_interface()
        st.markdown('</div>', unsafe_allow_html=True)
   






    if 'page' not in st.session_state:
        st.session_state['page'] = "login"




    # Page routing and handling
    if st.session_state['page'] == "login":
        login()
        if st.button("Don't have an account? Sign Up"):
            st.session_state['page'] = "signup"
            st.rerun()




    elif st.session_state['page'] == "signup":
        signup()
        if st.button("Already have an account? Login"):
            st.session_state['page'] = "login"
            st.rerun()




    else:
        
        st.sidebar.title("Welcome to AI PyTutor!..🤖")
        if st.sidebar.button("Dashboard"):
            st.session_state['page'] = "dashboard"
            st.rerun()
        if st.sidebar.button("Home"):
            st.session_state['page'] = "home"
            st.rerun()
        if st.sidebar.button("Python IDE"):
            st.session_state['page'] = "python_ide"
            st.rerun()
        if st.sidebar.button("Modules"):
            st.session_state['page'] = "modules"
            st.rerun()
        if st.sidebar.button("Logout"):
            logout()




        # Page content
        if st.session_state['page'] == "dashboard":
            display_dashboard()  # Corrected to call display_dashboard as a function
           
        elif st.session_state['page'] == "home":
            user_id = st.session_state.get('user_id')
            if user_id:
                progress = get_progress(user_id)
                st.success(f"Modules completed: {progress - 0}")
            st.title("Welcome to Your AI-Powered Python Tutor! 🚀")
            st.markdown('<div class="box"><h4>Ready to take your Python skills to the next level?</h4><p>Whether you\'re just starting or looking to sharpen your coding expertise, AI Python Tutor is here to guide you 24/7 with personalized lessons tailored just for you.</p></div>', unsafe_allow_html=True)
            st.markdown('<div class="box"><h4>Imagine having a mentor...</h4><p>Imagine having a mentor who never gets tired of your questions, explains concepts with infinite patience, and celebrates every bit of progress you make.</p></div>', unsafe_allow_html=True)
            st.markdown('<div class="box"><h4>Committed to Your Success</h4><p>By your side at every step, AI tutor is dedicated to helping you unlock your full potential.</p></div>', unsafe_allow_html=True)




        elif st.session_state['page'] == "python_ide":
            st.write(python_ide())




        elif st.session_state['page'] == "modules":
            module_selected = st.sidebar.radio('MODULES:', options=[
                "Introduction",
                "Module-1 : Introduction to python", "Module-1 test",
                "Module-2 : Python variables", "Module-2 test",
                "Module-3 : Python Data Types", "Module-3 test",
                "Module-4 : Operators-1", "Module-4 test",
                "Module-5 : Data Structures", "Module-5 test",
                "Module-6 : Operators-2", "Module-6 test",
                "Module-7 : Logical Operators", "Module-7 test",
                "Module-8 : Conditional Statements", "Module-8 test",
                "Module-9 : Loops", "Module-9 test", "Project-1",
                "Module-10 : Sets", "Module-10 test",
                "Module-11 : Dictionary", "Module-11 test",
                "Module-12 : String Functions", "Module-12 test",
                "Module-13 : Functions", "Module-13 test",
                "Module-14 : Lambda Functions", "Module-14 test",
                "Module-15 : File Handling", "Module-15 test",
                "Module-16 : Exception Handling", "Module-16 test",
                "Module-17 : OOPs-1", "Module-17 test",
                "Module-18 : OOPs-2", "Module-18 test",
                "Module-19 : OOPs-3", "Module-19 test", "Project-2"
            ])




            if module_selected == "Introduction":
                st.video(r"https://youtu.be/SaGTAj3n_aU?si=MwJr4NJ3ZJahatRG")
                content = get_file_content("Modules/introduction")
                st.markdown(content, unsafe_allow_html=True)
         


            elif module_selected == "Module-1 : Introduction to python":
                display_module(1, "Using the print function, write a sentence about your hobbies.","Just the print function and nothing else")
            elif module_selected == "Module-1 test":
                display_test(1, "You are a student and need to introduce yourself . Use the Python print function to print your introduction.")




            elif module_selected == "Module-2 : Python variables":
                display_module(2, "Take a student's name as input, store it in a variable and print its length.","Just Print Function and Python variables.")
            elif module_selected == "Module-2 test":
                display_test(2, "Suppose you are an employee working in a company. Store your employee ID, city, gender, and salary in separate variables and print them.")



            elif module_selected == "Module-3 : Python Data Types":
                display_module(3, "Create variables for Name, Class, and GPA (in decimal points) and print their data types.","Just the Print Function, Python variables and Python Data Types.")
            elif module_selected == "Module-3 test":
                display_test(3, "Create a variable named student_rollnumber and assign it a number in string format. Print its data type. Convert the variable to an integer and print the data type again.")




            elif module_selected == "Module-4 : Operators-1":
                display_module(4, "Imagine you have marks in two subjects, Maths and Science. Create a comparison using an operator to check if marks in Maths are greater than marks in Science. Print the result of this comparison.","Just the Print Function, Python variables, Python Data Types and Operators-1.")
            elif module_selected == "Module-4 test":
                display_test(4, "Suppose you are a student. The teacher just announced marks for subjects Maths, Science, and English, which are 70, 60, and 90 respectively. Store these in variables and print their sum.")




            elif module_selected == "Module-5 : Data Structures":
                display_module(5, "Create a list of numbers with elements [1, 3, 7, 2, 4], print the list, use a list method to remove the element 7. Print the modified list after removal.","Just the Print Function, Python variables, Python Data Types Operators-1 and Data Structures.")
            elif module_selected == "Module-5 test":
                display_test(5, "Create a list of fruits containing 'apple', 'banana', and 'orange'. Use a list method to add 'grape' to the end of the list. Print the modified list.")





            elif module_selected == "Module-6 : Operators-2":
                display_module(6, "Check if a student's name is present in a list of students using a membership operator. Print the result.","Just the Print Function, Python variables, Python Data Types Operators-1, Data Structures and Operators-2.")
            elif module_selected == "Module-6 test":
                display_test(6, "Create two variables pointing to the same list of marks. Use an identity operator to verify if they are the same object. Print the result.")




            elif module_selected == "Module-7 : Logical Operators":
                display_module(7, "Imagine a student with variables has_homework and has_study_materials set to True or False. Use logical operators to check if the student has both homework and study materials. Print the result of this logical operation.","Just the Logical Operators.")
            elif module_selected == "Module-7 test":
                display_test(7, "Write a program to check if a student has either completed their homework or has a test tomorrow. Print the result.")




            elif module_selected == "Module-8 : Conditional Statements":
                display_module(8, "Write a program that takes a person's    age checks if a person is eligible to vote or not.","Just the Conditional Statements.")
            elif module_selected == "Module-8 test":
                display_test(8, "Write a program to check the grade of a student based on their marks (e.g., A, B, C, etc.).")



            elif module_selected == "Module-9 : Loops":
                display_module(9, "Write a Python program to print the first 10 numbers using a while loop.","Just the Loops.")
            elif module_selected == "Module-9 test":
                display_test(9, "Write a Python program to print all the even numbers from 1 to 20 using a for loop.")




            elif module_selected == "Project-1":
                topics = [
                                                                                "Print Statement",
                                                                                "Python Variables",
                                                                                "Rules of Creating a Variable Name",
                                                                                "Comments",
                                                                                "Built-In Functions (Input, Len, etc.)",
                                                                                "What are Data Types?",
                                                                                "Built-in Data Types: Integer, Float, String",
                                                                                "Type Function",
                                                                                "Type Casting",
                                                                                "Arithmetic Operators",
                                                                                "Assignment Operators",
                                                                                "Comparison Operators","List and list methods","Identity,Membership and logical operator",
                                                                                "Conditional statements","Loops","tuple"
                                                                            ]
                project_content("Projects/Project-1",topics_completed =topics)



            elif module_selected == "Module-10 : Sets":
                display_module(10, "Create a set of your favorite movies and another set of your friend's favorite movies. Find the union of both sets and print the result.","Just the Sets")
            elif module_selected == "Module-10 test":
                display_test(10, "Create two sets of students who have opted for Maths and Science respectively: maths_students = {'John', 'Jane', 'Jim'} and science_students = {'Jane', 'Jim', 'Jake'}. Find the intersection of these sets and print the result.")




            elif module_selected == "Module-11 : Dictionary":
                display_module(11, "Create a dictionary of three students with their names as keys and their grades as values. Print the dictionary.","Just the Dictionary")
            elif module_selected == "Module-11 test":
                display_test(11, "Create a dictionary representing a student with keys name, age, and subjects where subjects is a list of subjects the student is enrolled in. Add a new subject to the list and print the modified dictionary.")




            elif module_selected == "Module-12 : String Functions":
                display_module(12, "","")
            elif module_selected == "Module-12 test":
                display_test(12, "")



            elif module_selected == "Module-13 : Functions":
                display_module(13, "Write a function calculate_average that takes a list of numbers as input and returns the average of those numbers.","")
            elif module_selected == "Module-13 test":
                display_test(13, "Write a function calculate_rectangle_area that takes width and height as parameters and returns the area of a rectangle.")



            elif module_selected == "Module-14 : Lambda Functions":
                display_module(14, "Write a lambda function that checks if a number is even.","")
            elif module_selected == "Module-14 test":
                display_test(14, "Write a lambda function that squares a given number.")



            elif module_selected == "Module-15 : File Handling":
                display_module(15, "Write a Python program that reads a text file and prints its contents.","")
            elif module_selected == "Module-15 test":
                display_test(15, "Write a Python program that writes a list of strings to a file.")



            elif module_selected == "Module-16 : Exception Handling":
                display_module(16, "Write a Python program that handles division by zero exception.","")
            elif module_selected == "Module-16 test":
                display_test(16, "Write a custom exception for invalid ages and handle it in a program.")



            elif module_selected == "Module-17 : OOPs-1":
                display_module(17, "Define a class Book with attributes title, author, and pages. Create an instance of the class and print the attributes.","")
            elif module_selected == "Module-17 test":
                display_test(17, "Define a class Car with attributes make, model, and year. Add a method display_info that prints the car's information. Create an instance of the class and call the method.")



            elif module_selected == "Module-18 : OOPs-2":
                display_module(18, "Define a base class Person with attributes name and age. Define a subclass Student that adds an attribute student_id and a method display_student_info that prints all attributes. Create an instance of Student and call the method.","")
            elif module_selected == "Module-18 test":
                display_test(18, "Define a base class Employee with attributes name and salary. Define a subclass Manager that adds an attribute department and a method display_manager_info that prints all attributes. Create an instance of Manager and call the method.")



            elif module_selected == "Module-19 : OOPs-3":
                display_module(19, "Define a class Employee with private attributes _name and _salary. Provide methods get_name, set_name, get_salary, and set_salary to access and update the attributes. Create an instance of the class and test the methods.","")
            elif module_selected == "Module-19 test":
                display_test(19, "Define a class Course with private attributes _course_name and _students (a list of student names). Provide methods to add a student, remove a student, and print the list of students. Create an instance of the class and test the methods.")


            elif module_selected == "Project-2":
                topics = [
                                                                                "Print Statement",
                                                                                "Python Variables",
                                                                                "Rules of Creating a Variable Name",
                                                                                "Comments",
                                                                                "Built-In Functions (Input, Len, etc.)",
                                                                                "What are Data Types?",
                                                                                "Built-in Data Types: Integer, Float, String",
                                                                                "Type Function",
                                                                                "Type Casting",
                                                                                "Arithmetic Operators",
                                                                                "Assignment Operators",
                                                                                "Comparison Operators"," List and list methods","Identity,Membership and logical operator",
                                                                                "Conditional statements","Loops","tuple", " Defining and Using Functions",
                                                                                " Understanding Lambda Functions",
                                                                                "Working with Python Modules and Packages",
                                                                                " File Handling in Python",
                                                                                " Exception Handling Techniques",
                                                                                " Introduction to Object-Oriented Programming",
                                                                                " Inheritance in OOP",
                                                                                " Encapsulation and Polymorphism in OOP"
                                                                            ]
                project_content("Projects/Project-2",topics_completed =topics)


if __name__ == "__main__":
    init_db()
    main()