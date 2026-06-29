# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PropertyAI is a FastAPI-based application that answers property-related queries. The system is built on [Pydantic AI](https://ai.pydantic.dev/) and runs on GPT 5.5 (medium reasoning effort), using a single agent that gathers information via tools and responds to the user.

## Development Commands

### Package Management
This project uses `uv` for dependency management:
- `uv sync` - Install dependencies from lock file
- `uv sync --frozen` - Install dependencies without updating lock file (used in CI)
- `uv add <package>` - Add a new dependency
- `uv run <command>` - Run commands in the uv environment

### Testing
- `uv run pytest tests` - Run all tests
- `uv run pytest tests/test_providers.py` - Run a specific test file
- `uv run pytest tests/test_providers.py::test_name` - Run a specific test

### Linting
- `ruff check src tests` - Check for linting issues
- `ruff check --fix src tests` - Auto-fix linting issues
- `ruff format src tests` - Format code

### Running the Application
- `uv run fastapi dev src/main.py` - Run FastAPI development server
- Direct execution: `uv run python -m src.main`

## Architecture

### Agent System

The core is a single Pydantic AI agent:

- **property_agent** (`src/agents/property_agent.py`):
  - A `pydantic_ai.Agent` configured with the property system prompt and tools (e.g. `document_search_tool`)
  - Pydantic AI manages the tool-calling loop internally; the agent gathers any information it needs via tools, then writes the final answer
  - Exposed via the `/v1/query/response` endpoint, which returns `result.output` (a string)

### Model Configuration

Model setup lives in `src/llm/llm_models.py`:

- `gpt_5_5`: an `OpenAIResponsesModel("gpt-5.5")` backed by an `OpenAIProvider` that reads `openai_api_key` from settings
- `medium_reasoning_settings`: `OpenAIResponsesModelSettings(openai_reasoning_effort="medium")`
- The agent uses this model instance and settings

### Tool System

Tools are plain Python functions passed to an agent via the `tools=[...]` argument (or the `@agent.tool` / `@agent.tool_plain` decorators). Pydantic AI derives the tool name, description, and JSON schema from the function name, docstring, and type-annotated signature.

- Example: `document_search_tool` in `src/tools/document_tool.py`

To add a tool to an agent, include the function in its `tools` list.

### Configuration

- Configuration uses Pydantic Settings in `src/config.py` (loads from `.env`)

### Prompt Management

- Prompts stored as markdown files in `src/prompts/`
- Accessed via `read_prompt(prompt_name)` from `src/prompts/prompt_store.py`
- Uses LRU caching for performance
- Agent prompt: `property_agent_prompt.md`

### API Structure

Two main routers:
- **Query Router** (`src/routers/query_router.py`): `GET /v1/query/response` - Main query endpoint
- **ETL Router** (`src/routers/etl_router.py`): `POST /v1/documents/:id` - Document management (stub)

## Environment Configuration

Required environment variables in `.env`:
- `OPENAI_API_KEY` - OpenAI API key for LLM provider

## Key Implementation Notes

1. **Async Throughout**: All agent operations are async (`await agent.run(...)`)
2. **Tool Loop**: Pydantic AI runs the tool-calling loop; the agent does not need a manual iteration count or a "completed" sentinel
3. **Reasoning Effort**: Set via `OpenAIResponsesModelSettings(openai_reasoning_effort=...)` in `src/llm/llm_models.py`

## Testing Notes

- Tests require `OPENAI_API_KEY` env var (set to "dummy" in CI)
- Python version: 3.13+
- Test framework: pytest with pythonpath set to "." in pyproject.toml

## Adding New Features

**To add a new tool**:
1. Write a type-annotated function in `src/tools/` with a descriptive docstring
2. Add the function to the relevant agent's `tools=[...]` list

**To change the model or reasoning effort**:
1. Edit `gpt_5_5` / `medium_reasoning_settings` in `src/llm/llm_models.py`

**To add a new agent**:
1. Create a `pydantic_ai.Agent` in `src/agents/`, reusing `gpt_5_5` and `medium_reasoning_settings`
2. Give it a system prompt (via `read_prompt`) and any tools it needs
3. Expose it through a router endpoint (see `src/routers/query_router.py`)
