"""Agent runner.

A small helper for executing a Pydantic AI agent with automatic retries.
Transient failures (e.g. provider rate limits or network errors) are retried
with random exponential backoff for up to five attempts.
"""

from typing import Any

from pydantic_ai import Agent
from pydantic_ai.agent import AgentRunResult
from tenacity import retry, stop_after_attempt, wait_random_exponential


@retry(
    wait=wait_random_exponential(multiplier=1, max=60),
    stop=stop_after_attempt(5),
    reraise=True,
)
async def run_agent(agent: Agent, *args: Any, **kwargs: Any) -> AgentRunResult:
    """Run a Pydantic AI agent, retrying on failure.

    The call is retried up to five times using random exponential backoff.

    Args:
        agent: The Pydantic AI ``Agent`` to run.
        *args: Positional arguments forwarded to ``agent.run`` (e.g. the query).
        **kwargs: Keyword arguments forwarded to ``agent.run``.

    Returns:
        The ``AgentRunResult`` produced by ``agent.run``.
    """
    return await agent.run(*args, **kwargs)
