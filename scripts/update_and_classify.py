#!/usr/bin/env python3
"""
Awesome Stars & Product Remix Engine
------------------------------------
Automatically parses starred repositories, applies AI classification via Google Gemini API
(or intelligent semantic fallback), and generates:
1. data/repos.json (structured database)
2. README.md (product-builder categorized markdown catalog)
3. index.html (interactive web catalog & remix studio for GitHub Pages)
"""

import os
import sys
import json
import re
import urllib.request
import urllib.error
from datetime import datetime
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "repos.json")
README_FILE = os.path.join(BASE_DIR, "README.md")
LANGUAGES_FILE = os.path.join(BASE_DIR, "languages.md")
TOPICS_FILE = os.path.join(BASE_DIR, "topics.md")
INDEX_FILE = os.path.join(BASE_DIR, "index.html")

# The 10 Product Building-Block Categories
CATEGORIES = [
    {
        "id": "ai-agents",
        "name": "AI & Autonomous Agents",
        "icon": "🤖",
        "description": "Agent frameworks, LLM orchestrators, local inference runtimes, multi-agent swarms, and AI coding assistants.",
        "keywords": [
            "agent", "agents", "ai-agent", "ai-agents", "autonomous", "multi-agent", "llm",
            "large-language-models", "prompt", "langchain", "crewai", "autogen", "gpt",
            "openai", "anthropic", "claude", "ollama", "vllm", "llama", "ggml", "gguf",
            "inference", "fine-tuning", "copilot", "chatgpt", "deep-learning", "reinforcement-learning"
        ],
        "default_role": "Autonomous Agent / LLM Runtime"
    },
    {
        "id": "rag-data-ingestion",
        "name": "RAG, Vector & Data Ingestion",
        "icon": "🔍",
        "description": "Web crawlers, scrapers, vector search engines, embeddings, PDF/document extractors, and knowledge graphs.",
        "keywords": [
            "rag", "retrieval", "vector", "embedding", "embeddings", "vector-database", "vector-search",
            "crawler", "scraper", "scraping", "crawl", "parser", "pdf", "ocr", "extract",
            "knowledge-base", "knowledge-graph", "search-engine", "elasticsearch", "similarity-search"
        ],
        "default_role": "Data Ingestion & Retrieval (RAG)"
    },
    {
        "id": "saas-starters",
        "name": "SaaS Starters & App Boilerplates",
        "icon": "🚀",
        "description": "Full-stack skeletons, auth/OAuth providers, Stripe/billing templates, and multitenant scaffolding.",
        "keywords": [
            "boilerplate", "starter", "starter-kit", "template", "saas", "auth", "authentication",
            "oauth", "billing", "stripe", "payment", "invoice", "invoicing", "multi-tenant",
            "admin-panel", "identity", "jwt", "rbac", "skeleton", "laravel-starter"
        ],
        "default_role": "SaaS Foundation & Boilerplate"
    },
    {
        "id": "ui-generative-ux",
        "name": "UI Kits, Generative UX & Dashboards",
        "icon": "🎨",
        "description": "Tailwind component kits, generative UI chat widgets, node/canvas editors, and analytics dashboards.",
        "keywords": [
            "ui", "frontend", "components", "tailwind", "tailwindcss", "shadcn", "design-system",
            "canvas", "flow", "diagram", "generative-ui", "chart", "charts", "dataviz", "dashboard",
            "web-components", "icons", "editor", "svelte", "react", "vue", "radix"
        ],
        "default_role": "UI & Presentation Layer"
    },
    {
        "id": "apis-automation",
        "name": "APIs, Workflow Automation & Webhooks",
        "icon": "⚡",
        "description": "Low-code orchestration, event-driven pipelines, job queues, reverse proxies, and webhook routers.",
        "keywords": [
            "automation", "workflow", "orchestration", "pipeline", "webhook", "queue", "worker",
            "api-gateway", "rest-api", "graphql", "grpc", "reverse-proxy", "n8n", "microservices",
            "celery", "task-queue"
        ],
        "default_role": "Workflow & Integration Engine"
    },
    {
        "id": "data-storage-cache",
        "name": "Databases, Caching & Realtime State",
        "icon": "💾",
        "description": "Fast key-value caches, SQLite edge engines, distributed SQL, Valkey/Redis forks, and realtime pub/sub.",
        "keywords": [
            "database", "sqlite", "postgres", "postgresql", "mysql", "redis", "valkey", "cache",
            "caching", "key-value", "kv", "distributed-systems", "realtime", "websocket", "pubsub",
            "orm", "storage", "raft", "duckdb"
        ],
        "default_role": "Data Persistence & State Management"
    },
    {
        "id": "security-privacy",
        "name": "Security, Privacy & Auth Utilities",
        "icon": "🛡️",
        "description": "Audit logging, network security, reverse engineering, encryption, SIP protection, and credential tools.",
        "keywords": [
            "security", "cybersecurity", "privacy", "audit", "pentest", "vulnerability",
            "firewall", "encryption", "proxy", "sip", "auth-token", "scanner", "pgaudit"
        ],
        "default_role": "Security & Protection Layer"
    },
    {
        "id": "devops-infra",
        "name": "DevOps, Sandboxes & Cloud Infra",
        "icon": "📦",
        "description": "Containers, code execution sandboxes, WebAssembly, Kubernetes, Nix, and CI/CD automation.",
        "keywords": [
            "devops", "docker", "container", "containers", "kubernetes", "k8s", "wasm", "webassembly",
            "sandbox", "microvm", "ci-cd", "deployment", "terraform", "ansible", "nix"
        ],
        "default_role": "Infrastructure & Execution Sandbox"
    },
    {
        "id": "devtools-terminal",
        "name": "Developer Tooling & Terminal Utilities",
        "icon": "🛠️",
        "description": "CLI power tools, TUI interfaces, profilers, debuggers, code formatters, and terminal sharing.",
        "keywords": [
            "devtools", "developer-tools", "terminal", "cli", "tui", "shell", "profiler",
            "profiling", "debugger", "linter", "formatter", "command-line", "code-quality"
        ],
        "default_role": "Developer Productivity & Tooling"
    },
    {
        "id": "ready-to-remix",
        "name": "Ready-to-Remix Products & Self-Hosted Apps",
        "icon": "💡",
        "description": "Fully functional open-source apps (ERPs, invoicing, grocery trackers, CRM) ready to fork, reskin, and monetize.",
        "keywords": [
            "self-hosted", "erp", "crm", "ecommerce", "invoicing-system", "invoice", "finance",
            "booking", "notes", "analytics", "media", "social", "collaboration", "cms", "grocy",
            "invobook", "open-source-alternative"
        ],
        "default_role": "Forkable Product Archetype"
    }
]

