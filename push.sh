#!/bin/bash
# Blog auto-push script

cd /home/admin/projects/blog

# Add and commit changes
git add -A
git commit -m "Auto: New blog posts"

# Push with token
git push https://hugow0528:***@github.com/hugow0528/blog.git main
