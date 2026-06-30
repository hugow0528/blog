#!/usr/bin/env python3
import os, base64, requests

with open('/home/admin/.gh_token', 'r') as f:
    token = f.read().strip()

h = {"Authorization": "token " + token, "Accept": "application/vnd.github+json"}
bd = "/home/admin/projects/blog"
o, r, b = "hugow0528", "blog", "main"

def pf(path, content, message):
    url = "https://api.github.com/repos/%s/%s/contents/%s" % (o, r, path)
    resp = requests.get(url, headers=h, params={"ref": b})
    sha = resp.json().get("sha") if resp.status_code == 200 else None
    payload = {"message": message, "content": base64.b64encode(content.encode()).decode(), "branch": b}
    if sha:
        payload["sha"] = sha
    return requests.put(url, headers=h, json=payload).status_code in [200, 201]

files = []
for root, dirs, filenames in os.walk(bd):
    for filename in filenames:
        if filename.endswith(('.html', '.css', '.xml', '.txt')):
            full_path = os.path.join(root, filename)
            rel_path = os.path.relpath(full_path, bd)
            files.append((rel_path, open(full_path).read(), "Auto: New posts"))

success = sum(1 for p, c, m in files if pf(p, c, m))
print("Pushed %d/%d files" % (success, len(files)))
