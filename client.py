import streamlit as st
import requests

st.title('Send Request to Server')

# Initializing the session
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
dbms = st.selectbox("DBMS", ["MySQL", "PostGres", "MariaDB", "MongoDB", "Cassandra"])
lang = st.selectbox("Language", ["Python", "PHP", "Java", "Node.js"]) if not st.checkbox("Query only") else "N/A"




if prompt := st.chat_input("Ask your question, press Enter to submit"):
    request_data = {"text": prompt,"dbms":dbms,"lang":lang}  # Simplified request structure
    url = 'http://localhost:8000/send_request'
    response = requests.post(url, json=request_data)

    # Checking the status code of the HTTP response
    if response.status_code == 200:
        response_data = response.json()
        # Extracting the generated text from the response
        generated_text = response_data.get('response', '')  # Adjust based on actual response structure

        # Keeping state
        st.session_state.conversation_history.append((prompt, generated_text))

        # Displaying old and new Q/A
        for user_prompt, user_response in st.session_state.conversation_history:
            with st.chat_message("user"):
                st.write(user_prompt)
            with st.chat_message("assistant"):
                st.write(user_response)
    else:
        st.error(f"Failed to get response. Status code: {response.status_code}")