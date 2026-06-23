#!/usr/bin/env python3
import subprocess
import os

TOKEN = "ghp_WQ...VOlG"
os.chdir('/home/admin/projects/blog')
subprocess.run(['git', 'add', '-A'])
subprocess.run(['git', 'commit', '-m', 'Auto: New blog posts'])
result = subprocess.run(['git', 'push', f'https://hugow0528:***@github.com/hugow0528/blog.git', 'main'], capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print(result.stderr)
