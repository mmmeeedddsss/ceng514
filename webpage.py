import streamlit as st
import time
import random

from predictor import Predictor

random.seed(41)

language = st.selectbox("Select Language", ["English", "Turkish"], index=0, placeholder="Choose an option", label_visibility="visible")
# Create text input for User question
user_question = st.text_input('Please enter your SQL question') 

# Create text input for Database ID
db_id = st.text_input('Please enter your DB ID') 

# Create a button that when pressed, will trigger an event
if st.button('Submit'):
    # Display the initial status
    status_text = st.empty()
    status_text.text('Loading...')
    
    # get the results from your user_prompt function
    with st.spinner("waiting"):
        print(f"Prediction for the language: {language}")
        p = Predictor(use_turkish=language == "Turkish")
        similar_questions = p.find_similar_items(user_question)
        expander = st.expander("SEE SIMILAR QUESTIONS")
        expander.write(similar_questions)
        result = p.user_prompt(user_question, db_id)

        # update the status
        status_text.text(result)

    # display the result 