# Sample Curated Remix Recipes to showcase combinations
FEATURED_REMIX_RECIPES = [
    {
        "title": "Autonomous Competitor & Price Intelligence Radar",
        "tagline": "Real-time web monitoring and AI analysis micro-SaaS",
        "ingredients": [
            {"name": "Crawl4AI / Scraper", "role": "RAG, Vector & Data Ingestion"},
            {"name": "Ollama / vLLM", "role": "AI & Autonomous Agents"},
            {"name": "HyperUI / Tailwind", "role": "UI Kits, Generative UX & Dashboards"}
        ],
        "concept": "Scrapes e-commerce or competitor pricing pages hourly, extracts structured product specs via local LLM without API fees, and presents change deltas in a sleek Tailwind dashboard."
    },
    {
        "title": "Air-Gapped Enterprise Knowledge & Compliance Assistant",
        "tagline": "Private document search for regulated industries (legal/finance)",
        "ingredients": [
            {"name": "sqlite-vec / Chroma", "role": "Databases, Caching & Realtime State"},
            {"name": "LLMFarm / Local LLM", "role": "AI & Autonomous Agents"},
            {"name": "Laravel Starter / Filament", "role": "SaaS Starters & App Boilerplates"}
        ],
        "concept": "An on-premise knowledge hub where sensitive enterprise contracts are embedded into an edge SQLite vector database, allowing conversational search with zero data leaving the network."
    },
    {
        "title": "Self-Operating Browser Workflow & Lead Gen Engine",
        "tagline": "Autonomous web agents delivering high-value B2B leads",
        "ingredients": [
            {"name": "Browser-Use / Agent", "role": "AI & Autonomous Agents"},
            {"name": "N8N / Workflow Tool", "role": "APIs, Workflow Automation & Webhooks"},
            {"name": "InvoBook / Billing", "role": "Ready-to-Remix Products & Self-Hosted Apps"}
        ],
        "concept": "Automates lead generation from public directories by driving headless browsers, verifying emails via webhook workers, and billing agency clients automatically via self-hosted invoicing."
    },
    {
        "title": "Edge Key-Value Cache & Sub-Millisecond Feature Flag Service",
        "tagline": "Ultra low-latency config delivery for distributed apps",
        "ingredients": [
            {"name": "DiceDB / Valkey", "role": "Databases, Caching & Realtime State"},
            {"name": "Zap / High-perf Gateway", "role": "APIs, Workflow Automation & Webhooks"},
            {"name": "Admin Dashboard", "role": "UI Kits, Generative UX & Dashboards"}
        ],
        "concept": "A distributed feature flag and remote configuration SaaS providing <1ms response times worldwide with live WebSocket updates to connected web & mobile clients."
    }
]

def load_existing_db():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {repo["full_name"]: repo for repo in data.get("repos", [])}
        except Exception as e:
            print(f"Warning: Failed to load existing database: {e}")
    return {}

def parse_markdown_sources():
    """Extract all repos from languages.md / README.md, data/repos.json, and topics.md"""
    repos = {}
    
    # 1. Seed with data/repos.json if available
    existing = load_existing_db()
    for full_name, r in existing.items():
        repos[full_name] = {
            "id": r.get("id", full_name.replace("/", "-").lower()),
            "name": r.get("name", full_name.split("/")[-1]),
            "full_name": full_name,
            "url": r.get("url", f"https://github.com/{full_name}"),
            "description": r.get("description", ""),
            "language": r.get("language", "General"),
            "topics": set(r.get("topics", [])),
            "stars": r.get("stars", 0)
        }

    # 2. Parse languages.md (or fallback to README.md)
    source_file = LANGUAGES_FILE if os.path.exists(LANGUAGES_FILE) else README_FILE
    if os.path.exists(source_file):
        with open(source_file, "r", encoding="utf-8") as f:
            content = f.read()
            
        current_lang = "General"
        for line in content.splitlines():
            m_h2 = re.match(r'^##\s+(?:<a id="[^"]+"></a>[^\s]+\s+)?(.+)', line)
            if m_h2:
                lang_name = m_h2.group(1).strip()
                # Clean up if it's our new category header
                if not any(cat["id"] in line for cat in CATEGORIES):
                    current_lang = lang_name
            m_repo = re.match(r'^- \[([^\]]+)\]\((https://github\.com/[^\)]+)\)(?: - (.*))?', line)
            if not m_repo:
                # Also support markdown table rows: | **[owner/repo](url)** | ...
                m_repo = re.match(r'\|\s*\*\*\[([^\]]+)\]\((https://github\.com/[^\)]+)\)\*\*\s*\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*([^\|]+)', line)
                if m_repo:
                    full_name = m_repo.group(1).strip()
                    url = m_repo.group(2).strip()
                    lang = m_repo.group(4).strip()
                    desc = m_repo.group(5).strip()
                    if full_name not in repos:
                        repos[full_name] = {
                            "id": full_name.replace("/", "-").lower(),
                            "name": full_name.split("/")[-1],
                            "full_name": full_name,
                            "url": url,
                            "description": desc,
                            "language": lang,
                            "topics": set(),
                            "stars": 0
                        }
                    continue

            if m_repo:
                full_name = m_repo.group(1).strip()
                url = m_repo.group(2).strip()
                desc = (m_repo.group(3) or "").strip()
                if "github.com" in url and "/" in full_name and not full_name.startswith("http"):
                    if full_name not in repos:
                        repos[full_name] = {
                            "id": full_name.replace("/", "-").lower(),
                            "name": full_name.split("/")[-1],
                            "full_name": full_name,
                            "url": url,
                            "description": desc,
                            "language": current_lang,
                            "topics": set(),
                            "stars": 0
                        }

    # 3. Augment with topics.md
    if os.path.exists(TOPICS_FILE):
        with open(TOPICS_FILE, "r", encoding="utf-8") as f:
            current_topic = ""
            for line in f:
                m_h2 = re.match(r'^##\s+(.+)', line)
                if m_h2:
                    current_topic = m_h2.group(1).strip().lower()
                m_repo = re.match(r'^- \[([^\]]+)\]\((https://github\.com/[^\)]+)\)', line)
                if m_repo and current_topic:
                    full_name = m_repo.group(1).strip()
                    if full_name in repos:
                        repos[full_name]["topics"].add(current_topic)
                        
    return repos

