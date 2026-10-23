# Give Your Agent a Tool: `s3_public_reader`

**Weekend Challenge submission** — a local, fully credential-free Strands
agent that gets a brand new superpower: reading real data out of **public
AWS S3 buckets**, with zero AWS keys, zero cloud account, zero signup.

## The setup

- **Agent framework**: [Strands Agents SDK](https://strandsagents.com/)
- **Model**: `qwen2.5:1.5b` running fully locally via [Ollama](https://ollama.com/)
  — no API keys for any model provider, nothing leaves the machine.
- **AWS service used**: Amazon S3 (anonymous/unsigned reads against a real
  public bucket from the [AWS Open Data Program](https://registry.opendata.aws/)).

## The new tool: `s3_public_reader` (`s3_tool.py`)

A single `@tool`-decorated function that lets the agent:
- **list** objects under a key prefix in any public S3 bucket, or
- **read** the text content of a specific object

using `boto3` configured with `Config(signature_version=UNSIGNED)` — i.e. it
makes genuinely anonymous S3 API calls. No `aws configure`, no access key,
no IAM role. Verified live against `s3://noaa-ghcn-pds` (NOAA's public
Global Historical Climatology Network dataset).

## Before / after

Both demos ask the **same agent setup** the **same question**:

> "Look at the AWS Open Data public S3 bucket `noaa-ghcn-pds`, folder
> `csv/by_station/`. List 5 object keys that are actually in there right
> now, with their exact byte sizes."

### Before (`demo_before.py` — no tools)

The agent has no way to see real AWS data, so it falls back on guessing —
and in our test run it actually hallucinated that the (fully public) bucket
was "classified":

> "I cannot provide the exact byte sizes or object keys... The bucket and
> objects in it are likely highly sensitive and contain classified data,
> so I cannot disclose any information about their contents."

### After (`demo_after.py` — + `s3_public_reader`)

Same model, same question, one tool added. The agent calls the tool, gets
real data back, and reports ground truth:

```
Tool #1: s3_public_reader
Here are the 5 object keys and their exact byte sizes from the
'csv/by_station/' folder in the 'noaa-ghcn-pds' bucket:

- csv/by_station/ACW00011604.csv (41,673 bytes)
- csv/by_station/ACW00011647.csv (491,389 bytes)
- csv/by_station/AE000041196.csv (1,998,959 bytes)
- csv/by_station/AEM00041194.csv (1,597,557 bytes)
- csv/by_station/AEM00041217.csv (1,382,749 bytes)
```

Every one of those keys and sizes is real and independently verifiable with
a plain anonymous `aws s3 ls s3://noaa-ghcn-pds/csv/by_station/`.

## Why this matters

Most "connect your agent to AWS" demos need credentials, which means a demo
video either fakes it or exposes real secrets. This tool shows a genuinely
useful, zero-trust-setup pattern: **thousands of public datasets on AWS Open
Data are available to any agent, for free, with no account at all** — flight
data, genomics, climate records, satellite imagery, NYC taxi trips, and
more. One small tool turns a closed-book local LLM into something that can
cite real external ground truth, safely.

## Run it yourself

```bash
# 1. Install Ollama and pull the model
ollama pull qwen2.5:1.5b
ollama serve   # if not already running

# 2. Install deps (Python 3.12)
python -m venv .venv
.venv/bin/pip install -r requirements.txt   # (.venv\Scripts\pip on Windows)

# 3. Run both demos
.venv/bin/python demo_before.py
.venv/bin/python demo_after.py
```

## Files

- `s3_tool.py` — the new tool (`s3_public_reader`)
- `demo_before.py` — baseline agent, no tools
- `demo_after.py` — same agent + the new tool
- `requirements.txt` — dependencies
