import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
import model as m

st.title("Welcome To Personalized Learning")
import mysql.connector  # Assuming MySQL (replace with your connector)
def set_default_bg(url):
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("{url}");
             background-size: cover;
             opacity: 0.8; 
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
set_default_bg("https://c4.wallpaperflare.com/wallpaper/935/849/231/background-tree-book-wallpaper-preview.jpg")
# Session state for user authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.session_state["page"] = "login"  # Default page

def connect_to_database():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="PLMS"
        )
        return mydb
    except mysql.connector.Error as err:
        print("Error connecting to database:", err)
        return None

def login(username, password):
    mydb = connect_to_database()
    mycursor = mydb.cursor()

    # Replace with your actual SQL SELECT query (consider password hashing)
    sql = "SELECT * FROM Register WHERE username = %s AND password = %s"
    val = (username, password)

    try:
        mycursor.execute(sql, val)
        result = mycursor.fetchone()
        if result:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.success("Login successful!")
            return True
        else:
            st.error("Invalid username or password")
            return False
    except mysql.connector.Error as err:
        print("Error logging in user:", err)
        st.error("Login failed!")
        return False
    finally:
        if mydb is not None:
            mydb.close()

def register(username, password , education, interests):
    mydb = connect_to_database()
    mycursor = mydb.cursor()

    # Replace with your actual SQL INSERT query (consider password hashing)
    sql = "INSERT INTO Register (username, password, Education, Interests) VALUES (%s, %s, %s, %s)"
    val = (username, password , education, interests)

    try:
        mycursor.execute(sql, val)
        mydb.commit()
        st.success("Registration successful!")
        return True
    except mysql.connector.Error as err:
        print("Error registering user:", err)
        st.error("Registration failed!")
        return False
    finally:
        if mydb is not None:
            mydb.close()

def login_page():
    st.header("Login")
    st.session_state.username = st.text_input("Username", key="login_username")  # Unique key
    password = st.text_input("Password", type="password", key="login_password")  # Unique key
    submit_login = st.button("Login", key="login_button")  # Add unique key

    if submit_login:
        if login(st.session_state.username, password):
            st.session_state["page"] = "page2" 

def register_page():
    st.header("Register")
    username = st.text_input("Username", key="register_username")  # Unique key
    password = st.text_input("Password", type="password", key="register_password")  # Unique key
    education = st.text_input("Education", type="default", key="register_education")
    interests = st.text_input("Interests", type="default", key="register_interests")
    submit_register = st.button("Register",key="submit_button")

    if submit_register:
        if register(username, password, education, interests):
            st.session_state["page"] = "login"  # Redirect to login page after successful registration

def logout():
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.session_state["page"] = "login"  # Redirect to login page after logout
    st.success("Logged out successfully!")

def create_navigation_bar():
    if st.sidebar.button("Login"):
        st.session_state["page"] = "login"
    if st.sidebar.button("Register"):
        st.session_state["page"] = "register"

def page2():
    # create_navigation_bar() 

    st.header("Dashboard")

    # Check if user is authenticated
    if not st.session_state["authenticated"]:
        st.error("Please login to access the dashboard.")
        return

    mydb = connect_to_database()
    mycursor = mydb.cursor()

    # Replace with your actual SQL SELECT query to fetch user details
    sql = "SELECT username, password, Education, Interests FROM Register WHERE username = %s"
    val = (st.session_state["username"],)  # Use session state username

    try:
        mycursor.execute(sql, val)
        result = mycursor.fetchone()
        if result:
            username, password, education, interests = result

            # Display user details
            st.subheader("User Details")
            st.write("Username:", username)
            # Consider masking password for security (don't store plain text passwords!)
            st.write("Password:", password[:2] + "** (masked)**")  # Mask password for security
            st.write("Education:", education)
            st.write("Interests:", interests)

            # Navigation options within the page (consider using st.sidebar for a cleaner layout)
            # Navigation options within the page
            # if st.button("Edit Profile"):
            #     edit_profile(
        else:
            st.error("User details not found!")
    except mysql.connector.Error as err:
        print("Error fetching user details:", err)
        st.error("An error occurred while retrieving your details.")
    finally:
        if mydb is not None:
            mydb.close()
    
    COURSES = st.button("COURSES", key="courses_button") 
     # Add unique key
    if COURSES:
        st.session_state["page"] = "courses" 


# import streamlit as st  # Assuming you're using Streamlit



import os
import pickle
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import os
import pickle
from sklearn.feature_extraction.text import CountVectorizer

# Get the full path to the courses.pkl file
current_directory = os.path.dirname(os.path.abspath(__file__))
courses_pkl_path = os.path.join(current_directory, 'courses.pkl')

# # Load the courses.pkl file with error handling
# with open(courses_pkl_path, 'rb') as f:
#     # courses_list = pickle.load(f, encoding='latin1')
#     courses_list = pd.read_pickle(courses_pkl_path)
#     # print(courses_list)