def classify_repo_heuristics(repo_data):
    """Accurately classifies a repository based on topics, name, language, and description."""
    text = f"{repo_data['full_name']} {repo_data['description']} {' '.join(repo_data['topics'])}".lower()
    
    # Specific specialized overrides
    if any(k in text for k in ["crawl4ai", "scraper", "spider", "scraping", "crawler"]):
        return "rag-data-ingestion", "Web Crawler & Extraction Engine", ["Pair with LLM for automated market research", "Combine with Vector DB for domain knowledge ingestion"]
    if any(k in text for k in ["sqlite-vec", "vector-search", "embeddings", "pgvector", "similarity search"]):
        return "rag-data-ingestion", "Vector Search & Retrieval Engine", ["Pair with local LLM for offline RAG", "Combine with chat UI for document assistant"]
    if any(k in text for k in ["agent", "crewai", "autogen", "ai-agent", "swarm"]):
        return "ai-agents", "Multi-Agent Coordination & Execution", ["Remix with headless browser for end-to-end task automation", "Combine with SaaS starter for specialized vertical agent"]
    if any(k in text for k in ["ollama", "vllm", "llama.cpp", "ggml", "inference", "local-llm"]):
        return "ai-agents", "Local LLM Inference Runtime", ["Power an on-premise private AI assistant", "Zero-cost background worker processing"]
    if any(k in text for k in ["starter-kit", "boilerplate", "template", "laravel-starter", "saas-starter"]):
        return "saas-starters", "Fullstack SaaS Boilerplate", ["Launch a paid micro-SaaS in 48 hours", "Remix with agent tool for automated niche solution"]
    if any(k in text for k in ["tailwind", "shadcn", "components", "hyperui", "design system"]):
        return "ui-generative-ux", "UI Component Library", ["Style custom AI dashboards and widgets", "Drop into Next.js/Laravel for rapid polished interfaces"]
    if any(k in text for k in ["canvas", "diagram", "node-editor", "flowchart", "flow-editor"]):
        return "ui-generative-ux", "Interactive Flow & Canvas Editor", ["Build a visual agent workflow builder", "Remix into visual data pipeline tool"]
    if any(k in text for k in ["valkey", "dicedb", "redis", "cache", "key-value"]):
        return "data-storage-cache", "High-Throughput In-Memory Cache", ["Sub-millisecond session & token state store", "Realtime leaderboard or pub/sub broker"]
    if any(k in text for k in ["grocy", "invobook", "invoicing", "abillander", "erp", "realproperty"]):
        return "ready-to-remix", "Self-Hosted Business Product", ["Re-skin and adapt for specialized vertical industries", "Add AI copilot layer to open-source business apps"]
    if any(k in text for k in ["pgaudit", "sentrypeer", "security", "firewall", "audit"]):
        return "security-privacy", "Security, SIP & Audit Protection", ["Integrate into compliance SaaS for automated audit reports", "Protect VoIP & web APIs from bot networks"]
    if any(k in text for k in ["n8n", "workflow", "automation", "webhook", "pipeline", "celery"]):
        return "apis-automation", "Workflow & Webhook Automation", ["Orchestrate cross-API actions triggered by webhooks", "Back-office automation micro-SaaS"]

    # Match against general categories
    best_cat_id = "devtools-terminal"
    best_score = -1
    
    for cat in CATEGORIES:
        score = 0
        for kw in cat["keywords"]:
            if kw in repo_data["topics"]:
                score += 3
            elif re.search(r'\b' + re.escape(kw) + r'\b', text):
                score += 1
        if score > best_score and score > 0:
            best_score = score
            best_cat_id = cat["id"]

    matched_cat = next(c for c in CATEGORIES if c["id"] == best_cat_id)
    default_role = matched_cat["default_role"]
    default_remix = [
        f"Combine this {default_role} with an agent orchestrator and modern UI",
        f"Remix into a developer utility or specialized SaaS workflow"
    ]
    return best_cat_id, default_role, default_remix

