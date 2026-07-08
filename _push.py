#!/usr/bin/env python3
import os, base64, requests

token = open('/home/admin/.gh_token').read().strip()
headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
base = "/home/admin/projects/blog"
owner, repo, branch = "hugow0528", "blog", "main"

def push(path, content, msg):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    r = requests.get(url, headers=headers, params={"ref": branch})
    sha = r.json().get("sha") if r.status_code == 200 else None
    p = {"message": msg, "content": base64.b64encode(content.encode()).decode(), "branch": branch}
    if sha: p["sha"] = sha
    return requests.put(url, headers=headers, json=p).status_code in [200, 201]

files = []
for root, _, fns in os.walk(base):
    for fn in fns:
        if fn.endswith(('.html', '.css', '.xml', '.txt')):
            fp = os.path.join(root, fn)
            rp = os.path.relpath(fp, base)
            files.append((rp, open(fp).read(), "Auto: New posts"))

ok = sum(push(p, c, m) for p, c, m in files)
print(f"Done {ok}/{len(files)}")
