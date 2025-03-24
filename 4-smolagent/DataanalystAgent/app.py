import os
import shutil
import gradio as gr
from smolagents import CodeAgent, HfApiModel, Tool
import pandas as pd

from gradio import Chatbot
from smolagents import stream_to_gradio
from huggingface_hub import login
from gradio.data_classes import FileData

login(os.getenv("HUGGINGFACEHUB_API_TOKEN"))

model = HfApiModel("Qwen/Qwen2.5-Coder-32B-Instruct")

agent = CodeAgent(
    tools=[],
    model=model,
    additional_authorized_imports=["numpy", "pandas", "matplotlib.pyplot", "seaborn", "scipy.stats"],
    max_steps=10,
)

base_prompt = """You are an expert data analyst.
According to the features you have and the data structure given below, determine which feature should be the target.
Then list 3 interesting questions that could be asked on this data, for instance about specific correlations with target variable.
Then answer these questions one by one, by finding the relevant numbers.
Meanwhile, plot some figures using matplotlib/seaborn and save them to the (already existing) folder './figures/': take care to clear each figure with plt.clf() before doing another plot.

In your final answer: summarize these correlations and trends
After each number derive real worlds insights, for instance: "Correlation between is_december and boredness is 1.3453, which suggest people are more bored in winter".
Your final answer should be a long string with at least 3 numbered and detailed parts.

Structure of the data:
{structure_notes}

The data file is passed to you as the variable data_file, it is a pandas dataframe, you can use it directly.
DO NOT try to load data_file, it is already a dataframe pre-loaded in your python interpreter!
"""

example_notes="""This data is about the Titanic wreck in 1912.
The target figure is the survival of passengers, notes by 'Survived'
pclass: A proxy for socio-economic status (SES)
1st = Upper
2nd = Middle
3rd = Lower
age: Age is fractional if less than 1. If the age is estimated, is it in the form of xx.5
sibsp: The dataset defines family relations in this way...
Sibling = brother, sister, stepbrother, stepsister
Spouse = husband, wife (mistresses and fiancés were ignored)
parch: The dataset defines family relations in this way...
Parent = mother, father
Child = daughter, son, stepdaughter, stepson
Some children travelled only with a nanny, therefore parch=0 for them."""

def get_images_in_directory(directory):
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'}

    image_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1].lower() in image_extensions:
                image_files.append(os.path.join(root, file))
    return image_files

def interact_with_agent(file_input, additional_notes):
    shutil.rmtree("./figures")
    os.makedirs("./figures")

    data_file = pd.read_csv(file_input)
    data_structure_notes = f"""- Description (output of .describe()):
    {data_file.describe()}
    - Columns with dtypes:
    {data_file.dtypes}"""

    prompt = base_prompt.format(structure_notes=data_structure_notes)

    if additional_notes and len(additional_notes) > 0:
        prompt += "\nAdditional notes on the data:\n" + additional_notes

    messages = [gr.ChatMessage(role="user", content=prompt)]
    yield messages + [
        gr.ChatMessage(role="assistant", content="⏳ _Starting task..._")
    ]

    plot_image_paths = {}
    for msg in stream_to_gradio(agent, prompt, data_file=data_file):
        messages.append(msg)
        for image_path in get_images_in_directory("./figures"):
            if image_path not in plot_image_paths:
                image_message = gr.ChatMessage(
                    role="assistant",
                    content=FileData(path=image_path, mime_type="image/png"),
                )
                plot_image_paths[image_path] = True
                messages.append(image_message)
        yield messages + [
            gr.ChatMessage(role="assistant", content="⏳ _Still processing..._")
        ]
    yield messages


with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue=gr.themes.colors.yellow,
        secondary_hue=gr.themes.colors.blue,
    )
) as demo:
    gr.Markdown("""# Qwen-2.5-Coder Data analyst 📊🤔

Drop a `.csv` file below, add notes to describe this data if needed, and **`Qwen2.5-Coder-32B-Instruct` will analyze the file content and draw figures for you!**""")
    file_input = gr.File(label="Your file to analyze")
    text_input = gr.Textbox(
        label="Additional notes to support the analysis"
    )
    submit = gr.Button("Run analysis!", variant="primary")
    chatbot = gr.Chatbot(
        label="Data Analyst Agent",
        type="messages",
        avatar_images=(
            None,
            "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/smolagents/mascot.png",
        ),
    )
    gr.Examples(
        examples=[["./example/titanic.csv", example_notes]],
        inputs=[file_input, text_input],
        cache_examples=False
    )

    submit.click(interact_with_agent, [file_input, text_input], [chatbot])

if __name__ == "__main__":
    demo.launch()