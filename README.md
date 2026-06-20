# Hugo's Dev Notes Blog

A simple, static blog built with pure HTML/CSS.

## Structure
```
blog/
├── index.html       # Homepage
├── style.css        # Styles  
├── posts/
│   ├── cloudflare-tunnel.html
│   ├── cloudflare-dns.html
│   ├── python-first-script.html
│   ├── python-variables.html
│   ├── what-is-vibe-coding.html
│   └── vibe-coding-tools.html
└── README.md
```

## Edit Posts
- Open any `.html` file in the `posts/` folder
- Add new posts by copying an existing file and editing

## Deploy
1. Copy to `~/deploys/blog/`
2. Run: `cd ~/deploys/blog && python3 -m http.server 8090`
3. Ensure blog.hugow.dev is in Cloudflare tunnel config
4. Restart Cloudflared

## Host Anywhere
This is pure HTML — no dependencies. You can also host on:
- GitHub Pages
- Netlify (drag & drop)
- Vercel
