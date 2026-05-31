#!/usr/bin/env python3
"""AI Social Media Kit - Cross-platform social post generator."""
import json, os, sys, random
from datetime import datetime
from pathlib import Path

# ── Post templates per platform ────────────
TEMPLATES = {
    "twitter": {
        "max_chars": 280,
        "templates": [
            "🚀 Just shipped: {name}\n\n{oneliner}\n\n{features}\n\n🔗 {url}\n\n#AI #Automation #BuildInPublic",
            "I built {name} on a $35 Raspberry Pi 🤯\n\n{oneliner}\n\n✨ {features}\n\n{url}",
            "{name} is now live!\n\n{oneliner}\n\n💡 {features}\n\n100% automated. Zero human touch.\n\n{url}",
        ],
    },
    "linkedin": {
        "max_chars": 3000,
        "templates": [
            """🎉 Excited to share my latest AI product: **{name}**

{oneliner}

**Key Features:**
{features_bullet}

**Why I built this:**
{builder_story}

**Tech Stack:**
🐍 Python stdlib
🖥️ $35 Raspberry Pi
⏰ 24/7 Cron automation
📦 Zero external dependencies

Check it out: {url}

#AI #Automation #IndieHacker #BuildInPublic #Python""",
        ],
    },
    "threads": {
        "max_chars": 500,
        "templates": [
            "🧵 New build: {name}\n\n{oneliner}\n\nBuilt on a $35 Pi. 100% automated.\n\n{url}",
        ],
    },
    "reddit": {
        "max_chars": 40000,
        "templates": [
            """**Title:** I built {name} — {oneliner}

**Body:**

Hey r/{subreddit}!

I've been building AI products on a $35 Raspberry Pi that run 100% autonomously. My latest:

**{name}** — {oneliner}

**What it does:**
{features_bullet}

**Why it's different:**
- 🚫 Zero human intervention — fully automated
- 💰 Runs on a $35 Raspberry Pi
- 📦 Zero external dependencies
- ⏰ 24/7 cron-scheduled

**Tech:** Python + stdlib only

{url}

I'm building 20 AI products this way. Happy to answer questions!

Edit: Thanks for the support everyone! 🙏""",
        ],
    },
    "devto": {
        "max_chars": 100000,
        "templates": [
            """---
title: "I Built {name} on a $35 Raspberry Pi (And It Runs 24/7)"
published: true
tags: [ai, automation, python, raspberrypi]
---

# {name}: {oneliner}

I built {name} to {builder_story}

## What It Does

{features_bullet}

## How It Works

{technical_explanation}

## Why Raspberry Pi?

- 💰 **Cost:** $35 one-time. No AWS bills.
- ⚡ **Always on:** 24/7 cron automation
- 🌍 **Offline-capable:** No cloud dependency
- 🐍 **Python stdlib:** Zero external deps

## The Code

```python
{code_snippet}
```

## What's Next?

{builder_story}

---

*This is part of my [20 AI Products Stack](https://ulnit.github.io/agent-store) — all running on a $35 Raspberry Pi.*

{url}""",
        ],
    },
}

STORY_TEMPLATES = [
    "I got tired of doing {task} manually. So I automated it with AI.",
    "Everyone said you need a $200/mo server to run AI. I proved them wrong with a $35 Pi.",
    "The best product is the one that runs itself. {name} is that product.",
    "At 2AM, while I was sleeping, {name} was still working. That's the dream.",
]

TECH_EXPLANATIONS = [
    "The engine is pure Python stdlib — no pip install needed. Pillow handles graphics, FFmpeg handles video, and cron handles scheduling. That's it. Simple, reliable, zero-cost.",
    "I use Python's built-in libraries exclusively. HTTP requests, file I/O, JSON parsing — all stdlib. For media, Pillow (images) and FFmpeg (video). The entire stack fits on a 32GB SD card.",
    "The pipeline: (1) Cron triggers the engine, (2) Python fetches data, (3) AI processes it, (4) Output is generated and pushed to GitHub Pages. No cloud, no serverless, no Docker. Just a Pi.",
]

CODE_SNIPPETS = [
    """# The entire automation pipeline
import requests, json
from pathlib import Path

data = requests.get("API_URL").json()
result = process_with_ai(data)
Path("output/report.md").write_text(result)
# Pushed to GitHub Pages automatically""",
    """# Zero-dependency thumbnail generator
from PIL import Image, ImageDraw

img = Image.new("RGB", (1280, 720))
draw = ImageDraw.Draw(img)
draw.text((640, 360), "AI Generated", fill="white")
img.save("thumbnail.png")""",
]

SUBREDDITS = [
    "SaaS", "SideProject", "PassiveIncome", "Entrepreneur",
    "IndieBiz", "Automate", "ArtificialIntelligence", "MachineLearning",
    "InternetIsBeautiful", "IMadeThis", "Python", "automation"
]

def generate_post(product, platform, custom=None):
    """Generate a social post for a given product and platform."""
    t = TEMPLATES.get(platform)
    if not t:
        return {"error": f"Unknown platform: {platform}"}

    template = random.choice(t["templates"])
    story = random.choice(STORY_TEMPLATES)
    tech = random.choice(TECH_EXPLANATIONS)
    code = random.choice(CODE_SNIPPETS)
    sub = random.choice(SUBREDDITS)

    # Build features bullet
    feats = product.get("features", [])
    features_str = ", ".join(f["title"] for f in feats[:4])
    features_bullet = "\n".join(f"- **{f['title']}:** {f['desc']}" for f in feats[:5])

    content = template.format(
        name=product["name"],
        oneliner=product["oneliner"],
        features=features_str,
        features_bullet=features_bullet,
        url=product.get("url", f"https://github.com/ulnit/{product['slug']}"),
        builder_story=story.format(name=product["name"], task=product.get("task", "this")),
        technical_explanation=tech,
        code_snippet=code,
        subreddit=sub,
    )

    # Truncate if needed
    max_chars = t["max_chars"]
    if len(content) > max_chars:
        content = content[:max_chars-3] + "..."

    return {
        "platform": platform,
        "content": content,
        "char_count": len(content),
        "max_chars": max_chars,
    }

