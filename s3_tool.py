"""
A new tool for a Strands agent: read any PUBLIC (anonymous-access) AWS S3 bucket.

Why this tool:
- Lots of real-world data lives in public S3 buckets (AWS Open Data program,
  government datasets, public research corpora) that anyone can read without
  an AWS account, IAM user, or any credentials at all.
- An LLM-only agent has no way to see that data. This tool gives it eyes on
  real AWS infrastructure, using *unsigned* S3 requests (signature_version
  UNSIGNED), so it needs zero AWS keys/secrets to work.

Verified live against s3://noaa-ghcn-pds (NOAA's public climate dataset).
"""
import boto3
from botocore import UNSIGNED
from botocore.config import Config
from strands import tool

_s3 = boto3.client("s3", region_name="us-east-1", config=Config(signature_version=UNSIGNED))

MAX_CHARS = 3000


@tool
def s3_public_reader(bucket: str, prefix: str = "", key: str = "", max_keys: int = 10) -> str:
    """Read data out of a PUBLIC AWS S3 bucket, with no AWS credentials required.

    Works only on buckets that allow anonymous/unsigned reads (e.g. AWS Open
    Data Program buckets like "noaa-ghcn-pds", "nyc-tlc", "1000genomes").

    Two modes:
    - LIST mode: pass `bucket` and `prefix` (key prefix / folder path) to list
      up to `max_keys` matching object keys and their sizes.
    - READ mode: pass `bucket` and `key` (an exact object key) to fetch and
      return that object's text content (truncated to a few KB if large).

    Args:
        bucket: The S3 bucket name, e.g. "noaa-ghcn-pds".
        prefix: Key prefix to list under, e.g. "csv/by_station/". Ignored if `key` is set.
        key: Exact object key to read, e.g. "csv/by_station/USW00094728.csv".
        max_keys: Max number of keys to return in LIST mode (default 10).
    """
    target = key or prefix or "(bucket root)"
    try:
        if key:
            obj = _s3.get_object(Bucket=bucket, Key=key)
            body = obj["Body"].read()
            text = body.decode("utf-8", errors="replace")
            if len(text) > MAX_CHARS:
                text = text[:MAX_CHARS] + f"\n...[truncated, {len(body)} bytes total]"
            return f"Read s3://{bucket}/{key} ({len(body)} bytes):\n\n{text}"
        else:
            resp = _s3.list_objects_v2(Bucket=bucket, Prefix=prefix, MaxKeys=max_keys)
            contents = resp.get("Contents", [])
            if not contents:
                return f"No objects found in s3://{bucket}/{prefix}"
            lines = [f"- {o['Key']}  ({o['Size']} bytes)" for o in contents]
            return f"Found {len(lines)} object(s) in s3://{bucket}/{prefix}:\n" + "\n".join(lines)
    except Exception as e:
        return f"Error accessing s3://{bucket}/{target}: {e}"
