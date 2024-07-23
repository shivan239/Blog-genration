2import streamlit as st
import requests
import json

# Replace with your Hugging Face API token
HF_API_TOKEN = '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'

# API URL for GPT-2 Medium model
API_URL = "https://api-inference.huggingface.co/models/gpt2-medium"

def generate_text(input_text, no_words, blog_style):
    try:
        # Construct the prompt
        prompt = f"Write a blog post for {blog_style} about the topic '{input_text}' within {no_words} words. Make sure the content is informative, engaging, and suitable for general readers."

        # Prepare headers and payload
        headers = {
            "Authorization": f"Bearer {HF_API_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": int(no_words),
                "temperature": 0.9,
                "repetition_penalty": 2.0,
                "top_k": 50,
                "top_p": 0.95
            }
        }

        # Make the API request
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Extract generated text
        response_json = response.json()
        if isinstance(response_json, list) and 'generated_text' in response_json[0]:
            generated_text = response_json[0]['generated_text']
        else:
            generated_text = response_json.get('generated_text', 'No text generated')
        
        return generated_text, response.elapsed.total_seconds()

    except requests.exceptions.RequestException as e:
        return f"Error generating response: {e}", 0

# Streamlit app setup
st.set_page_config(page_title="Generate Blogs", page_icon=' ', layout='centered', initial_sidebar_state='collapsed')

# Streamlit app UI
st.header('Generate Blogs')

input_text = st.text_input("Enter the blog topic", placeholder="Type your blog topic here")

col1, col2 = st.columns([5, 5])
with col1:
    no_words = st.text_input("No. of words", placeholder="Enter the number of words")

with col2:
    blog_style = st.selectbox("Writing the blog for", ('Researchers', 'Data Scientist', 'Common People'), index=0)

submit = st.button('Generate Blog')

if submit:
    if input_text and no_words.isdigit():
        response, generation_time = generate_text(input_text, no_words, blog_style)
        st.write(response)
        st.write(f"Generation Time: {generation_time:.2f} seconds")
    else:
        st.write("Please fill in all the fields correctly.")