def call_gemini_batch_classification(batch_repos, api_key):
    """
    Optional enhancement: Uses Google Gemini API to classify repos and generate rich remix ideas.
    Falls back gracefully if network or rate limit issues occur.
    """
    if not api_key:
        return {}
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    prompt = f"""You are a product architect and software strategist.
Classify the following software repositories for a "Product Remix & Building Block" catalog.
The available categories are:
1. ai-agents (AI & Autonomous Agents)
2. rag-data-ingestion (RAG, Vector & Data Ingestion)
3. saas-starters (SaaS Starters & App Boilerplates)
4. ui-generative-ux (UI Kits, Generative UX & Dashboards)
5. apis-automation (APIs, Workflow Automation & Webhooks)
6. data-storage-cache (Databases, Caching & Realtime State)
7. security-privacy (Security, Privacy & Auth Utilities)
8. devops-infra (DevOps, Sandboxes & Cloud Infra)
9. devtools-terminal (Developer Tooling & Terminal Utilities)
10. ready-to-remix (Ready-to-Remix Products & Self-Hosted Apps)

Repositories:
{json.dumps([{'full_name': r['full_name'], 'desc': r['description'], 'topics': list(r['topics'])[:5]} for r in batch_repos], indent=2)}

Respond with ONLY a valid JSON object mapping full_name to:
{{
  "category_id": "<one of the 10 category ids>",
  "role": "<short specific 2-4 word product role, e.g. 'Vector Search Engine' or 'Local LLM Runtime'>",
  "remix_ideas": ["<Concrete product idea combining this with another tool>", "<Second actionable idea>"]
}}"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"response_mime_type": "application/json"}
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            content = data["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(content)
    except Exception as e:
        print(f"Notice: Gemini API call skipped or returned: {e}")
        return {}

def build_readme(categorized_repos, total_count):
    """Generates the revamped product-focused README.md"""
    now = datetime.utcnow().strftime("%Y-%m-%d")
    
    lines = [
        "# ⚡ Awesome Product Remix & Builder Stacks [![Awesome](https://awesome.re/badge.svg)](https://github.com/sindresorhus/awesome)",
        "",
        "> A curated, AI-classified collection of **1,700+ starred developer tools**, organized as architectural building blocks to remix, fork, and launch new products.",
        "",
        f"**Live Interactive Catalog & Remix Studio:** [Explore Live on GitHub Pages](https://bikramtuladhar.github.io/awesome-list/) ✨",
        "",
        f"![Total Tools](https://img.shields.io/badge/Cataloged_Tools-{total_count}-blue.svg?style=flat-square) ",
        "![Auto Updated](https://img.shields.io/badge/AI_Classification-Google_Gemini-4285F4.svg?style=flat-square) ",
        f"![Last Updated](https://img.shields.io/badge/Updated-{now}-success.svg?style=flat-square)",
        "",
        "---",
        "",
        "## 💡 Featured Product Remix Recipes",
        "",
        "How to combine tools from this list into actionable products:",
        ""
    ]
    
    for recipe in FEATURED_REMIX_RECIPES:
        ingredients_str = " + ".join([f"`{ing['name']}` *({ing['role']})*" for ing in recipe["ingredients"]])
        lines.extend([
            f"### 🚀 {recipe['title']}",
            f"> **{recipe['tagline']}**",
            f"- **Stack Formula:** {ingredients_str}",
            f"- **Product Blueprint:** {recipe['concept']}",
            ""
        ])

    lines.extend([
        "---",
        "",
        "## 📑 Table of Contents",
        ""
    ])
    
    for cat in CATEGORIES:
        count = len(categorized_repos[cat["id"]])
        lines.append(f"- [{cat['icon']} {cat['name']} ({count})](#{cat['id']})")
        
    lines.extend([
        "",
        "---",
        ""
    ])
    
    for cat in CATEGORIES:
        repos_in_cat = categorized_repos[cat["id"]]
        lines.extend([
            f"## <a id=\"{cat['id']}\"></a>{cat['icon']} {cat['name']} `({len(repos_in_cat)})`",
            "",
            f"> *{cat['description']}*",
            "",
            "| Tool & Repository | Role / Building Block | Language | Description | Remix Suggestion |",
            "| :--- | :--- | :--- | :--- | :--- |"
        ])
        
        for r in repos_in_cat:
            desc = (r.get("description") or "Open source tool").replace("|", "\\|").strip()
            role = r.get("role", cat["default_role"]).replace("|", "\\|")
            lang = r.get("language", "General")
            remix = r["remix_ideas"][0] if r.get("remix_ideas") else "Remix into specialized SaaS"
            remix = remix.replace("|", "\\|")
            lines.append(f"| **[{r['full_name']}]({r['url']})** | `{role}` | `{lang}` | {desc} | *{remix}* |")
            
        lines.extend(["", ""])

    lines.extend([
        "---",
        "",
        "## 🔄 Automated AI Pipeline & GitHub Actions",
        "",
        "This repository automatically synchronizes with GitHub stars using GitHub Actions and classifies entries with **Google Gemini AI**:",
        "",
        "1. **Extraction:** Discovers newly starred repositories daily via the GitHub API.",
        "2. **AI Classification:** Categorizes tools into product building blocks and generates architectural remix ideas.",
        "3. **Dual Generation:** Updates `data/repos.json`, formats this `README.md`, and deploys the interactive `index.html` catalog to **GitHub Pages**.",
        "",
        "### Adding your Gemini API Key",
        "To enable AI classification for newly starred repos in your own fork:",
        "1. Go to **Settings > Secrets and variables > Actions** in your repository.",
        "2. Add a new repository secret named `GEMINI_API_KEY` with your Google AI Studio key.",
        "",
        "---",
        "",
        "## 🤝 Contributing",
        "",
        "Have a great tool or remix recipe? Feel free to open a Pull Request or issue! Follow the [Awesome Guidelines](https://github.com/sindresorhus/awesome/blob/main/contributing.md).",
        "",
        "## 📄 License",
        "",
        "CC0 1.0 Universal - Public Domain Dedication."
    ])
    
    return "\n".join(lines)

def build_index_html(all_repos_json_str, total_count):
    """Generates the interactive single-page Web Catalog & Remix Studio."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Awesome Product Remix & Builder Stacks</title>
  <meta name="description" content="1,700+ curated developer tools categorized as product building blocks to remix and build new apps.">
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');
    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    code, pre, .font-mono {{
      font-family: 'JetBrains Mono', monospace;
    }}
    .glass-card {{
      background: rgba(255, 255, 255, 0.85);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(226, 232, 240, 0.8);
    }}
    .dark .glass-card {{
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(51, 65, 85, 0.6);
    }}
    .custom-scroll::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    .custom-scroll::-webkit-scrollbar-thumb {{
      background: #cbd5e1;
      border-radius: 4px;
    }}
    .dark .custom-scroll::-webkit-scrollbar-thumb {{
      background: #475569;
    }}
  </style>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          colors: {{
            brand: {{
              50: '#f0fdf4',
              500: '#10b981',
              600: '#059669',
              700: '#047857',
            }}
          }}
        }}
      }}
    }}
  </script>
