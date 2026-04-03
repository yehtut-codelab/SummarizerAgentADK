"""ResearchAgent and SummarizerAgent."""

from __future__ import annotations

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search

from .config import MODEL_NAME, retry_config


def build_research_and_summarizer_agents() -> tuple[Agent, Agent]:
    """Create the two specialist agents"""
    research_agent = Agent(
        name="ResearchAgent",
        model=Gemini(
            model=MODEL_NAME,
            retry_options=retry_config,
        ),
        instruction="""You are a specialized research agent. Your only job is to use the
google_search tool to find 2-3 pieces of relevant information on the given topic and present the findings with citations.""",
        tools=[google_search],
        output_key="research_findings",
    )

    summarizer_agent = Agent(
        name="SummarizerAgent",
        model=Gemini(
            model=MODEL_NAME,
            retry_options=retry_config,
        ),
        instruction="""Read the provided research findings: {research_findings}
Create a concise summary as a bulleted list with 3-5 key points.""",
        output_key="final_summary",
    )

    return research_agent, summarizer_agent
