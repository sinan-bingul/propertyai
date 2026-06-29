from pathlib import Path

import tiktoken


def read_text_file(path: str | Path, encoding: str = "utf-8") -> str:
    """Read and return the contents of a text file."""
    return Path(path).read_text(encoding=encoding)


def count_tokens(text: str, model: str = "gpt-5") -> int:
    """Count the number of tokens in ``text`` using OpenAI's tokenizer."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("o200k_base")
    return len(encoding.encode(text))