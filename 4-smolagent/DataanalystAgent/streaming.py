from transformers.agents.agent_types import AgentAudio, AgentImage, AgentText, AgentType
from transformers.agents import ReactAgent


def pull_message(step_log: dict):
    try:
        from gradio import ChatMessage
    except ImportError:
        raise ImportError("Gradio should be installed in order to launch a gradio demo.")

    if step_log.get("rationale"):
        yield ChatMessage(role="assistant", content=step_log["rationale"])
    if step_log.get("tool_call"):
        used_code = step_log["tool_call"]["tool_name"] == "code interpreter"
        content = step_log["tool_call"]["tool_arguments"]
        if used_code:
            content = f"```py\n{content}\n```"
        yield ChatMessage(
            role="assistant",
            metadata={"title": f"🛠️ Used tool {step_log['tool_call']['tool_name']}"},
            content=content,
        )
    if step_log.get("observation"):
        yield ChatMessage(role="assistant", content=f"```\n{step_log['observation']}\n```")
    if step_log.get("error"):
        yield ChatMessage(
            role="assistant",
            content=str(step_log["error"]),
            metadata={"title": "💥 Error"},
        )


def stream_to_gradio(agent: ReactAgent, task: str, **kwargs):
    """Runs an agent with the given task and streams the messages from the agent as gradio ChatMessages."""

    try:
        from gradio import ChatMessage
    except ImportError:
        raise ImportError("Gradio should be installed in order to launch a gradio demo.")

    class Output:
        output: AgentType | str = None

    for step_log in agent.run(task, stream=True, **kwargs):
        if isinstance(step_log, dict):
            for message in pull_message(step_log):
                print("message", message)
                yield message

    Output.output = step_log
    if isinstance(Output.output, AgentText):
        yield ChatMessage(role="assistant", content=f"**Final answer:**\n```\n{Output.output.to_string()}\n```")
    elif isinstance(Output.output, AgentImage):
        yield ChatMessage(
            role="assistant",
            content={"path": Output.output.to_string(), "mime_type": "image/png"},
        )
    elif isinstance(Output.output, AgentAudio):
        yield ChatMessage(
            role="assistant",
            content={"path": Output.output.to_string(), "mime_type": "audio/wav"},
        )
    else:
        yield ChatMessage(role="assistant", content=Output.output)