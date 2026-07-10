#!/usr/bin/env python3
import os
import base64
import requests

token_path = os.path.expanduser("~/.gh_token")
if not os.path.exists(token_path):
    print(f"Token file not found at {token_path}")
    exit(1)

with open(token_path, "r") as f:
    token = f.read().strip()

headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
base_dir = "/home/admin/projects/blog"
owner, repo, branch = "hugow0528", "blog", "main"

def push_file(path, content, message):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    resp = requests.get(url, headers=headers, params={"ref": branch})
    sha = resp.json().get("sha") if resp.status_code == 200 else None
    payload = {"message": message, "content": base64.b64encode(content.encode()).decode(), "branch": branch}
    if sha:
        payload["sha"] = sha
    r = requests.put(url, headers=headers, json=payload)
    ok = r.status_code in (200, 201)
    status = "OK" if ok else f"FAIL {r.status_code}"
    print(f"  {status}: {path}")
    return ok

files = []
for root, dirs, filenames in os.walk(base_dir):
    dirs[:] = [d for d in dirs if d != '.git']
    for filename in filenames:
        if filename.endswith((".html", ".css", ".xml", ".txt")):
            full_path = os.path.join(root, filename)
            rel_path = os.path.relpath(full_path, base_dir)
            with open(full_path, "r") as f:
                content = f.read()
            files.append((rel_path, content, "Auto: New blog posts"))

print(f"Pushing {len(files)} files to {owner}/{repo}...")
success = sum(1 for p, c, m in files if push_file(p, c, m))
print(f"\nDone! {success}/{len(files)} files pushed successfully.")
