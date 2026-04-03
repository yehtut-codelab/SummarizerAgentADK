"""Chainlit chat UI for the SummarizerAgent pipeline."""

from __future__ import annotations

import chainlit as cl

from src.summarizer_agent.main import run


@cl.on_chat_start
async def on_chat_start() -> None:
    await cl.Message(
        content=(
            "SummarizerAgent is ready.\n"
            "Send a topic, and I will research and return a concise summary."
        )
    ).send()


@cl.on_message
async def on_message(message: cl.Message) -> None:
    async with cl.Step(name="research_and_summarize"):
        try:
            output = await run(message.content)
        except Exception as exc:
            output = f"Request failed: {exc}"

    await cl.Message(content=output).send()
