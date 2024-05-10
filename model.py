#!/usr/bin/env python
# coding: utf-8

# In[85]:


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
print('Dependencies Imported')


# In[86]:


data = pd.read_csv("/Users/saikeerthana/Downloads/Coursera.csv")
data.head(5)


# In[87]:


data.shape


# In[88]:


data.isnull().sum() #no value is missing


# In[89]:


data['Difficulty Level'].value_counts()


# In[8]:


data['Course Rating'].value_counts()


# In[90]:


data['University'].value_counts()


# In[91]:


data['Course Name']


# In[92]:


data = data[['Course Name','Difficulty Level','Course Description','Skills','Course URL']]


# In[93]:


data.head(5)


# In[94]:


# DATA PREPROCESSING
# Removing spaces between the words (Lambda funtions can be used as well)

data['Course Name'] = data['Course Name'].str.replace(' ',',')
data['Course Name'] = data['Course Name'].str.replace(',,',',')
data['Course Name'] = data['Course Name'].str.replace(':','')
data['Course Description'] = data['Course Description'].str.replace(' ',',')
data['Course Description'] = data['Course Description'].str.replace(',,',',')
data['Course Description'] = data['Course Description'].str.replace('_','')
data['Course Description'] = data['Course Description'].str.replace(':','')
data['Course Description'] = data['Course Description'].str.replace('(','')
data['Course Description'] = data['Course Description'].str.replace(')','')

#removing paranthesis from skills columns 
data['Skills'] = data['Skills'].str.replace('(','')
data['Skills'] = data['Skills'].str.replace(')','')


# In[95]:


data.head(5)


# In[98]:


data['tags'] = data['Course Name'] + data['Difficulty Level'] + data['Course Description'] + data['Skills']


# In[99]:


data.head(5)


# In[100]:


data['tags'].iloc[1]


# In[126]:


new_df = data[['Course Name','tags','Course URL']]


# In[127]:


new_df.head(5)


# In[128]:


new_df['tags'] = data['tags'].str.replace(',',' ')


# In[129]:


new_df['Course Name'] = data['Course Name'].str.replace(',',' ')


# In[130]:


new_df.rename(columns = {'Course Name':'course_name'}, inplace = True)


# In[131]:


new_df['tags'] = new_df['tags'].apply(lambda x:x.lower()) #lower casing the tags column


# In[132]:


new_df.head(5)


# In[108]:


new_df.shape


# TEXT VECTORIZATION
# 

# In[133]:


from sklearn.feature_extraction.text import CountVectorizer


# In[134]:


cv = CountVectorizer(max_features=5000,stop_words='english')


# In[135]:


vectors = cv.fit_transform(new_df['tags']).toarray()


# STEMMING PROCESS

# In[136]:


import nltk #natural language toolkit


# In[137]:


from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()


# In[138]:


#defining the stemming function
def stem(text):
    y=[]
    
    for i in text.split():
        y.append(ps.stem(i))
    
    return " ".join(y)


# In[139]:


new_df['tags'] = new_df['tags'].apply(stem) #applying stemming on the tags column


# SIMINLARITY MEASURE

# In[173]:


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
    user_profile += ''.join(user_interests)
if user_education:
    user_profile += ' ' + ''.join(user_education)
print(user_profile)

# Combine user interests and education into a single string
# user_profile = ' '.join(user_interests) + ' ' + ' '.join(user_education)

# Now you can continue with transforming user profile and course tags into vectors, and calculating cosine similarity.


# In[175]:


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def predict(username):
    uname = username
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
    combined_text = list(new_df['tags'])
    combined_text.append(user_profile)

    # Initialize CountVectorizer and fit on the combined text
    cv = CountVectorizer(max_features=6000, stop_words='english')
    vectors = cv.fit_transform(combined_text)

    # Get the index of the user profile in the vectors
    user_profile_index = len(combined_text) - 1
    # print(user_profile_index)
    # Calculate cosine similarity between user profile and course tags
    user_course_similarity = cosine_similarity(vectors[user_profile_index], vectors[:-1])
    # print(user_course_similarity)
    # Get indices of courses sorted by similarity
    sorted_indices = np.argsort(user_course_similarity[0])[::-1]
    # print(sorted_indices)
    # print(sorted_indices)
    # Print recommended courses
    return new_df,sorted_indices

# In[167]:


import pickle


# In[168]:



# In[169]:


# from IPython.display import FileLink

# # Assuming you've already saved the pickle files
# display(FileLink('similarity.pkl'))  # Clicking on this link will download the file
# display(FileLink('course_list.pkl'))  # Clicking on this link will download the file
# display(FileLink('courses.pkl'))  # Clicking on this link will download the file


# In[ ]:




