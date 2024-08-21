import streamlit as st
import time
import json
from google.cloud import texttospeech
import base64
from io import BytesIO
import tempfile
import os

# Decode the environment variable to get the JSON credentials
json_key_base64 = os.getenv('GOOGLE_CLOUD_CREDENTIALS')
json_key_content = base64.b64decode(json_key_base64).decode('utf-8')

# Use the credentials to create a temporary JSON file
with BytesIO(json_key_content.encode()) as json_key_file:
    client = texttospeech.TextToSpeechClient.from_service_account_info(json.load(json_key_file))

# Function to generate and play voice from text using Google TTS
def text_to_speech(text, speaker):
    if speaker == "Guest":
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-GB", name="en-GB-Wavenet-C"  # Female British English voice
        )
    else:
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", name="en-US-Wavenet-D"  # Male American English voice
        )

    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    synthesis_input = texttospeech.SynthesisInput(text=text)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Save the audio content to a temporary file and determine the duration
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
        temp_audio_file.write(response.audio_content)
        temp_audio_file_path = temp_audio_file.name

    # Play the audio in the Streamlit app
    audio_base64 = base64.b64encode(response.audio_content).decode()
    st.markdown(f'''
        <audio autoplay>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
    ''', unsafe_allow_html=True)

    # Calculate the duration of the audio in seconds
    from mutagen.mp3 import MP3
    audio_duration = MP3(temp_audio_file_path).info.length
    
    # Clean up the temporary audio file
    os.remove(temp_audio_file_path)

    return audio_duration

# Function to simulate conversation with timing for video capture
def simulate_conversation(conversation_steps):
    for step in conversation_steps:
        if step['speaker'] == "Guest":
            st.markdown(f'<div style="text-align: left; margin: 10px; padding: 10px; border-radius: 10px; background-color: #e0e0e0;">'
                        f'<strong>{step["speaker"]}</strong>: {step["message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="text-align: right; margin: 10px; padding: 10px; border-radius: 10px; background-color: #6c63ff; color: white;">'
                        f'<strong>{step["speaker"]}</strong>: {step["message"]}</div>', unsafe_allow_html=True)
        
        # Generate and play the corresponding audio, and get its duration
        audio_duration = text_to_speech(step["message"], step["speaker"])
        
        # Pause for the duration of the audio plus an additional delay
        time.sleep(audio_duration + 1)

# Initialize session state to control the presentation loop
if 'scenario_index' not in st.session_state:
    st.session_state.scenario_index = 0

# Scenarios to play in sequence for video capture
scenarios = [
    {
        "conversation": [
            {"speaker": "Guest", "message": "Hey Bill, Is there a good place to eat around here?"},
            {"speaker": "AI", "message": "There are 26 restaurants within 5 miles of the hotel. Do you have a preferred food type?"},
            {"speaker": "Guest", "message": "How about Italian."},
            {"speaker": "AI", "message": "You can stop me as I list the 5 Italian restaurants. Bona Vita 3 miles from here closes at 9pm..."},
            {"speaker": "AI", "message": "Can I text you the phone number and directions?"}
        ]
    },
    {
        "conversation": [
            {"speaker": "Guest", "message": "Hey Bill, What amenities does the hotel have?"},
            {"speaker": "AI", "message": "The hotel has an outdoor pool, a 200 square foot exercise gym, a conference center, a restaurant, bar, shuttle service to the airport, and a business lounge."},
            {"speaker": "AI", "message": "Can I text you the details of any of these services?"}
        ]
    },
    {
        "conversation": [
            {"speaker": "Guest", "message": "Hey Bill, Please order me food room service."},
            {"speaker": "AI", "message": "I have put the menu on your television. Let me know when you are ready with your food order."},
            {"speaker": "AI", "message": "Would you like any special dietary options?"}
        ]
    },
    {
        "conversation": [
            {"speaker": "Guest", "message": "Hey Bill, Give me a wakeup call at 7:30am."},
            {"speaker": "AI", "message": "I have set your wake up call for tomorrow Thursday, September 5th at 7:30am."},
            {"speaker": "AI", "message": "Do you prefer an alarm sound, music, or weather and news?"}
        ]
    }
]

# Function to handle the sequential scenario playback
def play_scenarios():
    if st.session_state.scenario_index < len(scenarios):
        current_scenario = scenarios[st.session_state.scenario_index]
        
        # Play the conversation for the current scenario
        simulate_conversation(current_scenario["conversation"])
        
        # Move to the next scenario after a short delay
        st.session_state.scenario_index += 1
        
        # Re-run the function to automatically move to the next scenario
        play_scenarios()

# Streamlit UI
st.title("Chat Concierge - Hotel Assistant")

# Start button to initiate the chat sequence
if st.button("Start Chat"):
    play_scenarios()