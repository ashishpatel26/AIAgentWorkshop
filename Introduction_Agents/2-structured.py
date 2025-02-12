# Requirements
import os
from openai import OpenAI
from pydantic import BaseModel

# Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ----------------------------------------------------------------
# Step 1 :  Define the response format in a Pydantic model
# ----------------------------------------------------------------

class CalenderEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


# ----------------------------------------------------------------
# Step 2: Call the Models
# ----------------------------------------------------------------
completion = client.beta.chat.completions.parse(
    model="gpt-4o",  # 1st parameter
    messages=[      # 2nd parameter
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Ashish and Shaishav are going to a science fair on Friday."
        },
    ],
    response_format=CalenderEvent,
)


# ----------------------------------------------------------------
# Step 3: Parse the response
# ----------------------------------------------------------------
event = completion.choices[0].message.parsed
print(event.name)
print(event.date)
print(event.participants)
