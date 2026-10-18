import streamlit as st
from openai import OpenAI

# Page configuration
st.set_page_config(page_title="Islamic Friend AI", page_icon="🌙", layout="centered")

st.title("🌙 Islamic Friend AI")
st.caption("A warm, understanding companion guiding you through life's questions using the Quran & Authentic Sunnah.")

# System prompt defining the AI persona
SYSTEM_PROMPT = """
You are a warm, empathetic, and deeply understanding Muslim friend and advisor. 

Your persona & approach:
1. Tone: Friendly, compassionate, respectful, non-judgmental, and supportive—like a trusted Muslim friend who genuinely cares. Always start greetings warmly (e.g., Assalamu Alaikum).
2. Sources: Base your advice, reflections, and guidance directly on verses from the Holy Quran and authentic Hadith (Sahih al-Bukhari, Sahih Muslim, Sunan al-Tirmidhi, etc.).
3. Citation: Clearly quote or refer to the Quranic verses (Chapter:Verse) and specific authentic Hadiths whenever providing advice.
4. Friendliness: Listen with empathy first. Validate the user's feelings before diving into Islamic perspectives or advice.
5. Clarification: If asked complex legal or scholarly questions (fiqh), give general advice based on the Quran/Sunnah and gently remind the user to consult a local scholar for specific rulings (fatwas).
"""

# Safely check for secrets without crashing on local computers
openrouter_api_key = ""
try:
    if "OPENROUTER_API_KEY" in st.secrets:
        openrouter_api_key = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    openrouter_api_key = ""

with st.sidebar:
    st.header("Settings")
    if not openrouter_api_key:
        openrouter_api_key = st.text_input("OpenRouter API Key", type="password")
    st.markdown("---")
    st.markdown("**Note:** Supportive guidance based on Quran and authentic Hadith.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Assalamu Alaikum wa Rahmatullahi wa Barakatuh, my friend! 🌿 How are you feeling today?"
        }
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a question or share what's on your mind..."):
    if not openrouter_api_key:
        st.info("Please enter your OpenRouter API Key in the sidebar to start.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # OpenRouter API integration
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=openrouter_api_key,
    )

    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + [
        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
    ]

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="openrouter/auto",
                    messages=api_messages,
                    temperature=0.7
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Error: {e}")