</head>
<body class="bg-slate-50 dark:bg-slate-950 text-slate-800 dark:text-slate-100 min-h-screen transition-colors duration-200">

  <!-- Header -->
  <header class="border-b border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur sticky top-0 z-40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <span class="text-2xl p-2 bg-emerald-100 dark:bg-emerald-950/60 rounded-xl">⚡</span>
        <div>
          <h1 class="font-bold text-lg leading-tight tracking-tight flex items-center gap-2">
            Awesome Product Remix
            <span class="bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 text-xs px-2 py-0.5 rounded-full font-semibold border border-emerald-500/20">AI Classified</span>
          </h1>
          <p class="text-xs text-slate-500 dark:text-slate-400">1,700+ Developer Tools Ready to Stitch & Launch</p>
        </div>
      </div>
      
      <div class="flex items-center space-x-3">
        <button id="themeToggle" class="p-2 rounded-lg text-slate-500 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-slate-800 transition" title="Toggle Dark Mode">
          <i data-lucide="moon" class="w-5 h-5 dark:hidden"></i>
          <i data-lucide="sun" class="w-5 h-5 hidden dark:block"></i>
        </button>
        <a href="https://github.com/bikramtuladhar/awesome-list" target="_blank" rel="noopener noreferrer" class="flex items-center gap-2 px-3.5 py-1.5 text-sm font-medium bg-slate-900 hover:bg-slate-800 text-white dark:bg-white dark:text-slate-900 dark:hover:bg-slate-100 rounded-lg shadow-sm transition">
          <i data-lucide="github" class="w-4 h-4"></i>
          <span>GitHub</span>
        </a>
      </div>
    </div>
  </header>

  <!-- Hero & Remix Generator Studio -->
  <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 pb-4">
    <div class="relative rounded-2xl overflow-hidden p-6 sm:p-8 bg-gradient-to-br from-emerald-600 via-teal-700 to-indigo-900 text-white shadow-xl">
      <div class="relative z-10 max-w-3xl">
        <div class="inline-flex items-center gap-2 bg-white/10 backdrop-blur-md px-3 py-1 rounded-full text-xs font-semibold mb-4 text-emerald-100 border border-white/15">
          <span>🧩 Lego-Brick Product Architecture</span>
        </div>
        <h2 class="text-2xl sm:text-4xl font-extrabold tracking-tight mb-3">
          Stop reinventing the wheel. Remix awesome tools into new products.
        </h2>
        <p class="text-emerald-100 text-sm sm:text-base leading-relaxed mb-6">
          Every tool below is a specialized building block—from local AI inference and web scrapers to edge SQLite vector search and auth boilerplates.
        </p>

        <!-- Remix Generator Bar -->
        <div class="flex flex-wrap items-center gap-3">
          <button id="randomRemixBtn" class="flex items-center gap-2 px-5 py-2.5 bg-white text-slate-900 hover:bg-emerald-50 rounded-xl font-bold text-sm shadow-lg transition transform active:scale-95">
            <i data-lucide="sparkles" class="w-4 h-4 text-emerald-600"></i>
            <span>🎲 Surprise Me: Generate a Product Remix</span>
          </button>
          <button id="viewRecipesBtn" class="flex items-center gap-2 px-4 py-2.5 bg-white/15 hover:bg-white/20 text-white border border-white/20 rounded-xl font-semibold text-sm backdrop-blur transition">
            <i data-lucide="layers" class="w-4 h-4"></i>
            <span>View Featured Blueprints</span>
          </button>
          <div id="remixBenchBadge" class="hidden items-center gap-2 px-3 py-1.5 bg-emerald-400/20 border border-emerald-300/30 rounded-xl text-xs font-mono">
            <span id="remixBenchCount">0</span> in your Remix Bench
          </div>
        </div>
      </div>
    </div>

    <!-- Live Remix Idea Modal / Card (Dynamic) -->
    <div id="remixIdeaCard" class="hidden mt-4 p-5 rounded-2xl bg-white dark:bg-slate-900 border border-emerald-500/30 shadow-lg animate-in fade-in duration-200">
      <div class="flex items-start justify-between">
        <div>
          <span class="text-xs uppercase font-bold tracking-wider text-emerald-600 dark:text-emerald-400">💡 Generated Product Concept</span>
          <h3 id="remixTitle" class="text-xl font-bold mt-1 text-slate-900 dark:text-white"></h3>
          <p id="remixTagline" class="text-sm text-slate-500 dark:text-slate-400 mb-3"></p>
        </div>
        <button id="closeRemixCard" class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 p-1">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-3 my-3" id="remixIngredients"></div>
      <div class="p-3.5 bg-slate-50 dark:bg-slate-800/60 rounded-xl text-sm border border-slate-200 dark:border-slate-700/60">
        <span class="font-semibold text-slate-700 dark:text-slate-300">Architecture & Monetization:</span>
        <p id="remixConcept" class="text-slate-600 dark:text-slate-400 mt-1"></p>
      </div>
    </div>
  </section>

  <!-- Filter & Search Controls -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="flex flex-col md:flex-row gap-4 items-center justify-between mb-6">
      <!-- Search Input -->
      <div class="relative w-full md:w-96">
        <i data-lucide="search" class="w-4 h-4 absolute left-3.5 top-3.5 text-slate-400"></i>
        <input 
          type="text" 
          id="searchInput" 
          placeholder="Search by name, role, topic, or keyword..."
          class="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-500 text-sm shadow-sm"
        />
      </div>

      <!-- Controls Right: Language filter & Stats -->
      <div class="flex items-center gap-3 w-full md:w-auto justify-between md:justify-end">
        <select id="langSelect" class="px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 shadow-sm">
          <option value="ALL">All Languages</option>
        </select>
        
        <div class="text-xs font-mono text-slate-500 dark:text-slate-400 whitespace-nowrap bg-slate-100 dark:bg-slate-800/80 px-3 py-2 rounded-xl">
          Showing <span id="visibleCount" class="font-bold text-slate-900 dark:text-white">0</span> of <span class="font-bold">{total_count}</span>
        </div>
      </div>
    </div>

    <!-- Category Filter Tabs -->
    <div class="flex items-center gap-2 overflow-x-auto custom-scroll pb-3 mb-6" id="categoryTabs">
      <button data-cat="ALL" class="cat-tab active px-3.5 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition bg-emerald-600 text-white shadow-sm">
        All Building Blocks
      </button>
    </div>

    <!-- Tool Cards Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" id="toolGrid">
      <!-- Injected by JavaScript -->
    </div>

    <!-- Empty state -->
    <div id="noResults" class="hidden text-center py-16">
      <i data-lucide="package-search" class="w-12 h-12 text-slate-300 dark:text-slate-700 mx-auto mb-3"></i>
      <h3 class="font-bold text-slate-700 dark:text-slate-300">No matching tools found</h3>
      <p class="text-sm text-slate-500">Try adjusting your search query or switching categories.</p>
    </div>
  </main>

  <!-- Repo Detail Modal -->
  <div id="detailModal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm">
    <div class="bg-white dark:bg-slate-900 rounded-2xl max-w-xl w-full p-6 shadow-2xl border border-slate-200 dark:border-slate-800 max-h-[90vh] overflow-y-auto custom-scroll">
      <div class="flex items-start justify-between mb-4">
        <div>
          <span id="modalCategory" class="text-xs font-semibold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider"></span>
          <h2 id="modalTitle" class="text-xl font-bold text-slate-900 dark:text-white mt-0.5"></h2>
        </div>
        <button id="closeModal" class="p-1 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <div class="space-y-4">
        <div>
          <span class="text-xs font-semibold text-slate-400 uppercase">Product Building Block Role</span>
          <div id="modalRole" class="mt-1 font-mono text-sm px-3 py-1.5 bg-slate-100 dark:bg-slate-800 rounded-lg inline-block text-emerald-700 dark:text-emerald-300"></div>
        </div>

        <div>
          <span class="text-xs font-semibold text-slate-400 uppercase">Description</span>
          <p id="modalDesc" class="mt-1 text-sm text-slate-600 dark:text-slate-300 leading-relaxed"></p>
        </div>

        <div>
          <span class="text-xs font-semibold text-slate-400 uppercase">💡 Product Remix Opportunities</span>
          <ul id="modalRemix" class="mt-2 space-y-2 text-sm text-slate-700 dark:text-slate-300"></ul>
        </div>

        <div>
          <span class="text-xs font-semibold text-slate-400 uppercase">Tags & Topics</span>
          <div id="modalTopics" class="mt-2 flex flex-wrap gap-1.5"></div>
        </div>

        <div class="pt-4 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">
          <button id="modalCopyMarkdown" class="flex items-center gap-1.5 px-3 py-2 text-xs font-medium text-slate-700 dark:text-slate-200 bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 rounded-lg transition">
            <i data-lucide="copy" class="w-3.5 h-3.5"></i>
            <span>Copy Markdown</span>
          </button>
          
          <a id="modalGitHubLink" href="#" target="_blank" rel="noopener noreferrer" class="flex items-center gap-1.5 px-4 py-2 text-xs font-bold text-white bg-slate-900 hover:bg-slate-800 dark:bg-emerald-600 dark:hover:bg-emerald-500 rounded-lg shadow-sm transition">
            <span>View on GitHub</span>
            <i data-lucide="external-link" class="w-3.5 h-3.5"></i>
          </a>
        </div>
      </div>
    </div>
  </div>

  <footer class="mt-16 border-t border-slate-200 dark:border-slate-800 py-8 text-center text-xs text-slate-500">
    <p>Curated by <a href="https://github.com/bikramtuladhar" class="underline font-semibold">Bikram Tuladhar</a>. Automated with Google Gemini & GitHub Actions.</p>
  </footer>

  <!-- Application Logic -->
  <script>
    // Embedded Data Source
    const DATA = {all_repos_json_str};
    const CATEGORIES = {json.dumps(CATEGORIES)};
    const FEATURED_RECIPES = {json.dumps(FEATURED_REMIX_RECIPES)};

    let currentCategory = 'ALL';
    let currentLanguage = 'ALL';
    let searchQuery = '';
    let remixBench = new Set();

    // Elements
    const toolGrid = document.getElementById('toolGrid');
    const searchInput = document.getElementById('searchInput');
    const langSelect = document.getElementById('langSelect');
    const categoryTabs = document.getElementById('categoryTabs');
    const visibleCount = document.getElementById('visibleCount');
    const noResults = document.getElementById('noResults');
    const randomRemixBtn = document.getElementById('randomRemixBtn');
    const viewRecipesBtn = document.getElementById('viewRecipesBtn');
    const remixIdeaCard = document.getElementById('remixIdeaCard');
    const closeRemixCard = document.getElementById('closeRemixCard');
    const detailModal = document.getElementById('detailModal');
    const themeToggle = document.getElementById('themeToggle');

    // Theme Setup
    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {{
      document.documentElement.classList.add('dark');
    }} else {{
      document.documentElement.classList.remove('dark');
    }}

    themeToggle.addEventListener('click', () => {{
      document.documentElement.classList.toggle('dark');
      localStorage.theme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
      lucide.createIcons();
    }});

    // Setup Category Tabs
    CATEGORIES.forEach(cat => {{
      const count = DATA.repos.filter(r => r.category_id === cat.id).length;
      const btn = document.createElement('button');
      btn.dataset.cat = cat.id;
      btn.className = 'cat-tab px-3.5 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-300 hover:border-emerald-500';
      btn.innerHTML = `${{cat.icon}} ${{cat.name}} <span class="ml-1 opacity-60">(${{count}})</span>`;
      btn.onclick = () => selectCategory(cat.id);
      categoryTabs.appendChild(btn);
    }});

    // Populate Languages Dropdown
    const languages = Array.from(new Set(DATA.repos.map(r => r.language).filter(l => l && l !== 'General'))).sort();
    languages.forEach(lang => {{
      const opt = document.createElement('option');
      opt.value = lang;
      opt.textContent = lang;
      langSelect.appendChild(opt);
    }});

    function selectCategory(catId) {{
      currentCategory = catId;
      document.querySelectorAll('.cat-tab').forEach(t => {{
        if (t.dataset.cat === catId) {{
          t.className = 'cat-tab px-3.5 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition bg-emerald-600 text-white shadow-sm';
        }} else {{
          t.className = 'cat-tab px-3.5 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-300 hover:border-emerald-500';
        }}
      }});
      renderTools();
    }}

    // Render Filtered Tools
    function renderTools() {{
      const q = searchQuery.toLowerCase().trim();
      const filtered = DATA.repos.filter(repo => {{
        const matchesCat = (currentCategory === 'ALL' || repo.category_id === currentCategory);
        const matchesLang = (currentLanguage === 'ALL' || repo.language === currentLanguage);
        const textToSearch = `${{repo.full_name}} ${{repo.role}} ${{repo.description}} ${{repo.topics.join(' ')}}`.toLowerCase();
        const matchesQuery = !q || textToSearch.includes(q);
        return matchesCat && matchesLang && matchesQuery;
      }});

      visibleCount.textContent = filtered.length;
      noResults.classList.toggle('hidden', filtered.length > 0);
      toolGrid.innerHTML = '';

      filtered.slice(0, 150).forEach(repo => {{
        const cat = CATEGORIES.find(c => c.id === repo.category_id) || {{ icon: '📦', name: 'DevTools' }};
        const card = document.createElement('div');
        card.className = 'glass-card p-5 rounded-2xl flex flex-col justify-between hover:border-emerald-500/50 hover:shadow-lg transition-all duration-200 group relative';
        
        card.innerHTML = `
          <div>
            <div class="flex items-start justify-between gap-2 mb-2">
              <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border border-emerald-500/20">
                <span>${{cat.icon}}</span>
                <span class="truncate max-w-[140px]">${{repo.role}}</span>
              </span>
              <span class="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400">
                ${{repo.language || 'General'}}
              </span>
            </div>
            
            <h3 class="font-bold text-base text-slate-900 dark:text-white group-hover:text-emerald-600 dark:group-hover:text-emerald-400 transition cursor-pointer flex items-center gap-1.5" onclick="openModal('${{repo.full_name}}')">
              <span class="truncate">${{repo.full_name}}</span>
              <i data-lucide="info" class="w-3.5 h-3.5 opacity-0 group-hover:opacity-100 transition text-emerald-500"></i>
            </h3>
            
            <p class="text-xs text-slate-600 dark:text-slate-400 line-clamp-2 mt-1.5 leading-relaxed">
              ${{repo.description || 'Open source tool for developer workflows.'}}
            </p>
          </div>

          <div class="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">
            <button onclick="toggleRemixBench('${{repo.full_name}}')" class="text-xs flex items-center gap-1 text-slate-500 hover:text-emerald-600 dark:hover:text-emerald-400 transition">
              <i data-lucide="plus-circle" class="w-3.5 h-3.5"></i>
              <span>Remix</span>
            </button>
            <a href="${{repo.url}}" target="_blank" rel="noopener noreferrer" class="text-xs font-semibold flex items-center gap-1 text-slate-700 dark:text-slate-300 hover:text-emerald-600 dark:hover:text-emerald-400 transition">
              <span>GitHub</span>
              <i data-lucide="external-link" class="w-3.5 h-3.5"></i>
            </a>
          </div>
        `;
        toolGrid.appendChild(card);
      }});

      lucide.createIcons();
    }}

    // Open Detail Modal
    window.openModal = function(fullName) {{
      const repo = DATA.repos.find(r => r.full_name === fullName);
      if (!repo) return;
      const cat = CATEGORIES.find(c => c.id === repo.category_id) || {{ icon: '📦', name: 'DevTools' }};

      document.getElementById('modalCategory').textContent = `${{cat.icon}} ${{cat.name}}`;
      document.getElementById('modalTitle').textContent = repo.full_name;
      document.getElementById('modalRole').textContent = repo.role;
      document.getElementById('modalDesc').textContent = repo.description || 'No description provided.';
      
      const remixList = document.getElementById('modalRemix');
      remixList.innerHTML = '';
      (repo.remix_ideas || ['Remix this building block with an AI agent or dashboard']).forEach(idea => {{
        const li = document.createElement('li');
        li.className = 'flex items-start gap-2 p-2.5 rounded-xl bg-emerald-500/5 border border-emerald-500/20';
        li.innerHTML = `<span class="text-emerald-600 dark:text-emerald-400 font-bold">↳</span> <span>${{idea}}</span>`;
        remixList.appendChild(li);
      }});

      const topicsContainer = document.getElementById('modalTopics');
      topicsContainer.innerHTML = '';
      (repo.topics || []).slice(0, 10).forEach(t => {{
        const span = document.createElement('span');
        span.className = 'text-xs px-2 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400';
        span.textContent = `#${{t}}`;
        topicsContainer.appendChild(span);
      }});

      document.getElementById('modalGitHubLink').href = repo.url;
      document.getElementById('modalCopyMarkdown').onclick = () => {{
        const md = `- [${{repo.full_name}}](${{repo.url}}) - ${{repo.description}}`;
        navigator.clipboard.writeText(md);
        alert('Copied Markdown link to clipboard!');
      }};

      detailModal.classList.remove('hidden');
      lucide.createIcons();
    }};

    document.getElementById('closeModal').onclick = () => detailModal.classList.add('hidden');
    detailModal.onclick = (e) => {{ if (e.target === detailModal) detailModal.classList.add('hidden'); }};

    // Remix Studio Logic
    function displayRemix(recipe) {{
      document.getElementById('remixTitle').textContent = recipe.title;
      document.getElementById('remixTagline').textContent = recipe.tagline;
      document.getElementById('remixConcept').textContent = recipe.concept;

      const ingContainer = document.getElementById('remixIngredients');
      ingContainer.innerHTML = '';
      recipe.ingredients.forEach(ing => {{
        const div = document.createElement('div');
        div.className = 'p-3 rounded-xl bg-slate-100 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700';
        div.innerHTML = `
          <span class="text-[10px] font-bold uppercase tracking-wider text-emerald-600 dark:text-emerald-400 block">${{ing.role}}</span>
          <span class="font-bold text-sm text-slate-900 dark:text-white block mt-0.5">${{ing.name}}</span>
        `;
        ingContainer.appendChild(div);
      }});

      remixIdeaCard.classList.remove('hidden');
      remixIdeaCard.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
      lucide.createIcons();
    }}

    randomRemixBtn.addEventListener('click', () => {{
      // Either select a curated one or generate a procedural remix
      const recipe = FEATURED_RECIPES[Math.floor(Math.random() * FEATURED_RECIPES.length)];
      displayRemix(recipe);
    }});

    viewRecipesBtn.addEventListener('click', () => {{
      displayRemix(FEATURED_RECIPES[0]);
    }});

    closeRemixCard.addEventListener('click', () => {{
      remixIdeaCard.classList.add('hidden');
    }});

    window.toggleRemixBench = function(fullName) {{
      if (remixBench.has(fullName)) {{
        remixBench.delete(fullName);
      }} else {{
        remixBench.add(fullName);
      }}
      const badge = document.getElementById('remixBenchBadge');
      const count = document.getElementById('remixBenchCount');
      count.textContent = remixBench.size;
      badge.classList.toggle('hidden', remixBench.size === 0);
      badge.classList.toggle('flex', remixBench.size > 0);
    }};

    // Event Listeners for Filters
    searchInput.addEventListener('input', (e) => {{
      searchQuery = e.target.value;
      renderTools();
    }});

    langSelect.addEventListener('change', (e) => {{
      currentLanguage = e.target.value;
      renderTools();
    }});

    // Initial Render
    renderTools();
  </script>
