from functools import lru_cache

PROMPT_FOLDER = "src/prompts"


@lru_cache(maxsize=100)
def read_prompt(prompt_name: str):
    with open(f"{PROMPT_FOLDER}/{prompt_name}.md", "r") as file:
        prompt = file.read()

    return prompt
