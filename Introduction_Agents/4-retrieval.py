import json
import os
from openai import OpenAI
from pydantic import BaseModel, Field

# Client Connect with openai
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ----------------------------------------------------------------
# Step 1: Define the tools(Function) that we want to call
# ----------------------------------------------------------------
def search_kb(question: str):
    """
    Load the whole knowledge base from jsonfile.
    (This is mock function for demostration purpose. we don't search)
    """
    with open(b"Introduction_Agents\\know-db.json", "r") as f:
        return json.load(f)
    
# ----------------------------------------------------------------
# Step 2: Call the model with search_kb tool defined
# ----------------------------------------------------------------
tools = [
    {
        "type"  : "function",
        "function" : {
            "name" : "search_kb",
            "description" : "Get the answer to the user's question from the knowledge base.",
            "parameters": {
                "type": "object",
                "properties": {
                "question": {"type": "string"},
                },
                "required" : ["question"],
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
        {"role": "system", "content": "You are a helpful assistant that answers questions from the knowledge base about our e-commerce store."},
        {
            "role": "user",
            "content": "What is the return policy of this company?"
        },
    ]
completion = client.chat.completions.create(
    model="gpt-4o",  # 1st parameter
    messages=messages, # 2nd parameter
    tools = tools, # 3rd parameter
)

completion.model_dump()

# ----------------------------------------------------------------
# Step 4: Execute search_kb function
# ----------------------------------------------------------------
def call_function(name, args):
    if name == "search_kb":
        return search_kb(**args)
    
    
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
class KBResponse(BaseModel):
    answer: str = Field(description="The answer to the user's question.")
    source: int = Field(description="The record id of the answer.")

    
completion2 = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    response_format=KBResponse,
) 

# ----------------------------------------------------------------
# Step 6: Check the model response
# ----------------------------------------------------------------

final_response = completion2.choices[0].message.parsed
print(F"Answer :{final_response.answer}\nSource: {final_response.source}")

    