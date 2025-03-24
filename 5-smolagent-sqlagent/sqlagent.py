import os
import gradio as gr
from sqlalchemy import text
from smolagents import tool, CodeAgent, HfApiModel
# import spaces
import pandas as pd
from database import engine, receipts
import pandas as pd

def get_receipts_table():
    """
    Fetches all data from the 'receipts' table and returns it as a Pandas DataFrame.
    Returns:
        A Pandas DataFrame containing all receipt data.
    """
    try:
        with engine.connect() as con:
            result = con.execute(text("SELECT * FROM receipts"))
            rows = result.fetchall()
        
        if not rows:
            return pd.DataFrame(columns=["receipt_id", "customer_name", "price", "tip"])

        # Convert rows into a DataFrame
        df = pd.DataFrame(rows, columns=["receipt_id", "customer_name", "price", "tip"])
        return df

    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]})  # Return error message in DataFrame format

@tool
def sql_engine(query: str) -> str:
    """
    Executes an SQL query on the 'receipts' table and returns formatted results.
    Args:
        query: The SQL query to execute.
    Returns:
        Query result as a formatted string.
    """
    try:
        with engine.connect() as con:
            rows = con.execute(text(query)).fetchall()

        if not rows:
            return "No results found."

        if len(rows) == 1 and len(rows[0]) == 1:
            return str(rows[0][0])  # Convert numerical result to string

        return "\n".join([", ".join(map(str, row)) for row in rows])

    except Exception as e:
        return f"Error: {str(e)}"

def query_sql(user_query: str) -> str:
    """
    Converts natural language input to an SQL query using CodeAgent
    and returns the execution results.
    Args:
        user_query: The user's request in natural language.
    Returns:
        The query result from the database as a formatted string.
    """

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

    print(f"{generated_sql}")

    # if not generated_sql.strip().lower().startswith(("select", "show", "pragma")):
    #     return "Error: Only SELECT queries are allowed."

    result = sql_engine(generated_sql)

    print(f"{result}")
    
    try:
        float_result = float(result)
        return f"{float_result:.2f}"
    except ValueError:
        return result 

def handle_query(user_input: str) -> str:
    """
    Calls query_sql, captures the output, and directly returns it to the UI.
    Args:
        user_input: The user's natural language question.
    Returns:
        The SQL query result as a plain string to be displayed in the UI.
    """
    return query_sql(user_input)

agent = CodeAgent(
    tools=[sql_engine],
    model=HfApiModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct", token="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"),
)

with gr.Blocks() as demo:
    gr.Markdown("""
# Plain Text Query Interface
This tool allows you to query a receipts database using natural language. Simply type your question into the input box, and the tool will generate and execute an SQL query to retrieve relevant data. The results will be displayed in the output box.
### Usage:
1. Enter a question related to the receipts data in the text box.
2. The tool will convert your question into an SQL query and execute it.
3. The result will be displayed in the output box.
> The current receipts table is also displayed for reference.
""")

    with gr.Row():
        with gr.Column(scale=1):
            user_input = gr.Textbox(label="Ask a question about the data")
            query_output = gr.Textbox(label="Result")
        
        with gr.Column(scale=2):
            gr.Markdown("### Receipts Table")
            receipts_table = gr.Dataframe(value=get_receipts_table(), label="Receipts Table")

    user_input.change(fn=handle_query, inputs=user_input, outputs=query_output)

    demo.load(fn=get_receipts_table, outputs=receipts_table)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)