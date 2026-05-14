# chat_app.py  —  (Bonus) Streamlit UI for UC-2 Onboarding Bot
# Responsibility: Simple browser chat interface wired to POST /onboard.
# Owner: Engineer B (bonus task)
#
# TODO: Page config — st.set_page_config(title="NexaSupport Onboarding Assistant")
#
# TODO: Session state
#   - st.session_state.messages = []  (list of {"role", "content"})
#   - st.session_state.session_id = uuid4()
#
# TODO: Render chat history
#   - Loop st.session_state.messages, render with st.chat_message(role)
#
# TODO: Chat input
#   - user_input = st.chat_input("Ask an onboarding question...")
#   - On submit: POST to http://localhost:8000/onboard with session_id + user_message
#   - Append user + assistant messages to session state
#   - Show sources in st.caption below the answer
#
# Run with:  streamlit run ui/chat_app.py


import streamlit as st


def main():
    st.title("NexaSupport Onboarding Assistant")
    st.caption("Powered by LLaMA 3 · Groq Cloud")
    # TODO: implement chat UI


if __name__ == "__main__":
    main()
