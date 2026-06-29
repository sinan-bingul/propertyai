from pathlib import Path

import pymupdf
import typer
from skill_generation.llm_providers import get_openai_client
import asyncio

app = typer.Typer()

openai_client = get_openai_client()

PK_COURSE_DIR = Path("data/pk_course")


@app.callback()
def main() -> None:
    """PK course processing CLI."""


@app.command("process_pk_course")
def process_pk_course() -> None:
    """Read every PDF file under data/pk_course (including sub folders)."""
    pdf_paths = sorted(PK_COURSE_DIR.rglob("*.pdf"))

    pdf_paths = pdf_paths[:1]
    for pdf_path in pdf_paths:
        with pymupdf.open(pdf_path) as doc:
            text = "\n".join(page.get_text() for page in doc)
        print(f"--- {pdf_path} ({len(text)} chars) ---")
        print(text[:5000])
    
    response = asyncio.run(openai_client.responses.create(
        model="gpt-5.5",
        instructions="System prompt"
        input=prompt,
        reasoning={"effort": "none"},
    ))

    return response.output_text

if __name__ == "__main__":
    app()
