# Requirements: OpenAI Python SDK
import os
from openai import OpenAI

# 1st line
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# 2nd line
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role" : "user",
            "content" : "Who won the world series in 2020?"
        },
    ],
)

# 3rd line
response = completion.choices[0].message.content
print(response)