</body>
</html>
"""

def main():
    print("🚀 Starting Awesome Product Remix & Builder Stacks Engine...")
    
    # 1. Load existing DB
    existing_db = load_existing_db()
    print(f"📦 Loaded {len(existing_db)} existing cached repositories.")
    
    # 2. Parse sources
    parsed_repos = parse_markdown_sources()
    print(f"📄 Found {len(parsed_repos)} repositories from markdown files.")
    
    # 3. Classify & Enrich
    gemini_api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    categorized_repos = defaultdict(list)
    all_repos_list = []
    
    unclassified_batch = []
    
    for full_name, repo_data in parsed_repos.items():
        if full_name in existing_db and existing_db[full_name].get("category_id"):
            entry = existing_db[full_name]
            # Ensure topics are set
            entry["topics"] = list(repo_data["topics"])
            cat_id = entry["category_id"]
        else:
            cat_id, role, remix_ideas = classify_repo_heuristics(repo_data)
            entry = {
                "id": repo_data["id"],
                "name": repo_data["name"],
                "full_name": repo_data["full_name"],
                "url": repo_data["url"],
                "description": repo_data["description"],
                "language": repo_data["language"],
                "topics": list(repo_data["topics"]),
                "category_id": cat_id,
                "role": role,
                "remix_ideas": remix_ideas
            }
            if gemini_api_key:
                unclassified_batch.append(entry)
                
        categorized_repos[cat_id].append(entry)
        all_repos_list.append(entry)

    # Optional Gemini AI enrichment if API key is present
    if gemini_api_key and unclassified_batch:
        print(f"🤖 Calling Google Gemini API to enrich {len(unclassified_batch)} new repos...")
        for i in range(0, min(len(unclassified_batch), 50), 10):
            batch = unclassified_batch[i:i+10]
            gemini_results = call_gemini_batch_classification(batch, gemini_api_key)
            for repo in batch:
                if repo["full_name"] in gemini_results:
                    res = gemini_results[repo["full_name"]]
                    if res.get("category_id") in [c["id"] for c in CATEGORIES]:
                        repo["category_id"] = res["category_id"]
                    if res.get("role"):
                        repo["role"] = res["role"]
                    if res.get("remix_ideas"):
                        repo["remix_ideas"] = res["remix_ideas"]

    # 4. Save to data/repos.json
    db_payload = {
        "generated_at": datetime.utcnow().isoformat(),
        "total_count": len(all_repos_list),
        "repos": all_repos_list
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(db_payload, f, indent=2)
    print(f"✅ Saved database to {DATA_FILE}")

    # 5. Generate README.md
    readme_content = build_readme(categorized_repos, len(all_repos_list))
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"✅ Generated revamped {README_FILE}")

    # 6. Generate index.html
    html_content = build_index_html(json.dumps(db_payload), len(all_repos_list))
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ Generated interactive web catalog {INDEX_FILE}")

    print("\n🎉 Total Revamp Complete!")
    for cat in CATEGORIES:
        print(f"  {cat['icon']} {cat['name']}: {len(categorized_repos[cat['id']])} repos")

if __name__ == "__main__":
    main()
