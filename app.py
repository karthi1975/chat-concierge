import streamlit as st
import time

# Function to simulate conversation with timing for video capture
def simulate_conversation(conversation_steps, delay=2):
    for step in conversation_steps:
        if step['speaker'] == "Guest":
            st.markdown(f'<div style="text-align: left; margin: 10px; padding: 10px; border-radius: 10px; background-color: #e0e0e0;">'
                        f'<strong>{step["speaker"]}</strong>: {step["message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="text-align: right; margin: 10px; padding: 10px; border-radius: 10px; background-color: #6c63ff; color: white;">'
                        f'<strong>{step["speaker"]}</strong>: {step["message"]}</div>', unsafe_allow_html=True)
        time.sleep(delay)  # Delay between messages to allow for video capture

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
            {"speaker": "AI", "message": "Stop me as I list the 5 Italian restaurants. Bona Vita 3 miles from here closes at 9pm..."},
            {"speaker": "AI", "message": "Can I text you the phone number and directions?"}
        ]
    },
    {
        "conversation": [
            {"speaker": "Guest", "message": "Hey Bill, What amenities does the hotel have?"},
            {"speaker": "AI", "message": "The hotel has an outdoor pool, a 200 sq. ft. exercise gym, a conference center, a restaurant, bar, shuttle service to the airport, and a business lounge."},
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
        simulate_conversation(current_scenario["conversation"], delay=2)
        
        # Move to the next scenario after a short delay
        time.sleep(2)
        st.session_state.scenario_index += 1
        
        # Re-run the function to automatically move to the next scenario
        play_scenarios()
    else:
        st.write('<div style="text-align: center; font-size: 1.5em; color: green;">Presentation complete.</div>', unsafe_allow_html=True)

# Start playing scenarios
st.title("Chat Concierge - Hotel Assistant")
play_scenarios()