def batch_post(product, platforms=None):
    """Generate posts for all platforms."""
    if platforms is None:
        platforms = list(TEMPLATES.keys())

    results = {}
    for p in platforms:
        results[p] = generate_post(product, p)
    return results

# ── Product database ───────────────────────
PRODUCTS_DB = [
    {
        "name": "AI Video Factory", "slug": "ai-video-factory",
        "oneliner": "AI自动写脚本、生成幻灯片、合成视频。零人工，全自动。",
        "url": "https://github.com/ulnit/ai-video-factory",
        "task": "video editing and script writing",
        "features": [
            {"title": "全自动视频生成", "desc": "AI从选题到成品，零人工干预"},
            {"title": "1080p幻灯片", "desc": "Pillow渲染精美幻灯片"},
            {"title": "AI脚本", "desc": "自动研究热门话题生成脚本"},
            {"title": "背景音乐", "desc": "FFmpeg自动合成背景音乐"},
            {"title": "定时发布", "desc": "每天7:00自动生成"},
        ],
    },
    {
        "name": "AI API Gateway", "slug": "ai-api-gateway",
        "oneliner": "白标AI API转售平台。转售GPT-4o/Claude，30-50%利润。",
        "url": "https://github.com/ulnit/ai-api-gateway",
        "task": "managing API keys and billing",
        "features": [
            {"title": "OpenAI兼容", "desc": "完全兼容OpenAI SDK"},
            {"title": "30-50%加价", "desc": "你的定价-成本=你的利润"},
            {"title": "用量统计", "desc": "实时Token统计"},
            {"title": "API Key管理", "desc": "独立Key+限额"},
            {"title": "速率限制", "desc": "内置rate limiting"},
        ],
    },
    {
        "name": "AI Trading Signals", "slug": "ai-trading-signals",
        "oneliner": "A股AI交易信号。每日自动生成买卖建议+风险评分。",
        "url": "https://github.com/ulnit/ai-trading-signals",
        "task": "tracking stocks and analyzing charts",
        "features": [
            {"title": "A股全覆盖", "desc": "新浪财经实时数据"},
            {"title": "AI趋势分析", "desc": "多维度技术指标"},
            {"title": "每日报告", "desc": "工作日16:00自动生成"},
            {"title": "信号推送", "desc": "自动推送到消息平台"},
            {"title": "风险评分", "desc": "AI仓位管理建议"},
        ],
    },
    {
        "name": "AI Thumbnail Pro", "slug": "ai-thumbnail-pro",
        "oneliner": "AI驱动的社交媒体缩略图生成器。8种预设，批量生成。",
        "url": "https://github.com/ulnit/ai-thumbnail-pro",
        "task": "designing social media graphics",
        "features": [
            {"title": "8种预设", "desc": "YouTube/博客/社媒全覆盖"},
            {"title": "渐变配色", "desc": "8组精美配色方案"},
            {"title": "批量生成", "desc": "一次命令全部格式"},
            {"title": "自动排版", "desc": "智能换行居中"},
            {"title": "API模式", "desc": "可集成工作流"},
        ],
    },
    {
        "name": "AI Agent Toolkit", "slug": "ai-agent-toolkit",
        "oneliner": "AI Agent开发者必备CLI工具集。零依赖，Python stdlib only。",
        "url": "https://github.com/ulnit/ai-agent-toolkit",
        "task": "writing boilerplate code",
        "features": [
            {"title": "零依赖", "desc": "Python stdlib only"},
            {"title": "20+工具", "desc": "爬虫/API/数据/文件"},
            {"title": "Agent就绪", "desc": "结构化CLI输出"},
            {"title": "Web工具", "desc": "HTTP+HTML+JSON一站式"},
            {"title": "数据分析", "desc": "CSV/JSON自动分析"},
        ],
    },
]

# ── CLI ────────────────────────────────────
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AI Social Media Kit")
    parser.add_argument("--product", type=str, default="AI Video Factory", help="Product name")
    parser.add_argument("--platform", type=str, default="all", help="Platform or 'all'")
    parser.add_argument("--output", type=str, help="Output JSON file")
    args = parser.parse_args()

    # Find product
    product = None
    for p in PRODUCTS_DB:
        if p["name"].lower() == args.product.lower():
            product = p
            break

    if not product:
        print(f"产品 '{args.product}' 未找到")
        print("可用: ", ", ".join(p["name"] for p in PRODUCTS_DB))
        sys.exit(1)

    if args.platform == "all":
        results = batch_post(product)
    else:
        results = {args.platform: generate_post(product, args.platform)}

    output = {
        "product": product["name"],
        "generated_at": datetime.now().isoformat(),
        "posts": results,
    }

    if args.output:
        Path(args.output).write_text(json.dumps(output, indent=2, ensure_ascii=False))
        print(f"✅ Saved to {args.output}")
    else:
        print(json.dumps(output, indent=2, ensure_ascii=False))