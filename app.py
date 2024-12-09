import streamlit as st
import google.generativeai as ai
from datetime import datetime
import base64

# Configure the Generative AI
ai.configure(api_key="your_api_key")
model = ai.GenerativeModel('gemini-pro')

# Initialize chatbot and session state variables
if "chatbot" not in st.session_state:
    st.session_state.chatbot = model.start_chat(history=[])

if "history" not in st.session_state:
    st.session_state.history = []

if "theme" not in st.session_state:
    st.session_state.theme = "Light"

# Streamlit App Title
st.title("🤖 Welcome to SSG's Chatbot")

# Sidebar for user settings and options
with st.sidebar:
    st.header("Settings")
    theme = st.radio("Choose Theme:", ["Light", "Dark"])
    st.session_state.theme = theme
    
    if st.button("Clear Chat History"):
        st.session_state.history = []
        st.success("Chat history cleared!")

    if st.button("Download Chat History"):
        chat_text = "\n".join([f"[{role}] {content}" for role, content in st.session_state.history])
        b64 = base64.b64encode(chat_text.encode()).decode()
        href = f'<a href="data:text/plain;base64,{b64}" download="chat_history.txt">Download Chat History</a>'
        st.markdown(href, unsafe_allow_html=True)

    st.markdown("This AI chatbot is powered by **Shivam** and **Innomatics Research Lab**.")
    st.markdown("You can interact with the chatbot, give feedback, and even download the conversation!")

# Apply theme based on user selection
if st.session_state.theme == "Dark":
    st.markdown(
        """
        <style>
        body {
            background-color: #333;
            color: #FFF;
        }
        .stButton > button {
            background-color: #444;
            color: #FFF;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Helper function to display messages with timestamp on a new line
def display_message(role, content):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if role == "human":
        st.chat_message("human").write(content)
        st.markdown(f"<p style='font-size: 10px; color: grey;'>{timestamp}</p>", unsafe_allow_html=True)
    else:
        st.chat_message("ai").write(content)
        st.markdown(f"<p style='font-size: 10px; color: grey;'>{timestamp}</p>", unsafe_allow_html=True)

# Display conversation history
for role, content in st.session_state.history:
    display_message(role, content)

# Input for user prompt
user_prompt = st.chat_input("Type your message here...")

# Handle user input and AI response
if user_prompt:
    # Display user's message
    display_message("human", user_prompt)
    st.session_state.history.append(("human", user_prompt))
    
    # Generate AI response with a loading indicator
    with st.spinner("AI is thinking..."):
        try:
            response = st.session_state.chatbot.send_message(user_prompt)
            ai_response = response.text if response.text else "I'm not sure how to respond to that."
        except Exception as e:
            ai_response = f"An error occurred: {str(e)}"

    # Display AI's message
    display_message("ai", ai_response)
    st.session_state.history.append(("ai", ai_response))

    # Add emoji reactions
    st.markdown("React to the response:")
    cols = st.columns([1, 1, 1, 1])
    if cols[0].button("👍"):
        st.success("You liked this response!")
    if cols[1].button("👎"):
        st.warning("You disliked this response!")
    if cols[2].button("😂"):
        st.info("You found this response funny!")
    if cols[3].button("🤔"):
        st.info("This response made you think!")

    # Provide feedback option
    feedback = st.text_input("Give feedback on this response (optional):")
    if feedback:
        st.success("Thank you for your feedback!")
