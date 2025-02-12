import json
import os

import requests
from openai import OpenAI
from pydantic import BaseModel, Field

# Client Connect with openai
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ----------------------------------------------------------------
# Step 1: Define the tools(Function) that we want to call
# ----------------------------------------------------------------

def get_weather(latitude, longitude):
    """
    This is a publically available API that returns the weather for a given location
    """
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
        )
    data = response.json()
    # print("data:\n",data)
    return data["current"]

# ----------------------------------------------------------------
# Step 2: Call the model with get_weather tool defined
# ----------------------------------------------------------------
tools = [
    {
        "type"  : "function",
        "function" : {
            "name" : "get_weather",
            "description" : "Get current temprature for provided coordinates in celsius",
            "parameters": {
                "type": "object",
                "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"}
                },
                "required" : ["latitude","longitude"],
                "additionalProperties": False,
            },
            "strict" : True,
        },
            
    }
]

# ----------------------------------------------------------------
# Step 3: Call the model
# ----------------------------------------------------------------
messages=[     
        {"role": "system", "content": "You are a helpful weather assistant."},
        {
            "role": "user",
            "content": "What's weather like in Surat today?"
        },
    ]
completion = client.beta.chat.completions.parse(
    model="gpt-4o",  # 1st parameter
    messages=messages, # 2nd parameter
    tools = tools, # 3rd parameter
)

completion.model_dump()

# ----------------------------------------------------------------
# Step 4: Execute get_weather function
# ----------------------------------------------------------------
def call_function(name, args):
    if name == "get_weather":
        return get_weather(**args)
    
    
for tool_call in completion.choices[0].message.tool_calls:
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    messages.append(completion.choices[0].message)
    result = call_function(name, args)
    messages.append(
        {
            "role" : "tool",
            "tool_call_id": tool_call.id,
            "content" : json.dumps(result)
        }
    )
    
# ----------------------------------------------------------------
# Step 5: Supply result and call model again
# ----------------------------------------------------------------
class WeatherResponse(BaseModel):
    temperature: float = Field(description="The current temperature in celsius for the given location")
    response: str = Field(description="A natural language response to the user's question")

    
completion2 = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    response_format=WeatherResponse,
) 

# ----------------------------------------------------------------
# Step 6: Check the model response
# ----------------------------------------------------------------

final_response = completion2.choices[0].message.parsed
print(F"Temperature :{final_response.temperature}°C\nResponse: {final_response.response}")