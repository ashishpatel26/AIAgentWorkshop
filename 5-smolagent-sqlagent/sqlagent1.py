import os
import gradio as gr
from sqlalchemy import text
from smolagents import tool, CodeAgent, HfApiModel
import pandas as pd
from database import engine, receipts

# Function to fetch receipt data from the database
def get_receipts_table():
    try:
        with engine.connect() as con:
            result = con.execute(text("SELECT * FROM receipts"))
            rows = result.fetchall()

        if not rows:
            return pd.DataFrame(columns=["receipt_id", "customer_name", "price", "tip"])

        df = pd.DataFrame(rows, columns=["receipt_id", "customer_name", "price", "tip"])
        return df

    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]})  # Return error message in DataFrame format
    
def sanitize_query(query: str) -> str:
    """
    Sanitizes the query to ensure that values are properly quoted and formatted.
    Args:
        query (str): The raw SQL query from user input.
    Returns:
        str: The sanitized query.
    """
    # Basic escape to handle single quotes in names and ensure proper query formatting
    query = query.replace("'", "''")  # Escape single quotes by doubling them
    return query

@tool
def sql_engine(query: str) -> str:
    """
    Executes an SQL query on the 'receipts' table and returns formatted results.
    Args:
        query (str): The SQL query to execute.
    Returns:
        str: The result of the SQL query as a formatted string.
    """
    try:
        query = sanitize_query(query)  # Sanitize the query before execution
        
        with engine.connect() as con:
            rows = con.execute(text(query)).fetchall()

        if not rows:
            return "No results found."

        if len(rows) == 1 and len(rows[0]) == 1:
            return str(rows[0][0])  # Convert numerical result to string

        return "\n".join([", ".join(map(str, row)) for row in rows])

    except Exception as e:
        return f"Error: {str(e)}"

# Function to handle natural language query and convert it to SQL
def query_sql(user_query: str) -> str:
    schema_info = (
        "The database has a table named 'receipts' with the following schema:\n"
        "- receipt_id (INTEGER, primary key)\n"
        "- customer_name (VARCHAR(16))\n"
        "- price (FLOAT)\n"
        "- tip (FLOAT)\n"
        "Generate a valid SQL SELECT query using ONLY these column names.\n"
        "DO NOT explain your reasoning, and DO NOT return anything other than the SQL query itself."
    )

    generated_sql = agent.run(f"{schema_info} Convert this request into SQL: {user_query}")

    if not isinstance(generated_sql, str):
        return f"{generated_sql}"  # Handle unexpected numerical result

    result = sql_engine(generated_sql)
    
    try:
        float_result = float(result)
        return f"{float_result:.2f}"
    except ValueError:
        return result 

# Function to call query_sql and display the results in the UI
def handle_query(user_input: str) -> str:
    return query_sql(user_input)

# Initialize the agent with the necessary tools
agent = CodeAgent(
    tools=[sql_engine],
    model=HfApiModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct", token=""hf-key....""),
)

# Gradio UI layout
with gr.Blocks() as demo:
    gr.Markdown("""
    <style>
        .header { font-size: 24px; font-weight: bold; color: #333333; }
        .description { color: #666666; font-size: 16px; }
        .box { border: 1px solid #ccc; padding: 15px; border-radius: 10px; background-color: #f9f9f9; }
        .footer { text-align: center; font-size: 14px; color: #888888; }
    </style>
    <div class="header">
        <img src="path_to_logo.png" style="height: 60px; vertical-align: middle; margin-right: 10px;">
        Receipts Database Query Interface
    </div>
    <div class="description">
        This tool allows you to query the receipts database using natural language. Enter your question, and the system will generate and execute an SQL query to retrieve the data.
    </div>
    """)

    with gr.Row():
        with gr.Column(scale=1):
            user_input = gr.Textbox(label="Ask a question about the data", placeholder="E.g., 'What is the total price of all receipts?'")
            query_output = gr.Textbox(label="Result", interactive=False, lines=5)

        with gr.Column(scale=2):
            gr.Markdown("### Receipts Table")
            receipts_table = gr.Dataframe(value=get_receipts_table(), label="Receipts Table", wrap=True)

    user_input.change(fn=handle_query, inputs=user_input, outputs=query_output)
    demo.load(fn=get_receipts_table, outputs=receipts_table)

    gr.Markdown("""
    <div class="footer">
        Developed by Ashish Patel. All rights reserved.
    </div>
    """)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7861, share=True)
