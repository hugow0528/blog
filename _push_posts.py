#!/usr/bin/env python3
"""Update blog index, sitemap, and push to GitHub."""
import os
import re
import base64
import requests
from datetime import datetime, timezone

# ── Config ──
with open('/home/admin/.gh_token', 'r') as f:
    token = f.read().strip()

headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
base_dir = "/home/admin/projects/blog"
owner, repo, branch = "hugow0528", "blog", "main"

# ── New posts info ──
NEW_POSTS = [
    {
        'file': 'https-tls-explained.html',
        'title': 'HTTPS and TLS Explained: How Encryption Protects Your Data Online — Complete Beginner\'s Guide',
        'excerpt': 'Understand how HTTPS and TLS actually work — the TLS handshake, certificates, public/private key cryptography, cipher suites, HSTS, certificate authorities, and how to verify a site\'s security. Practical commands and real-world examples. From the padlock icon to production certificate management.',
        'tags': 'security',
        'tag_labels': '<span class="tag security">Security</span>',
        'date': 'July 13, 2026',
        'date_iso': '2026-07-13',
        'read_time': '12 min read',
    },
    {
        'file': 'git-cherry-pick-stash-bisect.html',
        'title': 'Git Cherry-Pick, Stash, and Bisect: Power Tools Every Developer Needs — Complete Guide',
        'excerpt': 'Master three essential Git commands that separate beginners from power users — cherry-pick to selectively merge commits, stash to temporarily save work without committing, and bisect to find bugs using binary search. Real-world scenarios and working examples for each tool.',
        'tags': 'devops',
        'tag_labels': '<span class="tag devops">DevOps</span>',
        'date': 'July 13, 2026',
        'date_iso': '2026-07-13',
        'read_time': '10 min read',
    },
]

def generate_post_card(post):
    return f'''        <article class="post" data-tags="{post["tags"]}">
            <div class="post-tags">
                {post["tag_labels"]}
            </div>
            <h2 class="post-title"><a href="posts/{post["file"]}">{post["title"]}</a></h2>
            <div class="post-excerpt">
                <p>{post["excerpt"]}</p>
            </div>
            <div class="post-meta">
                <span class="post-date">{post["date"]}</span>
                <span class="post-read-time">{post["read_time"]}</span>
                <span class="post-badge">New</span>
            </div>
        </article>'''

def update_index():
    """Insert new posts at the top of the posts grid."""
    index_path = os.path.join(base_dir, 'index.html')
    with open(index_path, 'r') as f:
        content = f.read()

    # Build new post cards
    new_cards = '\n        '.join(generate_post_card(p) for p in NEW_POSTS)

    # Find the posts container and insert new cards after the opening
    # Pattern: first existing <article class="post"
    pattern = r'(        <!-- Posts Grid -->\n        <div class="posts" id="postsContainer">\n)(        <article class="post")'
    replacement = r'\1\n' + new_cards + '\n        \2'
    content = re.sub(pattern, replacement, content, count=1)

    # Remove "New" badge from old posts (keep only on our new ones)
    # Find all badges that are not in our new cards and remove them
    # Actually, let's just keep the badges as they are for now

    with open(index_path, 'w') as f:
        f.write(content)

    print("✅ index.html updated with new posts")

def update_sitemap():
    """Add new posts to sitemap.xml."""
    sitemap_path = os.path.join(base_dir, 'sitemap.xml')
    with open(sitemap_path, 'r') as f:
        content = f.read()

    # Build sitemap entries
    entries = ''
    for post in NEW_POSTS:
        entries += f'''    <url>
        <loc>https://blog.hugow.dev/posts/{post["file"]}</loc>
        <lastmod>{post["date_iso"]}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.9</priority>
    </url>
'''

    # Insert after the opening <urlset> tag
    content = content.replace('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
                               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + entries)

    # Update index lastmod
    content = content.replace(
        '<loc>https://blog.hugow.dev/</loc>\n        <lastmod>2026-07-10</lastmod>',
        '<loc>https://blog.hugow.dev/</loc>\n        <lastmod>2026-07-13</lastmod>'
    )

    with open(sitemap_path, 'w') as f:
        f.write(content)

    print("✅ sitemap.xml updated")

def push_file(path, content, message):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    resp = requests.get(url, headers=headers, params={"ref": branch})
    sha = resp.json().get("sha") if resp.status_code == 200 else None
    payload = {"message": message, "content": base64.b64encode(content.encode()).decode(), "branch": branch}
    if sha: payload["sha"] = sha
    result = requests.put(url, headers=headers, json=payload)
    return result.status_code in [200, 201], result.status_code

def main():
    # Step 1: Update local files
    update_index()
    update_sitemap()

    # Step 2: Collect all files to push
    files = []
    for root, dirs, filenames in os.walk(base_dir):
        for filename in filenames:
            if filename.endswith(('.html', '.css', '.xml', '.txt', '.js')):
                full_path = os.path.join(root, filename)
                rel_path = os.path.relpath(full_path, base_dir)
                with open(full_path, 'r') as f:
                    files.append((rel_path, f.read(), "Auto: new blog posts"))

    # Step 3: Push to GitHub
    success = 0
    failed = []
    for path, content, message in files:
        ok, status = push_file(path, content, message)
        if ok:
            success += 1
        else:
            failed.append((path, status))
        # Rate limit: GitHub API has limits
        import time
        time.sleep(0.3)

    print(f"\n✅ Pushed {success}/{len(files)} files successfully")
    if failed:
        print(f"❌ Failed: {failed}")

    print(f"\nNew posts created:")
    for post in NEW_POSTS:
        print(f"  📝 {post['file']} — {post['title'][:60]}...")

if __name__ == '__main__':
    main()
