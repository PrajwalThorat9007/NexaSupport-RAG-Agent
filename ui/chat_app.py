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


# ui/chat_app.py — Bonus UC-2 Streamlit UI
# Engineer: E2 Barnam

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uuid
import streamlit as st
from agents.onboarding_bot import OnboardingBot

# ── Page config ───────────────────────────────────────────
st.set_page_config(
    page_title="NexaSupport Onboarding Assistant",
    page_icon="🤝",
    layout="centered"
)

# ── Custom styling ────────────────────────────────────────
st.markdown("""
    <style>
        .stChatMessage { border-radius: 12px; padding: 8px; }
        .stChatInputContainer { border-top: 1px solid #e0e0e0; padding-top: 10px; }
        .source-tag {
            background-color: #f0f4ff;
            border-left: 3px solid #4f8ef7;
            padding: 6px 10px;
            border-radius: 4px;
            font-size: 0.8em;
            color: #444;
            margin-top: 6px;
        }
    </style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────
st.title("🤝 NexaSupport Onboarding Assistant")
st.caption("Powered by LLaMA 3 · Groq Cloud · RAG")
st.divider()

# ── Session state init ────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "bot" not in st.session_state:
    with st.spinner("Loading assistant..."):
        st.session_state.bot = OnboardingBot()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "sources" not in st.session_state:
    st.session_state.sources = []

# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 💬 Session Info")
    st.caption(f"Session ID: `{st.session_state.session_id[:8]}...`")
    st.caption(f"Messages: {len(st.session_state.messages)}")

    st.divider()
    st.markdown("### 💡 Example Questions")
    examples = [
        "How do I connect my CRM to NexaSupport?",
        "How do I set up auto-tagging?",
        "What happens if CRM sync fails?",
        "How do I invite my team members?",
        "How do I configure ticket routing rules?",
        "What are the API rate limits?"
    ]
    for example in examples:
        if st.button(example, use_container_width=True):
            st.session_state.pending_input = example

    st.divider()
    if st.button("🔄 Reset Conversation", use_container_width=True):
        st.session_state.bot.reset()
        st.session_state.messages = []
        st.session_state.sources = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

# ── Render chat history ───────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("sources"):
            sources_text = " · ".join(
                s.split(":")[-1] for s in msg["sources"]
            )
            st.markdown(
                f'<div class="source-tag">📄 Sources: {sources_text}</div>',
                unsafe_allow_html=True
            )

# ── Handle example button clicks ─────────────────────────
if "pending_input" in st.session_state:
    user_input = st.session_state.pop("pending_input")
else:
    user_input = None

# ── Chat input ────────────────────────────────────────────
typed_input = st.chat_input("Ask an onboarding question...")
if typed_input:
    user_input = typed_input

# ── Process input ─────────────────────────────────────────
if user_input:
    # Show user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = st.session_state.bot.chat(user_input)

        answer = result["answer"]
        sources = result["sources"]

        st.markdown(answer)
        if sources:
            sources_text = " · ".join(
                s.split(":")[-1] for s in sources
            )
            st.markdown(
                f'<div class="source-tag">📄 Sources: {sources_text}</div>',
                unsafe_allow_html=True
            )

    # Save to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })