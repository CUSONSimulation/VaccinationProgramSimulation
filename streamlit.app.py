import streamlit as st
import os
from openai import OpenAI
import anthropic
from io import BytesIO
import base64
from streamlit_mic_recorder import mic_recorder
from streamlit.runtime import get_instance
from streamlit.runtime.scriptrunner import get_script_run_ctx
import re
from docx import Document
import tomllib
import hmac
import warnings
import io
import logging
import uuid
import time
from datetime import datetime, timedelta


# Create a custom logger
def get_logger():
    log = logging.getLogger(__name__)
    if not log.hasHandlers():  # Avoid adding handlers multiple times
        log.setLevel(logging.INFO)
        file_handler = logging.FileHandler("log.txt", mode="a", encoding="utf-8")
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "{asctime}\t{levelname}\t{module}\t{threadName}\t{funcName}\t{lineno}\n{message}",
            style="{",
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        log.addHandler(file_handler)
        log.addHandler(console_handler)
    return log


if "logger" not in st.session_state:
    st.session_state.logger = get_logger()
log = st.session_state.logger

warnings.filterwarnings("ignore", category=DeprecationWarning)


def get_uuid():
    timestamp = time.time()
    id = uuid.uuid4()
    id = f"{id}-{timestamp}"
    id = base64.urlsafe_b64encode(id.encode("utf-8")).decode("utf-8")
    return id[:8]


def get_session():
    runtime = get_instance()
    ctx = get_script_run_ctx()
    session_id = ctx.session_id
    session_info = runtime._instance.get_client(session_id)
    return session_id


