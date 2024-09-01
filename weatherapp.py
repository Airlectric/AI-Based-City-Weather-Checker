from langchain_groq import ChatGroq
from langchain.agents import Tool
from langchain.tools.base import BaseTool
from langgraph.graph import Graph
import requests
import streamlit as sl

#AI Model


groq_api_key = sl.secrets["general"]["GROQ_API_KEY"]

model = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    groq_api_key=groq_api_key,
)


##Weather tool
class TomorrowIOWeatherTool(BaseTool):
    name = "tomorrow_io_weather"
    description = "Fetch weather forecasts from the Tomorrow.io API"

    def _run(self, location: str):
        url = "https://api.tomorrow.io/v4/timelines"
        querystring = {
            "location": location,
            "fields": ["temperature", "cloudCover"],
            "units": "imperial",
            "timesteps": "1d",
            "apikey": sl.secrets["general"]["TOMORROWDOTIO_API_KEY"]
        }
        response = requests.request("GET", url, params=querystring)
        return response.text

    async def _arun(self, location: str):
        return self._run(location)


## functions which serve as nodes
def get_req(state):
    messages = state['messages']
    user_input = messages[-1]
    complete_query ="Your task is to provide only the city name based on the user input only, Nothing more, just the city name mentioned. Following is the user query: " + user_input
    response = model.invoke(complete_query)
    state['messages'].append(response.content)
    return state

def findWeather(state):
    messages = state['messages']
    agent_response = messages[-1]
    weather = TomorrowIOWeatherTool()
    weather_data = weather.run(agent_response)
    state['messages'].append(weather_data)
    return state

def filter_res(state):
    messages = state['messages']
    user_input = messages[0]
    available_info = messages[-1]
    agent2_query = "Your task is to provide info concisely based on the user query and the available information from the internet and format it with creative emojis and well structured and vertical manner. \
                     following is the user query: " + user_input + "Available information: " + available_info
    response = model.invoke(agent2_query)
    return response.content

## Langraph initialization
workflow = Graph()

workflow.add_node('agent', get_req)
workflow.add_node('weather tool', findWeather)
workflow.add_node('responder', filter_res)

workflow.add_edge('agent', 'weather tool')
workflow.add_edge('weather tool', 'responder')

workflow.set_entry_point('agent')
workflow.set_finish_point('responder')

checkWeather = workflow.compile()


