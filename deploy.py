#!/usr/bin/env python3
import os
import base64
import requests

with open(os.path.expanduser("~/.gh_token"), "r") as f:
    token = f.read().strip()

headers = {"Authorization": "token " + token, "Accept": "application/vnd.github+json"}
base_dir = "/home/admin/projects/blog"
owner = "hugow0528"
repo = "blog"
branch = "main"

def push_file(path, content, message):
    url = "https://api.github.com/repos/" + owner + "/" + repo + "/contents/" + path
    resp = requests.get(url, headers=headers, params={"ref": branch})
    sha = None
    if resp.status_code == 200:
        sha = resp.json().get("sha")
    payload = {"message": message, "content": base64.b64encode(content.encode()).decode(), "branch": branch}
    if sha:
        payload["sha"] = sha
    r = requests.put(url, headers=headers, json=payload)
    status = r.status_code
    if status not in [200, 201]:
        print("  ERR " + path + ": " + str(status))
    return status in [200, 201]

files = []
for root, dirs, filenames in os.walk(base_dir):
    for filename in filenames:
        if filename.endswith((".html", ".css", ".xml", ".txt")):
            full_path = os.path.join(root, filename)
            rel_path = os.path.relpath(full_path, base_dir)
            files.append((rel_path, open(full_path).read(), "Auto: New posts"))

print("Pushing " + str(len(files)) + " files...")
success = 0
for p, c, m in files:
    if push_file(p, c, m):
        success += 1
print("Done: " + str(success) + "/" + str(len(files)) + " files pushed")
