import streamlit as st

from chatbot import Chatbot
from config import HF_MODEL, AVATAR_URL


# This must be the first Streamlit command.
st.set_page_config(
    page_title="Hugging Face Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Custom CSS adds visual styling that is not available
# through the standard Streamlit theme alone.
st.markdown(
    """
    <style>
        :root {
            --bg: #07111f;
            --bg-soft: #0d1b2a;
            --panel: rgba(15, 23, 42, 0.78);
            --panel-strong: rgba(17, 24, 39, 0.95);
            --card: rgba(15, 23, 42, 0.9);
            --line: rgba(148, 163, 184, 0.25);
            --ink: #e2e8f0;
            --muted: #a5b4cf;
            --blue: #60a5fa;
            --cyan: #22d3ee;
            --purple: #8b5cf6;
            --glow: rgba(96, 165, 250, 0.28);
        }

        html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], section.main {
            background:
                radial-gradient(circle at top left, rgba(96, 165, 250, 0.22), transparent 32%),
                radial-gradient(circle at bottom right, rgba(34, 211, 238, 0.18), transparent 30%),
                linear-gradient(135deg, var(--bg) 0%, #0b1324 100%) !important;
            color: var(--ink) !important;
        }

        .block-container {
            max-width: 1100px;
            padding-top: 2rem;
            padding-bottom: 6rem;
        }

        .hero {
            position: relative;
            padding: 2rem 2.2rem;
            margin-bottom: 1.6rem;
            border: 1px solid var(--line);
            border-radius: 28px;
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.94), rgba(15, 23, 42, 0.75)) !important;
            box-shadow: 0 22px 50px rgba(15, 23, 42, 0.45);
            overflow: hidden;
        }

        .hero::before {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, rgba(96, 165, 250, 0.18), rgba(139, 92, 246, 0.12));
            pointer-events: none;
        }

        .hero > * {
            position: relative;
            z-index: 1;
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            padding: 0.42rem 0.8rem;
            margin-bottom: 0.9rem;
            color: #dbeafe;
            background: rgba(96, 165, 250, 0.12);
            border: 1px solid rgba(96, 165, 250, 0.4);
            border-radius: 999px;
            font-size: 0.73rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .hero h1 {
            margin: 0;
            color: #f8fbff !important;
            font-size: clamp(2.2rem, 5vw, 4rem);
            letter-spacing: -0.06em;
            line-height: 1.05;
        }

        .hero p {
            max-width: 700px;
            margin: 0.9rem 0 0;
            color: var(--muted) !important;
            font-size: 1.04rem;
            line-height: 1.7;
        }

        .empty-state {
            padding: 1.3rem 1.2rem;
            margin: 1rem 0 1.3rem;
            text-align: center;
            color: var(--muted) !important;
            border: 1px dashed rgba(148, 163, 184, 0.4);
            border-radius: 18px;
            background: rgba(15, 23, 42, 0.55) !important;
        }

        [data-testid="stChatMessage"] {
            padding: 1.05rem 1.1rem !important;
            margin: 0.7rem 0;
            border: 1px solid var(--line) !important;
            border-radius: 20px !important;
            background: rgba(15, 23, 42, 0.78) !important;
            color: var(--ink) !important;
            box-shadow: 0 12px 28px rgba(2, 6, 23, 0.18);
        }

        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] span,
        [data-testid="stChatMessage"] li,
        [data-testid="stChatMessage"] code,
        [data-testid="stChatMessage"] div {
            color: var(--ink) !important;
        }

        [data-testid="stChatMessage"] a {
            color: #93c5fd !important;
            font-weight: 600;
        }

        [data-testid="stChatMessage"] pre {
            background: rgba(15, 23, 42, 0.9) !important;
            border: 1px solid rgba(148, 163, 184, 0.15);
            border-radius: 14px;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(4, 10, 19, 0.96), rgba(15, 23, 42, 0.94)) !important;
            border-right: 1px solid rgba(148, 163, 184, 0.15) !important;
        }

        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] h4,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] div {
            color: var(--ink) !important;
        }

        [data-testid="stSidebar"] .stMetric {
            background: rgba(96, 165, 250, 0.08);
            border: 1px solid rgba(96, 165, 250, 0.2);
            border-radius: 16px;
            padding: 0.6rem 0.8rem;
        }

        [data-testid="stChatInput"] {
            background: rgba(15, 23, 42, 0.88) !important;
            border: 1px solid rgba(96, 165, 250, 0.6) !important;
            border-radius: 18px !important;
            box-shadow: 0 0 0 1px rgba(96, 165, 250, 0.15), 0 16px 35px rgba(15, 23, 42, 0.25);
        }

        [data-testid="stChatInput"]:focus-within {
            border-color: rgba(34, 211, 238, 0.9) !important;
            box-shadow: 0 0 0 3px rgba(34, 211, 238, 0.18);
        }

        [data-testid="stChatInput"] textarea {
            color: var(--ink) !important;
            background: transparent !important;
        }

        [data-testid="stBottom"] {
            background: transparent !important;
        }

        .stButton > button {
            border: 1px solid rgba(96, 165, 250, 0.4);
            background: linear-gradient(135deg, rgba(96, 165, 250, 0.18), rgba(139, 92, 246, 0.18));
            color: #e0f2fe;
            border-radius: 12px;
            font-weight: 600;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 18px rgba(96, 165, 250, 0.12);
        }

        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #2563eb, #7c3aed) !important;
            border: none !important;
            color: white !important;
        }

        .stCodeBlock {
            border-radius: 12px;
        }

        @media (max-width: 640px) {
            .hero {
                padding: 1.4rem 1.1rem;
                border-radius: 20px;
            }

            .block-container {
                padding-top: 1rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

def initialize_chatbot() -> None:
    """
    Create the chatbot only once for the current browser session.

    Streamlit reruns this file after every interaction.
    Session State prevents a new Chatbot from being created
    during each rerun.
    """
    if "bot" not in st.session_state:
        st.session_state.bot = Chatbot()


def clear_conversation() -> None:
    """Remove previous messages but keep the chatbot available."""
    st.session_state.bot.reset()


# Create or retrieve the chatbot stored in Session State.
initialize_chatbot()


# Sidebar
with st.sidebar:
    st.markdown("## 🤖 Hugging Face Agent")

    st.caption(
        "An intelligent assistant for quick answers, coding help, and web research."
    )

    st.divider()

    st.markdown("#### Active model")
    st.code(HF_MODEL, language=None)

    st.markdown("#### Available tools")
    st.success("DuckDuckGo web search enabled", icon="🔎")

    st.markdown("#### Conversation")
    message_count = max(
        len(st.session_state.bot.messages) - 1,
        0,
    )
    st.metric("Messages", message_count)

    if st.button(
        "＋ Start new chat",
        use_container_width=True,
        type="primary",
    ):
        clear_conversation()
        st.rerun()

    st.divider()

    st.caption(
        "Conversation history currently lasts only for this "
        "browser session. Permanent memory can be added later."
    )


# Main header
st.markdown(
    """
    <section class="hero">
        <span class="hero-badge">AI Assistant</span>
        <h1>Ask anything. Build faster.</h1>
        <p>
            Your smart assistant is ready to answer questions, generate ideas,
            explain code, and search the web for the latest information.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)


# Do not display the system prompt in the interface.
visible_messages = [
    message
    for message in st.session_state.bot.messages
    if message["role"] != "system"
]


# Show an introduction and example prompts before the first message.
if not visible_messages:
    st.markdown(
        """
        <div class="empty-state">
            Begin by writing a message below or selecting
            one of these example prompts.
        </div>
        """,
        unsafe_allow_html=True,
    )

    suggestions = [
        (
            "🐍 Explain Python",
            "Explain Python functions to a beginner with an example.",
        ),
        (
            "💡 Brainstorm",
            "Give me five useful AI project ideas for beginners.",
        ),
        (
            "✍️ Improve writing",
            "Help me write a professional project introduction.",
        ),
    ]

    suggestion_columns = st.columns(len(suggestions))

    for column, (label, suggestion) in zip(
        suggestion_columns,
        suggestions,
    ):
        with column:
            if st.button(label, use_container_width=True):
                st.session_state.pending_prompt = suggestion
                st.rerun()


# Display existing conversation messages.
for message in visible_messages:
    avatar = "🧑‍💻" if message["role"] == "user" else (AVATAR_URL or "✨")

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])


# Display the message input at the bottom of the page.
prompt = st.chat_input(
    "Message your AI assistant...",
    max_chars=4000,
)


# Use a suggestion as the prompt when a suggestion button is clicked.
if not prompt and "pending_prompt" in st.session_state:
    prompt = st.session_state.pop("pending_prompt")


# Process a new message.
if prompt:
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=(AVATAR_URL or "✨")):
        with st.spinner("Thinking..."):
            try:
                answer = st.session_state.bot.reply(prompt)
            except Exception as error:
                st.error(f"Request failed: {error}")
            else:
                st.markdown(answer)