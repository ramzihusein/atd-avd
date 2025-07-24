#!/usr/bin/env python3

import os
import requests
import sys
import json

# Required environment variables
GITHUB_REPO = os.environ.get("GITHUB_REPO")        # Format: "owner/repo"
WORKFLOW_FILE = os.environ.get("WORKFLOW_FILE")    # e.g., "manual-run.yml"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")      # GitHub PAT with `workflow` scope
GITHUB_REF = os.environ.get("GITHUB_REF", "main")  # Branch to run against

# Optional input arguments passed as JSON string
inputs = {}
if len(sys.argv) > 1:
    try:
        inputs = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        print("Invalid JSON passed as argument.")
        sys.exit(1)

if not GITHUB_REPO or not WORKFLOW_FILE or not GITHUB_TOKEN:
    print("Missing required environment variables.")
    sys.exit(1)

url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/workflows/{WORKFLOW_FILE}/dispatches"
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}
payload = {
    "ref": GITHUB_REF,
    "inputs": inputs
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 204:
    print("✅ Workflow triggered successfully.")
    sys.exit(0)
else:
    print(f"❌ Failed to trigger workflow: {response.status_code}")
    print(response.text)
    sys.exit(1)
