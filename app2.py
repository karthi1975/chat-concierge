import streamlit as st
import time
from gtts import gTTS
import base64
from io import BytesIO

# Function to generate and play voice from text
def text_to_speech(text, speaker):
    tts = gTTS(text=text, lang='en', tld='com')
    
    # Save the audio file to a BytesIO object
    with BytesIO() as audio:
        tts.write_to_fp(audio)
        audio.seek(0)
        audio_base64 = base64.b64encode(audio.read()).decode()
    
    # Return the audio player HTML code with autoplay and hidden controls
    return f'''
        <audio autoplay style="display:none;">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
    '''

# Sample conversation
conversation = [
    {"speaker": "Guest", "message": "Hey Bill, Is there a good place to eat around here?"},
    {"speaker": "AI", "message": "There are 26 restaurants within 5 miles of the hotel. Do you have a preferred food type?"},
    {"speaker": "Guest", "message": "How about Italian."},
    {"speaker": "AI", "message": "Stop me as I list the 5 Italian restaurants. Bona Vita 3 miles from here closes at 9pm..."},
]

# Display conversation and play audio
for step in conversation:
    st.markdown(f"**{step['speaker']}:** {step['message']}")
    st.markdown(text_to_speech(step["message"], step["speaker"]), unsafe_allow_html=True)
    time.sleep(2 + len(step["message"]) * 0.05)  # Adjust delay based on text length