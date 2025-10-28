import streamlit as st
import openai

st.set_page_config(page_title="AI Chatbot 💬", page_icon="🤖")

st.title("🤖 AI Chatbot App")
st.write("Talk to your AI assistant below:")

# Input OpenAI API key
api_key = st.text_input("Enter your OpenAI API Key:", type="password")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input box
if prompt := st.chat_input("Type your message here..."):
    if not api_key:
        st.warning("⚠️ Please enter your OpenAI API key first!")
    else:
        # Append user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant response
        try:
            openai.api_key = api_key
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            reply = response["choices"][0]["message"]["content"]

            # Display assistant message
            with st.chat_message("assistant"):
                st.markdown(reply)

            # Append to chat history
            st.session_state.messages.append({"role": "assistant", "content": reply})

        except Exception as e:
            st.error(f"Error: {e}")
