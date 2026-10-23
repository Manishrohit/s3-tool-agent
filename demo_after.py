"""
AFTER: the SAME Strands agent + SAME local Ollama model, now equipped with
ONE new tool: s3_public_reader (anonymous, credential-free S3 access).

Ask it the exact same question as demo_before.py. This time it can actually
call the tool, read the real bucket listing, and answer with ground truth
instead of a guess -- and it needed zero AWS credentials to do it.
"""
from strands import Agent
from strands.models.ollama import OllamaModel
from s3_tool import s3_public_reader

model = OllamaModel(host="http://127.0.0.1:11434", model_id="qwen2.5:1.5b")

agent = Agent(
    model=model,
    tools=[s3_public_reader],
    system_prompt=(
        "You are a helpful assistant with access to a tool called s3_public_reader "
        "that can list or read objects in public AWS S3 buckets without any credentials. "
        "Use it whenever a question needs real data from a public S3 bucket. "
        "Report real tool results, don't invent data."
    ),
)

QUESTION = (
    "Look at the AWS Open Data public S3 bucket 'noaa-ghcn-pds', folder "
    "'csv/by_station/'. List 5 object keys that are actually in there right now, "
    "with their exact byte sizes."
)

if __name__ == "__main__":
    print("=== AFTER: agent WITH the new s3_public_reader tool ===")
    print(f"Question: {QUESTION}\n")
    agent(QUESTION)
