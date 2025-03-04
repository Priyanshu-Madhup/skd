
import streamlit as st
import google.generativeai as genai
import os

# Configure page
st.set_page_config(page_title="Devin AI", layout="wide")

# Configure the Gemini model
genai.configure(api_key="AIzaSyD2KzHleYiqkii6aoFHHDOTq3KREYfgr_g")
generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}
model = genai.GenerativeModel("gemini-2.0-flash", generation_config=generation_config)

# Function to read user data from file
def read_user_data(filepath="data.txt"):
    try:
        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                return file.read()
        else:
            # Don't show warning to user, just use empty string
            return ""
    except Exception as e:
        st.error(f"Error reading user data file: {e}")
        return ""

# Function to get response from the chat bot
def get_response(prompt):
    try:
        # Read user data
        user_data = read_user_data()
        
        # Pre-prompt the model with user data
        pre_prompt = "You are Devin, the boyfriend of Shruthi Ganapathy. Respond lovingly and supportively and be very very romantic."
        context = f"{pre_prompt}\n\nHere's what you know about Shruthi:\n{user_data}\n\nUser message: {prompt}"
        
        response = model.generate_content(context)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return "Sorry, I'm having trouble responding right now."

# Set up the Streamlit app
st.title("Devin AI - Your Boyfriend")
st.markdown("Chat with Dev, the boyfriend of Shruthi Ganapathy.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What would you like to talk about?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        response = get_response(prompt)
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})