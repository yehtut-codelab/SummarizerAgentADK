"""Minimal runner for ResearchAgent and SummarizerAgent."""

from __future__ import annotations

import asyncio
import sys
from contextlib import suppress

from google.adk.agents import SequentialAgent
from google.adk.runners import InMemoryRunner

from .agents import build_research_and_summarizer_agents
from .config import configure_google_api_key


def extract_response_text(response: object) -> str:
    """Extract text from ADK run_debug response for CLI display."""
    if isinstance(response, (list, tuple)):
        for item in reversed(response):
            content = getattr(item, "content", None)
            if content is None:
                continue
            parts = getattr(content, "parts", None)
            if not isinstance(parts, list):
                continue
            texts = []
            for part in parts:
                text = getattr(part, "text", None)
                if isinstance(text, str) and text.strip():
                    texts.append(text.strip())
            if texts:
                return "\n".join(texts)
    return str(response)


async def run(prompt: str) -> str:
    configure_google_api_key()

    research_agent, summarizer_agent = build_research_and_summarizer_agents()
    root_agent = SequentialAgent(
        name="ResearchSummarizerPipeline",
        sub_agents=[research_agent, summarizer_agent],
    )

    runner = InMemoryRunner(agent=root_agent)
    response = await runner.run_debug(prompt)
    return extract_response_text(response)


def run_sync(prompt: str) -> str:
    """Run async pipeline with Windows-safe loop lifecycle handling."""
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)

        def _loop_exception_handler(_loop: asyncio.AbstractEventLoop, context: dict) -> None:
            # Ignore noisy Windows SSL teardown races that can happen during shutdown.
            message = str(context.get("message", ""))
            exc = context.get("exception")
            if "Fatal error on SSL transport" in message:
                return
            if isinstance(exc, OSError) and getattr(exc, "winerror", None) == 10038:
                return

            default_handler = _loop.get_exception_handler()
            if default_handler is not None and default_handler is not _loop_exception_handler:
                default_handler(_loop, context)
            else:
                _loop.default_exception_handler(context)

        loop.set_exception_handler(_loop_exception_handler)

        result = loop.run_until_complete(run(prompt))

        # Give transport callbacks a chance to finish before shutting down the loop.
        loop.run_until_complete(asyncio.sleep(0.2))

        pending = [
            task
            for task in asyncio.all_tasks(loop)
            if not task.done()
        ]
        for task in pending:
            task.cancel()
        if pending:
            with suppress(Exception):
                loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))

        loop.run_until_complete(loop.shutdown_asyncgens())
        if hasattr(loop, "shutdown_default_executor"):
            loop.run_until_complete(loop.shutdown_default_executor())
        return result
    finally:
        asyncio.set_event_loop(None)
        loop.close()


def main() -> None:
    prompt = input("Enter a topic to research and summarize: ").strip()
    if not prompt:
        print("Prompt is required.")
        return

    result = run_sync(prompt)
    print("\n--- Summary ---\n")
    print(result)


if __name__ == "__main__":
    main()
