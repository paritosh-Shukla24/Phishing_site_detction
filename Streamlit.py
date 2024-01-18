# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1V3Ea_wb52FmVEF3z0zBkDAcgV4cT_d_K
"""

# app.py
#!pip install streamlit
#!pip install joblib
#!pip install pyngrok
from pyngrok import ngrok
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import tensorflow as tf
import pickle

# Load your trained model using pickle
with open('/content/Phishing.pkl', 'rb') as file:
    model = pickle.load(file)  # Load the model from the file

# Rest of your Streamlit app code...


# Create a Streamlit web app
st.title('Machine Learning Model Deployment with Streamlit')

# Add a text input for user input
st.header('Enter Input Features')
feature1 = st.number_input('Feature 1')
url=st.text_input('Enter a URL:', '')
url=[url]
tokenizer=tf.keras.preprocessing.text.Tokenizer(num_words=10000,oov_token='<OOV>')
NEW_URL_SEQ=tokenizer.texts_to_sequences(url)
new_url_padded=tf.keras.preprocessing.sequence.pad_sequences(NEW_URL_SEQ)



# Create a button to make predictions
if st.button('Make Prediction'):
    # Prepare user input as a DataFrame


    # Make predictions using the loaded model
    prediction = model.predict(new_url_padded)

    # Display the prediction
    st.subheader('Prediction')
    if prediction[0]>=0.5:
        print('phishing website{Probability:',prediction[0],')')
    else:
        print('Legitimate website{Probability:',prediction[0],')')
#public_url = ngrok.connect(port='8501')
!streamlit run /content/untitled1.ipynb --server.port 8501



# You can add more functionality, charts, or explanations as needed