def elapsed(start):
    duration = time.time() - start
    duration_td = timedelta(seconds=duration)
    days = duration_td.days
    hours, remainder = divmod(duration_td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    dur_str = ""
    if days:
        dur_str = f"{days} days "
    if hours:
        dur_str += f"{hours} hours "
    if minutes:
        dur_str += f"{minutes} minutes "
    if seconds:
        dur_str += f"{seconds} seconds"
    return dur_str


def password_entered():
    """Checks whether a password entered by the user is correct."""
    if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
        st.session_state["password_correct"] = True
        del st.session_state["password"]  # Don't store the password.
        autoplay_audio(open("assets/unlock.mp3", "rb").read())
        log.info(f"Session Start: {get_session()}")
    else:
        st.session_state["password_correct"] = False


@st.cache_data
def load_settings():
    return tomllib.load(open("settings.toml", "rb"))


@st.cache_data
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def speech_to_text(client, audio):
    try:
        id = audio["id"]
        log.debug(f"STT: {id}")
        audio_bio = io.BytesIO(audio["bytes"])
        audio_bio.name = "audio.wav"
        transcript = client.audio.transcriptions.create(
            model="whisper-1", response_format="text", file=audio_bio
        )
        st.session_state.processed_audio = id
        return transcript
    except Exception as e:
        log.exception("")


def text_to_speech(client, text):
    try:
        log.debug(f"TTS: {text}")
        # Use the appropriate voice based on the current active agent
        current_voice = st.session_state.settings["sam"]["voice"] if st.session_state.sam_active else st.session_state.settings["noa"]["voice"]
        
        response = client.audio.speech.create(
            model="tts-1",
            voice=current_voice,
            input=text,
        )
        autoplay_audio(response.content)
    except Exception as e:
        log.exception("")


def autoplay_audio(audio_data):
    b64 = base64.b64encode(audio_data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)


# Send prompt to Anthropic and get response
def stream_response_anthropic(client, messages):
    try:
        log.debug(f"Sending text request to Anthropic: {messages[-1]['content']}")
        
        # Use the appropriate instruction based on which agent is active
        system_content = st.session_state.settings["sam_instruction"] if st.session_state.sam_active else st.session_state.settings["noa_instruction"]
        
        stream = client.messages.create(
            model=st.session_state.settings["parameters"]["model"],
            messages=messages[1:],
            max_tokens=1000,
            system=system_content,
            temperature=st.session_state.settings["parameters"]["temperature"],
            stream=True,
        )
        for chunk in stream:
            if isinstance(
                chunk,
                anthropic.types.raw_content_block_delta_event.RawContentBlockDeltaEvent,
            ):
                yield chunk.delta.text
    except Exception as e:
        log.exception("")


# Send prompt to OpenAI and get response
def stream_response_openai(client, messages):
    try:
        log.debug(f"Sending text request to OpenAI: {messages[-1]['content']}")
        
        # Get the correct system message based on which agent is active
        if st.session_state.sam_active:
            # If Sam is active, use Sam's instruction
            messages_to_send = [{"role": "system", "content": st.session_state.settings["sam_instruction"]}] + messages[1:]
        else:
            # Otherwise use Noa's instruction
            messages_to_send = [{"role": "system", "content": st.session_state.settings["noa_instruction"]}] + messages[1:]
        
        # Optimize for faster responses by setting max_tokens appropriately
        # This helps avoid unnecessary computation for very long responses
        # Adjust the max_tokens value based on your needs
        stream = client.chat.completions.create(
            model=st.session_state.settings["parameters"]["model"],
            messages=messages_to_send,
            temperature=st.session_state.settings["parameters"]["temperature"],
            stream=True,
            max_tokens=800,  # Limiting max tokens for faster responses
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
    except Exception as e:
        log.exception("")


def show_download():
    document = create_transcript_document()
    col1, col2 = st.columns([1, 1])
    # Button to download the full conversation transcript
    with col1:
        st.download_button(
            label="📥 Download Transcript",
            data=document,
            file_name="Transcript.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )


def create_transcript_document():
    doc = Document()
    doc.add_heading("Conversation Transcript\n", level=1)

    for message in st.session_state.messages[1:]:
        if message["role"] == "user":
            p = doc.add_paragraph()
            p.add_run(st.session_state.settings["user_name"] + ": ").bold = True
            p.add_run(message["content"])
        else:
            p = doc.add_paragraph()
            # Use the appropriate name based on which agent responded
            agent_name = st.session_state.settings["sam"]["name"] if message.get("agent") == "sam" else st.session_state.settings["noa"]["name"]
            p.add_run(agent_name + ": ").bold = True
            p.add_run(message["content"])

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer


# Session Initialization
def init_session():
    if "settings" not in st.session_state:
        st.session_state.settings = load_settings()
        defaults = {
            "show_intro": True,
            "chat_active": False,
            "messages": [
                {"role": "system", "content": st.session_state.settings["noa_instruction"]}
            ],
            "processed_audio": None,
            "manual_input": None,
            "end_session_button_clicked": False,
            "download_transcript": False,
            "start_time": time.time(),
            "sam_active": False,  # Start with Noa for pre-briefing
            "debrief_active": False,  # Flag for debriefing phase
        }
        for key, val in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = val


def setup_sidebar():
    # Determine which agent is active for the sidebar
    if st.session_state.sam_active:
        st.sidebar.header(f"Meeting with {st.session_state.settings['sam']['name']}")
        container1 = st.sidebar.container(border=True)
        with container1:
            st.image(st.session_state.settings['sam']['avatar'])
            st.subheader(f"Name: {st.session_state.settings['sidebar']['Sam_Name']}")
            st.subheader(f"Position: {st.session_state.settings['sidebar']['Sam_Position']}")
            st.subheader(f"Years in Position: {st.session_state.settings['sidebar']['Sam_Years_in_Position']}")
            st.subheader(f"Facility: {st.session_state.settings['sidebar']['Sam_Facility']}")
    else:
        st.sidebar.header(f"Session with {st.session_state.settings['noa']['name']}")
        container1 = st.sidebar.container(border=True)
        with container1:
            st.image(st.session_state.settings['noa']['avatar'])
            st.subheader(f"Name: {st.session_state.settings['sidebar']['Noa_Name']}")
            st.subheader(f"Position: {st.session_state.settings['sidebar']['Noa_Position']}")
            st.subheader(f"Institution: {st.session_state.settings['sidebar']['Noa_Institution']}")

    # Button Login
    if "password_correct" in st.session_state and st.session_state.password_correct:
        st.session_state.chat_active = True
        st.session_state.show_intro = False
    else:
        st.sidebar.header("Access Code")
        with st.sidebar.container(border=True):
            with st.form("Credentials"):
                st.text_input("Access Code", type="password", key="password")
                st.form_submit_button("Start Chat", on_click=password_entered)
            if "password_correct" in st.session_state:
                st.error("😕 Invalid Code")


def show_messages():
    for message in st.session_state.messages[1:]:
        if message["role"] == "user":
            name = st.session_state.settings["user_name"]
            avatar = st.session_state.settings["user_avatar"]
        else:
            # Determine which agent's info to use based on the message
            if message.get("agent") == "sam":
                name = st.session_state.settings["sam"]["name"]
                avatar = st.session_state.settings["sam"]["avatar"]
            else:
                name = st.session_state.settings["noa"]["name"]
                avatar = st.session_state.settings["noa"]["avatar"]
                
        with st.chat_message(name, avatar=avatar):
            st.markdown(message["content"])


def handle_audio_input(client):
    with st.sidebar.container(border=True):
        audio = mic_recorder(
            start_prompt="🎙 Record",
            stop_prompt="📤 Stop",
            just_once=False,
            use_container_width=True,
            format="wav",
            key="recorder",
        )
    # Check if there is a new audio recording and it has not been processed yet
    if audio and audio["id"] != st.session_state.processed_audio:
        transcript = speech_to_text(client, audio)
        return transcript


def process_user_query(text_client, speech_client, user_query):
    # Check for transition triggers
    
    # 1. Transition from Noa to Sam (pre-brief to simulation)
    if not st.session_state.sam_active and not st.session_state.debrief_active and re.search(r"meet with sam|talk to sam|ready to meet|start simulation|begin simulation", user_query.lower()):
        st.session_state.sam_active = True
    
    # 2. Transition from Sam to Noa (simulation to debrief)
    if st.session_state.sam_active and not st.session_state.debrief_active and re.search(r"ready for feedback|end session|finish|complete|goodbye", user_query.lower()):
        st.session_state.sam_active = False
        st.session_state.debrief_active = True
        st.session_state.end_session_button_clicked = True
        st.session_state.download_transcript = True
    
    # Display the user's query
    with st.chat_message(
        st.session_state.settings["user_name"],
        avatar=st.session_state.settings["user_avatar"],
    ):
        st.markdown(user_query)

    # Store the user's query into the history
    st.session_state.messages.append({"role": "user", "content": user_query.strip()})

    # Stream the assistant's reply
    # Determine which agent is responding
    current_agent = "sam" if st.session_state.sam_active else "noa"
    agent_name = st.session_state.settings["sam"]["name"] if st.session_state.sam_active else st.session_state.settings["noa"]["name"]
    agent_avatar = st.session_state.settings["sam"]["avatar"] if st.session_state.sam_active else st.session_state.settings["noa"]["avatar"]
    
    with st.chat_message(agent_name, avatar=agent_avatar):
        # Empty container to display the assistant's reply
        assistant_reply_box = st.empty()

        # A blank string to store the assistant's reply
        assistant_reply = ""

        # Iterate through the stream
        for chunk in (
            stream_response_openai(text_client, st.session_state.messages)
            if st.session_state.settings["parameters"]["model"].startswith("gpt")
            else stream_response_anthropic(text_client, st.session_state.messages)
        ):
            assistant_reply += chunk
            assistant_reply_box.markdown(assistant_reply)

        # Once the stream is over, update chat history with agent info
        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_reply.strip(), "agent": current_agent}
        )
        
        # Play audio response
        text_to_speech(speech_client, assistant_reply)


def main():
    # Inject CSS for custom styles
    local_css("style.css")

    init_session()
    text_client = (
        OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        if st.session_state.settings["parameters"]["model"].startswith("gpt")
        else anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    )
    speech_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    st.title(st.session_state.settings["title"])
    setup_sidebar()

    # Display text before Start Chat is pressed
    if st.session_state.show_intro:
        with st.container(border=True):
            st.markdown(st.session_state.settings["intro"])

    # Check if chat is active
    if st.session_state.chat_active:
        show_messages()

        # Check if there's a manual input and process it
        if st.session_state.manual_input:
            user_query = st.session_state.manual_input
        else:
            # Update placeholder text based on current agent
            if st.session_state.sam_active:
                placeholder_text = "Chat with Sam Richards about implementing the flu vaccination program..."
            elif st.session_state.debrief_active:
                placeholder_text = "Ask Noa questions about your feedback or the simulation..."
            else:
                placeholder_text = "Chat with Noa to prepare for your meeting with Sam..."
                
            user_query = st.chat_input(placeholder_text)
            transcript = handle_audio_input(speech_client)
            if transcript:
                user_query = transcript

        if user_query:
            process_user_query(text_client, speech_client, user_query)
            if st.session_state.manual_input:
                st.session_state.manual_input = None
                st.rerun()

        # Handle end session button - only show during Sam conversation
        if st.session_state.sam_active and not st.session_state.debrief_active:
            if st.button("End Session & Get Feedback"):
                st.session_state.sam_active = False
                st.session_state.debrief_active = True
                st.session_state.end_session_button_clicked = True
                st.session_state.download_transcript = True
                st.session_state["manual_input"] = "Ready for feedback on my conversation with Sam."
                # Trigger the manual input immediately
                st.rerun()

        # Show the download button during debrief
        if st.session_state.download_transcript:
            show_download()

    st.sidebar.warning(st.session_state.settings["warning"])


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        id = get_uuid()
        log.exception(f"Unhandled exception: {id}")
        st.error(
            f"{st.session_state.settings['error_message']}\n\n**Reference id: {id}**"
        )
