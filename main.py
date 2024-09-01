import streamlit as sl
import streamlit.components.v1 as com

from weatherapp import checkWeather 

def get_weather(user_input):
    input = {"messages": [user_input]}
    response = checkWeather.invoke(input)
    sl.session_state["response"] = response
    

with sl.container():
    col1, col2 = sl.columns([1,2])

    with col1:
        com.iframe("https://lottie.host/embed/27cd04af-f29d-4e64-91bd-b6e2040b8945/qWOrnKhKIy.json")
        

    with col2:
        sl.title('Global City Weather Checker')
        

sl.markdown("---")

with sl.form(key='weather_form', clear_on_submit=True):
    user_input=sl.text_input('Enter prompt to obtain weather information about a City', max_chars=60,key='user_input')
    submit_button = sl.form_submit_button(label='Get Weather')

    

if submit_button:
    response_message = get_weather(user_input)

    sl.markdown("<h3 style='color: #4CAF50;'>🌤️ Weather Information</h3>", unsafe_allow_html=True) 
    sl.markdown(f"""
        <div style='padding: 15px; border: 2px solid #4CAF50; border-radius: 10px;'>
            <p style='font-size: 18px; ;'><strong>{sl.session_state['response']}</strong></p>
        </div>
    """, unsafe_allow_html=True)


