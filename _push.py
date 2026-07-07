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
    result = requests.put(url, headers=headers, json=payload)
    if result.status_code in [200, 201]:
        print(f"  ✅ {path}")
        return True
    else:
        print(f"  ❌ {path}: {result.status_code} - {result.text[:200]}")
        return False

files = []
for root, dirs, filenames in os.walk(base_dir):
    for filename in filenames:
        if filename.endswith(('.html', '.css', '.xml', '.txt')):
            full_path = os.path.join(root, filename)
            rel_path = os.path.relpath(full_path, base_dir)
            with open(full_path, 'r') as f:
                content = f.read()
            files.append((rel_path, content, "Auto: New blog posts - Python closures & GitHub Actions runners"))

print(f"Pushing {len(files)} files...\n")
success = sum(1 for p, c, m in files if push_file(p, c, m))
print(f"\n✅ Pushed {success}/{len(files)} files")
