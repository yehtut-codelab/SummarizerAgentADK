from src.summarizer_agent.agents import build_research_and_summarizer_agents


def test_agents_are_created() -> None:
    research_agent, summarizer_agent = build_research_and_summarizer_agents()

    assert research_agent.name == "ResearchAgent"
    assert summarizer_agent.name == "SummarizerAgent"
