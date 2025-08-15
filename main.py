from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from dataclasses import dataclass


class Result(BaseModel):
    year: int
    author: str


@dataclass
class Params:
    programming_language: str


agent = Agent(
    "google-gla:gemini-1.5-flash",
    deps_type=Params,
    output_type=Result,
)


@agent.system_prompt
def get_system_prompt(ctx: RunContext[Params]) -> str:
    print(f"System prompt called with deps: {ctx.deps}")
    return f"You are a knowledge base for the following programming language: {ctx.deps.programming_language}"


result = agent.run_sync(
    "What year was the language released released?",
    deps=Params(programming_language="Rust"),
)
print(result.output.year)
print(result.output.author)