# Load the courses.pkl file with error handling
with open(courses_pkl_path, 'rb') as f:
    try:
        courses_list = pd.read_pickle(courses_pkl_path)
        print(courses_list)
        if courses_list.empty:
            st.error("The courses list is empty.")
        else:
            # st.success("Courses loaded successfully.")
            # Print out the courses_list to inspect its contents
            print(courses_list.head())
    except Exception as e:
        st.error(f"Error loading courses list: {e}")

similarity_path = os.path.join(current_directory, 'similarity.pkl')


# Load the similarity.pkl file (similar error handling can be added)
with open(similarity_path, 'rb') as f:
    similarity = pickle.load(f)

import mysql.connector
import sqlite3
import mysql.connector

import mysql.connector
import sqlite3
import mysql.connector

def get_user_profile(username):
    """Fetches user interests and education from the PLMS database.

    Args:
        username (str): The username of the user to retrieve data for.

    Returns:
        tuple: A tuple containing user interests (string) and education (string),
               or None if no data is found for the user.
    """

    # Establish a connection to the PLMS database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="PLMS"
    )
    cursor = mydb.cursor()

    try:
        # Fetch user interests from the 'register' table
        cursor.execute("SELECT Interests FROM Register WHERE username = %s", (username,))
        interests = cursor.fetchone()

        # Check if data was found for the user
        if interests:
            interests = interests[0]  # Extract the interest value from the tuple

        # Fetch user education from the 'education' table
        cursor.execute("SELECT Education FROM Register WHERE username = %s", (username,))
        education = cursor.fetchone()

        if education:
            education = education[0]  # Extract the education value from the tuple

        return interests, education
    except mysql.connector.Error as e:
        print(f"An error occurred: {e}")
        return None  # Indicate error by returning None
    finally:
        cursor.close()
        mydb.close()

# Example usage (replace 'your_username' with the actual username)
user_interests,user_education = get_user_profile('Sailaja123')
user_profile = ''
if user_interests:
    user_profile += ' '.join(user_interests)
if user_education:
    user_profile += ' ' + ' '.join(user_education)
print(user_profile)


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommended_course(courses):
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    print(courses)

    uname = st.session_state.username
    # Example usage (replace 'your_username' with the actual username)
    user_interests, user_education = get_user_profile(uname)
    user_profile = ''

    if user_interests:
        user_profile += ''.join(user_interests)
    if user_education:
        user_profile += ' ' + ''.join(user_education)

    # print(user_profile)
    # Tokenize user profile into individual words
    user_profile_words = user_profile.split()
    # print(user_profile_words)
    # print(len(user_profile_words))
    # Combine user profile and course tags into a single list
    combined_text = list(courses)
    combined_text.append(user_profile)
    print(combined_text)
    # Initialize CountVectorizer and fit on the combined text
    cv = CountVectorizer(max_features=6000, stop_words='english')
    vectors = cv.fit_transform(combined_text)

    # Get the index of the user profile in the vectors
    user_profile_index = len(combined_text) - 1
    # print(user_profile_index)
    # Calculate cosine similarity between user profile and course tags
    user_course_similarity = cosine_similarity(vectors[user_profile_index], vectors[:-1])
    print(user_course_similarity)
    # Get indices of courses sorted by similarity
    sorted_indices = np.argsort(user_course_similarity[0])[::-1]
    print(sorted_indices)
    print(sorted_indices)
    # Print recommended courses
    # sorted_indices = np.argsort(user_course_similarity[0])[::-1]
    
    for idx in sorted_indices[:5]:  # Print top 5 recommended courses
        st.write(courses.iloc[idx]['course_name'])
        st.write(courses.iloc[idx]['Course URL'])


    


# Sample usage

# Sample usage

def courses():
    st.markdown("<h2 style='text-align: center; color: white;'>Course Recommendation System</h2>", unsafe_allow_html=True)
    
    with open(courses_pkl_path, 'rb') as f:
        courses_list = pd.read_pickle(courses_pkl_path)
    
    if st.button('Show Recommended Courses'):
        st.write("Recommended Courses based on your interests are :")
        df,sorted=m.predict(st.session_state.username)
        for idx in sorted[:5]:  # Print top 5 recommended courses
            st.write(df.iloc[idx]['course_name'])
            st.write(df.iloc[idx]['Course URL'])
        

def logout():
    st.session_state["authenticated"] = False
    st.session_state["username"] = None



def main():
    """
    Streamlit app for user registration and login with navigation
    """

    # Navigation bar using Streamlit experimental features
    # if st._experimental_show_sidebar:
    #     st.sidebar.markdown("## Navigation")
    #     selected_page = st.sidebar.selectbox("Select page", ["Login", "Register"])

    # if selected_page == "Login":
    #     st.session_state["page"] = "login"
    # elif selected_page == "Register":
    #     st.session_state["page"] = "register"

    # Display login or register page based on session state
    if st.session_state["page"] == "login":
        login_page()
    if st.session_state["page"]=="register":
        register_page()
    if st.session_state["page"]=="page2":
        page2()
    if st.session_state["page"]=="courses":
        courses()
    
if __name__ == "__main__":
    create_navigation_bar() 
    main()
    