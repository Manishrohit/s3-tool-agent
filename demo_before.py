"""
BEFORE: a plain Strands agent running a local Ollama model, no tools at all.

Ask it something that can only be answered by looking at *real, current* data
sitting in a public AWS S3 bucket. Watch it either refuse, guess, or hallucinate,
because it has no way to reach outside its own training data.
"""
from strands import Agent
from strands.models.ollama import OllamaModel

model = OllamaModel(host="http://127.0.0.1:11434", model_id="qwen2.5:1.5b")

agent = Agent(
    model=model,
    tools=[],
    system_prompt=(
        "You are a helpful assistant. Answer directly and honestly. "
        "If you cannot know something because you lack real-time data access, say so plainly."
    ),
)

QUESTION = (
    "Look at the AWS Open Data public S3 bucket 'noaa-ghcn-pds', folder "
    "'csv/by_station/'. List 5 object keys that are actually in there right now, "
    "with their exact byte sizes."
)

if __name__ == "__main__":
    print("=== BEFORE: agent with NO tools ===")
    print(f"Question: {QUESTION}\n")
    agent(QUESTION)
