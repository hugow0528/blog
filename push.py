#!/usr/bin/env python3
import subprocess
import os

# Read token from file
with open('/home/admin/.gh_token', 'r') as f:
    token = f.read().strip()

# Change to blog directory
os.chdir('/home/admin/projects/blog')

# Git add and commit
subprocess.run(['git', 'add', '-A'])
subprocess.run(['git', 'commit', '-m', 'Auto: New blog posts'])

# Push with token
url = f'https://hugow0528:{token}@github.com/hugow0528/blog.git'
result = subprocess.run(['git', 'push', url, 'main'], capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print(result.stderr)
