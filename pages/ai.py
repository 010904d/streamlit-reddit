import streamlit as st
import google.generativeai as genai

# Configure Google AI Python SDK
genai.configure(api_key="AIzaSyCBh5rrB48seOouSD9GCWJVRxmS-VtgY6Q")

# Define generation configuration and safety settings
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

# Create the generative model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings=safety_settings,
    generation_config=generation_config,
)

# Start a chat session
chat_session = model.start_chat(history=[])

# Streamlit app
st.title("AI Chat")

# Text input for user input
user_input = st.text_input("You:", "")

# Send user input to the model and display response
if st.button("Send"):
    if user_input:
        response = chat_session.send_message(user_input)
        st.write("AI:", response.text)
        





