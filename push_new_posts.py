import os
import base64
import requests

with open('/home/admin/.gh_token', 'r') as f:
    token = f.read().strip()

headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
base_dir = "/home/admin/projects/blog"
owner, repo, branch = "hugow0528", "blog", "main"

def push_file(path, content, message):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    resp = requests.get(url, headers=headers, params={"ref": branch})
    sha = resp.json().get("sha") if resp.status_code == 200 else None
    payload = {"message": message, "content": base64.b64encode(content.encode()).decode(), "branch": branch}
    if sha: payload["sha"] = sha
    r = requests.put(url, headers=headers, json=payload)
    status = r.status_code
    if status not in [200, 201]:
        print(f"  ❌ {path}: HTTP {status}")
        if status == 403:
            print(f"     {r.json().get('message', 'Unknown error')}")
    return status in [200, 201]

# Push only the changed/new files
files_to_push = [
    ("posts/python-debugging-profiling.html", "Auto: New post — Python Debugging and Profiling"),
    ("posts/network-fundamentals.html", "Auto: New post — Network Fundamentals"),
    ("index.html", "Auto: Update index with new posts"),
    ("sitemap.xml", "Auto: Update sitemap with new posts"),
]

success = 0
for rel_path, message in files_to_push:
    full_path = os.path.join(base_dir, rel_path)
    with open(full_path, 'r') as f:
        content = f.read()
    print(f"Pushing: {rel_path} ({len(content)} bytes)...")
    if push_file(rel_path, content, message):
        print(f"  ✅ {rel_path}")
        success += 1
    else:
        print(f"  ❌ {rel_path}")

print(f"\n✅ Pushed {success}/{len(files_to_push)} files")
