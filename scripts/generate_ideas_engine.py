#!/usr/bin/env python3
"""
Product Ideas & Swap Engine Generator
-------------------------------------
Maps 100% of the 1,729+ starred repositories into 40 functional component slots
and 40 Product Remix Ideas. Supports:
1. Interactive Slot Swapping (swap any repository with an equivalent alternative from your stars)
2. Cross-Project Idea Combiner (combine any 2+ product ideas into a brand-new super-product)
3. 100% Coverage Verification across all starred repositories
"""

import os
import json
import re
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "repos.json")
IDEAS_JSON_FILE = os.path.join(BASE_DIR, "data", "ideas.json")
IDEAS_MD_FILE = os.path.join(BASE_DIR, "IDEAS.md")

SPECIFIC_SLOTS = [
    ("slot_llm_local", "Local & Edge LLM Inference Engine", "🧠", [
        "llama.cpp", "ggml", "ollama", "vllm", "bitnet", "powerinfer", "llmfarm",
        "esp32-llm", "local-llm", "onnx", "mediapipe", "gguf", "inference"
    ]),
    ("slot_voice_audio", "Voice, Speech-to-Text & Audio Engine", "🎙️", [
        "whisper", "moonshine", "voice", "speech", "audio", "tts", "stt", "sound",
        "music", "webrtc", "sip"
    ]),
    ("slot_mcp_protocol", "Model Context Protocol (MCP) & Agent Skills", "🔌", [
        "mcp", "model-context-protocol", "tool-use", "function-calling", "agent-skills", "anthropic"
    ]),
    ("slot_multi_agent", "Multi-Agent Orchestrator & Autonomous Swarms", "🤖", [
        "ai-agents", "agents", "ai-agent", "crewai", "autogen", "swarm", "langgraph",
        "autonomous", "agent"
    ]),
    ("slot_ai_coding", "AI Coding Copilot, PR Review & Code Gen", "💻", [
        "code-review", "copilot", "coding-assistant", "codegen", "cursor", "claude-code",
        "aider", "swe", "claude"
    ]),
    ("slot_computer_vision", "Computer Vision, Image & Video AI", "👁️", [
        "computer-vision", "video", "image-processing", "opencv", "diffusion", "yolo",
        "ocr", "tesseract", "ffmpeg"
    ]),
    ("slot_ai_gateway", "AI Gateway, LLM Proxy & Token Router", "⚡", [
        "gomodel", "litellm", "ai-gateway", "openai", "chatgpt", "prompt", "llm-proxy",
        "llm", "gpt"
    ]),
    ("slot_ml_training", "Deep Learning, Fine-Tuning & ML Framework", "🔬", [
        "unsloth", "deep-learning", "machine-learning", "reinforcement-learning",
        "pytorch", "tensorflow", "jupyter", "neural", "ai"
    ]),
    ("slot_web_scraper", "Web Scraper, Headless Browser & Crawler", "🕷️", [
        "crawler", "scraper", "scraping", "crawl4ai", "puppeteer", "playwright",
        "spider", "dataflowkit", "crawl"
    ]),
    ("slot_vector_rag", "Vector Database & Hybrid RAG Search", "🔍", [
        "vector", "sqlite-vec", "milvus", "infinity", "pg_embedding", "embeddings",
        "rag", "zincsearch", "elasticsearch", "search-engine", "search"
    ]),
    ("slot_pdf_docs", "PDF, Document Processing & Knowledge Graphs", "📄", [
        "pdf", "docx", "document", "signature", "markdown", "knowledge-base",
        "logseq", "wiki", "notes", "obsidian", "documentation"
    ]),
    ("slot_laravel_erp", "Laravel Business App, Invoicing & CRM", "💼", [
        "invobook", "abillander", "realproperty", "invoice", "invoicing", "erp",
        "crm", "filament", "accounting", "pos"
    ]),
    ("slot_laravel_core", "Laravel Ecosystem, Starters & Packages", "🧱", [
        "laravel", "blade", "sanctum", "socialite", "beautymail", "eloquent",
        "artisan", "livewire"
    ]),
    ("slot_auth_identity", "Authentication, Passkeys, OIDC & Multi-Tenancy", "🔐", [
        "auth", "authentication", "oauth", "passkey", "hanko", "supertokens",
        "pocket-id", "multi-tenant", "jwt", "sso", "identity", "rbac"
    ]),
    ("slot_billing_metering", "Usage Metering, Subscriptions & Billing", "💳", [
        "openmeter", "lago", "billing", "stripe", "payment", "fintech",
        "subscription", "feature-flags", "flipt", "pricing"
    ]),
    ("slot_tailwind_ui", "Tailwind CSS, Component Kits & Design Systems", "🎨", [
        "tailwindcss", "tailwind", "hyperui", "shadcn", "css", "ui-components",
        "design-system", "icons", "animation", "ui"
    ]),
    ("slot_react_nextjs", "React, Next.js & Modern Frontend Stacks", "⚛️", [
        "react", "nextjs", "next.js", "redux", "webpack", "vite", "astro",
        "remix", "shadcn-ui"
    ]),
    ("slot_vue_svelte", "Vue, Svelte & Reactive UI Frameworks", "✨", [
        "vue", "vuejs", "nuxt", "svelte", "solidjs", "htmx", "alpinejs", "angular"
    ]),
    ("slot_canvas_dataviz", "Interactive Canvas, 3D WebGL & Data Visualization", "📊", [
        "canvas", "diagram", "flow", "chart", "dataviz", "d3", "webgl", "3d",
        "babylon", "unity", "game", "imgui", "visualization"
    ]),
    ("slot_mobile_cross", "Mobile, iOS, Android & Cross-Platform Apps", "📱", [
        "android", "ios", "swift", "kotlin", "flutter", "dart", "react-native",
        "electron", "tauri", "mobile"
    ]),
    ("slot_postgres_sql", "PostgreSQL Extensions, Distributed SQL & Migrations", "🐘", [
        "postgresql", "postgres", "yugabyte", "orioledb", "pgcopydb", "age",
        "columnar", "mysql", "percona", "sql", "database", "orm"
    ]),
    ("slot_sqlite_edge", "SQLite Engines, Embedded DBs & Local Storage", "🗄️", [
        "sqlite", "letos", "duckdb", "turso", "libsql", "embedded-database",
        "local-first", "storage"
    ]),
    ("slot_redis_kv", "In-Memory Cache, Redis/Valkey & KV Engines", "🚀", [
        "redis", "valkey", "dicedb", "dragonfly", "cachegrand", "cache",
        "key-value", "memcached", "raft"
    ]),
    ("slot_realtime_api", "Realtime Pub/Sub, WebSockets, gRPC & API Gateways", "📡", [
        "mercure", "websocket", "grpc", "graphql", "huma", "chi", "rest-api",
        "api", "pubsub", "http", "proxy", "reverse-proxy"
    ]),
    ("slot_workflow_queue", "Workflow Orchestration, Job Queues & Pipelines", "🔄", [
        "automation", "workflow", "pipeline", "tekton", "queue", "ftl", "cron",
        "scheduler", "webhook", "n8n", "kafka"
    ]),
    ("slot_k8s_cloud", "Kubernetes, GitOps, Service Mesh & Cloud Native", "☸️", [
        "kubernetes", "k8s", "k8sgpt", "helm", "fluxcd", "argocd", "istio",
        "cloud-native", "serverless", "aws", "cloud", "microservices"
    ]),
    ("slot_terraform_iac", "Terraform, Proxmox, IaC & Server Provisioning", "🏗️", [
        "terraform", "proxmox", "ansible", "iac", "devops", "cloudflare",
        "nginx", "traefik", "dns", "vpn"
    ]),
    ("slot_docker_sandbox", "Docker, Unikernels, MicroVMs & Container Runtimes", "📦", [
        "docker", "container", "copacetic", "nanos", "wasm", "webassembly",
        "sandbox", "devcontainer", "virtualization"
    ]),
    ("slot_observability", "Observability, eBPF Telemetry, Logs & Analytics", "📈", [
        "monitoring", "pixie", "ebpf", "prometheus", "grafana", "opentelemetry",
        "analytics", "vince", "tracetest", "logging", "metrics"
    ]),
    ("slot_app_security", "Cybersecurity, Pentesting, Bot Defense & Auditing", "🛡️", [
        "security", "security-tools", "trivy", "crowdsec", "anubis", "sentrypeer",
        "pgaudit", "vulnapi", "pentest", "firewall", "encryption", "cybersecurity", "privacy"
    ]),
    ("slot_terminal_tui", "Modern Terminals, Web Shells & TUI Dashboards", "⌨️", [
        "terminal", "ttyd", "waveterm", "tui", "shell", "bash", "zsh", "cli",
        "facad", "gama", "clipboard", "command-line"
    ]),
    ("slot_macos_linux", "macOS, Linux Kernel, System Utilities & Hardware", "🍎", [
        "macos", "sketchybar", "linux", "kernel", "assembly", "arm64",
        "raspberry-pi", "arduino", "iot", "embedded", "windows"
    ]),
    ("slot_git_devtools", "Git Workflows, Compilers, Linters & Dev Productivity", "🛠️", [
        "git", "github", "github-actions", "compiler", "linter", "debugger",
        "testing", "benchmark", "developer-tools", "code-quality"
    ]),
    ("slot_selfhosted_apps", "Turn-Key Self-Hosted Apps, Media & Productivity", "🏠", [
        "self-hosted", "grocy", "papercups", "cms", "blog", "ecommerce", "media", "social"
    ])
]

FALLBACK_SLOTS = [
    ("slot_php_modern", "PHP Frameworks, Profilers & Server Runtimes", "🐘", [
        "php", "php-spx", "symfony", "composer", "wordpress"
    ]),
    ("slot_go_systems", "High-Concurrency Go Libraries & Microservice Tools", "🐹", [
        "golang", "go"
    ]),
    ("slot_rust_zig", "Zero-Cost Rust, Zig & C/C++ Systems Building Blocks", "🦀", [
        "rust", "zig", "c++", "cpp", "c"
    ]),
    ("slot_python_data", "Python Data Science, Automation & Scripting Libraries", "🐍", [
        "python", "data-science", "data-analysis", "pandas", "numpy"
    ]),
    ("slot_js_ts_core", "TypeScript / Node.js Runtime Utilities & SDKs", "🟨", [
        "typescript", "javascript", "nodejs", "deno", "bun"
    ]),
    ("slot_curated_playbooks", "Architecture Playbooks, Engineering Guides & Reference Stacks", "📚", [
        "awesome", "awesome-list", "education", "books", "interview", "roadmap", "architecture"
    ])
]

ALL_SLOTS = SPECIFIC_SLOTS + FALLBACK_SLOTS

# 40 Comprehensive Product Ideas (Every single one of the 40 slots is primary in at least one idea,
# and each idea combines 3 complementary slots so you can swap any repo inside any slot!)
PRODUCT_IDEAS = [
    {
        "id": "idea-01",
        "title": "On-Premise Voice AI Receptionist & SIP Shield",
        "domain": "AI & Voice Automation",
        "tagline": "Zero-cloud-cost voice booking with built-in VoIP fraud defense for clinics & law firms",
        "primary_slot": "slot_voice_audio",
        "slots": ["slot_voice_audio", "slot_app_security", "slot_laravel_erp"],
        "architecture": "Connects to a SIP trunk where VoIP security tools filter robocalls, local speech-to-text transcribes caller intent in <100ms, and a Laravel/Filament backend books appointments automatically.",
        "monetization": "$149–$299/mo flat fee appliance for dental clinics, law offices, and HVAC contractors."
    },
    {
        "id": "idea-02",
        "title": "Offline Cross-Platform AI Copilot & Edge Model Runner",
        "domain": "Local AI & Edge Compute",
        "tagline": "Run quantized 1-bit & GGUF LLMs privately across MacBooks, iPhones, and embedded hardware",
        "primary_slot": "slot_llm_local",
        "slots": ["slot_llm_local", "slot_mobile_cross", "slot_sqlite_edge"],
        "architecture": "Executes quantized local LLMs on consumer CPUs/GPUs using C++/GGML runtimes, stores chat embeddings in local SQLite, and wraps the experience in a sleek native mobile/desktop shell.",
        "monetization": "$49 one-time native license or $19/mo enterprise air-gapped seat."
    },
    {
        "id": "idea-03",
        "title": "Universal MCP Server Hub & Enterprise Tool Bridge",
        "domain": "AI Agents & MCP",
        "tagline": "One-click Model Context Protocol gateway connecting Claude/Cursor to internal databases & APIs",
        "primary_slot": "slot_mcp_protocol",
        "slots": ["slot_mcp_protocol", "slot_auth_identity", "slot_postgres_sql"],
        "architecture": "Exposes standardized MCP tools over secure OIDC/Passkey authentication so AI assistants can safely query production SQL schemas, trigger workflows, and inspect logs with role-based guardrails.",
        "monetization": "$29/developer/mo team governance subscription."
    },
    {
        "id": "idea-04",
        "title": "Autonomous Multi-Agent B2B Research & Outreach Swarm",
        "domain": "Autonomous Agent Swarms",
        "tagline": "Self-coordinating agent teams that scrape prospects, qualify leads, and draft personalized pitches",
        "primary_slot": "slot_multi_agent",
        "slots": ["slot_multi_agent", "slot_web_scraper", "slot_workflow_queue"],
        "architecture": "Orchestrates specialized research, verification, and copywriting agents that crawl target company sites, enrich data in background queues, and push verified leads into CRM pipelines.",
        "monetization": "$199–$499/mo B2B growth automation SaaS."
    },
    {
        "id": "idea-05",
        "title": "Automated PR Security Reviewer & Codebase Refactoring Bot",
        "domain": "AI DevTools",
        "tagline": "Self-hosted AI code reviewer that catches security flaws, writes unit tests, and patches PRs",
        "primary_slot": "slot_ai_coding",
        "slots": ["slot_ai_coding", "slot_git_devtools", "slot_docker_sandbox"],
        "architecture": "Triggers on every GitHub pull request, spins up an ephemeral container sandbox to run static analysis + LLM review, and commits suggested fixes directly to the feature branch.",
        "monetization": "$15/repo/mo or $99/mo unlimited self-hosted team license."
    },
    {
        "id": "idea-06",
        "title": "Autopilot Video Studio & Visual Defect Inspector",
        "domain": "Computer Vision & Media",
        "tagline": "Automated video rendering, OCR subtitle generation, and duplicate media asset management",
        "primary_slot": "slot_computer_vision",
        "slots": ["slot_computer_vision", "slot_voice_audio", "slot_python_data"],
        "architecture": "Combines computer vision, OCR, and FFmpeg pipelines with local speech synthesis to automatically edit, caption, deduplicate, and publish short-form and long-form video content.",
        "monetization": "$89/mo creator studio SaaS or agency automation package."
    },
    {
        "id": "idea-07",
        "title": "Reverse Cloudflare for LLMs (AI Gateway & Semantic Cache)",
        "domain": "AI Infrastructure",
        "tagline": "Unified Go AI proxy that blocks scraper bots, caches repeated prompts, and routes across 10+ LLMs",
        "primary_slot": "slot_ai_gateway",
        "slots": ["slot_ai_gateway", "slot_redis_kv", "slot_app_security"],
        "architecture": "Intercepts incoming HTTP traffic to block AI crawlers, hashes and caches repetitive LLM prompts in sub-millisecond in-memory KV stores, and load-balances fallback models.",
        "monetization": "$79–$299/mo infrastructure proxy that cuts customer LLM bills by 50%."
    },
    {
        "id": "idea-08",
        "title": "No-Code Domain LLM Fine-Tuning & Evaluation Workbench",
        "domain": "ML & Fine-Tuning",
        "tagline": "Turn company CSVs and support logs into fine-tuned LoRA adapters in 30 minutes with 80% less VRAM",
        "primary_slot": "slot_ml_training",
        "slots": ["slot_ml_training", "slot_python_data", "slot_canvas_dataviz"],
        "architecture": "Ingests raw datasets, cleanses training pairs with Python pipelines, runs accelerated LoRA fine-tuning, and visualizes loss curves and benchmark evals on an interactive dashboard.",
        "monetization": "$149/mo ML ops platform + compute markup."
    },
    {
        "id": "idea-09",
        "title": "Real-Time Competitor Price & Product Change Radar",
        "domain": "Web Data Extraction",
        "tagline": "Headless browser cluster that turns e-commerce & SaaS pricing pages into clean JSON webhooks",
        "primary_slot": "slot_web_scraper",
        "slots": ["slot_web_scraper", "slot_realtime_api", "slot_tailwind_ui"],
        "architecture": "Schedules stealth headless crawlers to extract structured DOM data, detects pricing or stock diffs, and pushes real-time alerts via Server-Sent Events to a Tailwind dashboard.",
        "monetization": "$49–$199/mo e-commerce intelligence subscription."
    },
    {
        "id": "idea-10",
        "title": "Air-Gapped Enterprise Hybrid RAG & Knowledge Appliance",
        "domain": "Enterprise Search & RAG",
        "tagline": "Sub-50ms dense vector + full-text search engine for confidential legal and medical records",
        "primary_slot": "slot_vector_rag",
        "slots": ["slot_vector_rag", "slot_pdf_docs", "slot_llm_local"],
        "architecture": "Extracts text and tables from scanned PDFs via OCR, indexes hybrid dense/sparse vectors into an embedded or distributed vector DB, and answers complex queries with citations.",
        "monetization": "$5,000/yr on-premise enterprise license for regulated industries."
    },
    {
        "id": "idea-11",
        "title": "Encrypted Digital Contract Room & Graph Knowledge Vault",
        "domain": "Document Automation & PKM",
        "tagline": "Local-first Markdown knowledge graph integrated with bulk PDF cryptographic signing",
        "primary_slot": "slot_pdf_docs",
        "slots": ["slot_pdf_docs", "slot_auth_identity", "slot_vue_svelte"],
        "architecture": "Combines a bidirectional Markdown outliner with automated PDF generation and cryptographic digital signatures so teams can draft, link, and execute legal agreements privately.",
        "monetization": "$19/user/mo DocuSign + Notion alternative."
    },
    {
        "id": "idea-12",
        "title": "White-Label Vertical ERP, Invoicing & Property Management OS",
        "domain": "Vertical B2B SaaS",
        "tagline": "Turn-key Laravel & Filament business suite for contractors, landlords, and wholesalers",
        "primary_slot": "slot_laravel_erp",
        "slots": ["slot_laravel_erp", "slot_laravel_core", "slot_tailwind_ui"],
        "architecture": "Built on a strict Laravel & Filament foundation with modular invoicing, inventory tracking, time-sheets, and PDF financial reporting ready to re-skin for any niche industry.",
        "monetization": "$49/mo vertical SaaS or $299 self-hosted agency license."
    },
    {
        "id": "idea-13",
        "title": "Rapid Multi-Tenant Laravel SaaS Launchpad",
        "domain": "Full-Stack Boilerplates",
        "tagline": "Production-ready Laravel skeleton with OAuth social login, transactional email builder, and RBAC",
        "primary_slot": "slot_laravel_core",
        "slots": ["slot_laravel_core", "slot_auth_identity", "slot_postgres_sql"],
        "architecture": "Unifies Laravel Sanctum/Socialite authentication, visual HTML email templates, database-per-tenant isolation, and automated health checks into a 48-hour MVP launcher.",
        "monetization": "$149 one-time developer boilerplate or agency starter kit."
    },
    {
        "id": "idea-14",
        "title": "Passkey-First Identity Broker & Multi-Tenant SSO Cloud",
        "domain": "Identity & Access Management",
        "tagline": "Drop-in WebAuthn passkeys, OIDC federation, and granular tenant permissions for modern apps",
        "primary_slot": "slot_auth_identity",
        "slots": ["slot_auth_identity", "slot_redis_kv", "slot_react_nextjs"],
        "architecture": "Replaces legacy passwords with biometric passkeys and OIDC tokens, backed by sub-millisecond Redis session revocation and drop-in React/Next.js auth widgets.",
        "monetization": "Free up to 5,000 MAUs, then $0.02/MAU + $99/mo enterprise SSO."
    },
    {
        "id": "idea-15",
        "title": "Usage-Based AI Token Metering, Billing & Feature Flag Engine",
        "domain": "FinTech & Monetization",
        "tagline": "Real-time API/token consumption metering wired directly to Stripe invoices and feature gates",
        "primary_slot": "slot_billing_metering",
        "slots": ["slot_billing_metering", "slot_realtime_api", "slot_postgres_sql"],
        "architecture": "Ingests high-throughput usage events via Go APIs, aggregates billable metrics in real time, triggers automated invoices, and toggles customer feature flags when quotas are reached.",
        "monetization": "0.5% of billed volume or $199/mo self-hosted enterprise tier."
    },
    {
        "id": "idea-16",
        "title": "Generative UI Component Studio & Tailwind Theme Builder",
        "domain": "Frontend & Design Systems",
        "tagline": "Copy-paste Tailwind v4 components with live AI restyling and interactive layout previews",
        "primary_slot": "slot_tailwind_ui",
        "slots": ["slot_tailwind_ui", "slot_react_nextjs", "slot_ai_coding"],
        "architecture": "Pairs a curated library of accessible Tailwind CSS blocks with an LLM layout generator that exports clean React, Vue, or Blade code on the fly.",
        "monetization": "$79 lifetime all-access pass for indie hackers and frontend teams."
    },
    {
        "id": "idea-17",
        "title": "Edge-Rendered Next.js E-Commerce & Content Engine",
        "domain": "Modern Web & Jamstack",
        "tagline": "Ultra-fast React/Next.js storefront with instant search, server actions, and headless CMS",
        "primary_slot": "slot_react_nextjs",
        "slots": ["slot_react_nextjs", "slot_tailwind_ui", "slot_sqlite_edge"],
        "architecture": "Combines React Server Components and modern bundlers with edge-replicated SQLite databases to deliver sub-50ms page loads globally.",
        "monetization": "$29/mo hosted storefront or commercial template license."
    },
    {
        "id": "idea-18",
        "title": "Reactive Real-Time Collaborative Whiteboards & Micro-Apps",
        "domain": "Reactive Frontend",
        "tagline": "Lightweight Vue/Svelte/HTMX reactive web apps with live multiplayer state synchronization",
        "primary_slot": "slot_vue_svelte",
        "slots": ["slot_vue_svelte", "slot_realtime_api", "slot_redis_kv"],
        "architecture": "Uses fine-grained reactive UI frameworks paired with Server-Sent Events and WebSockets to sync cursors, forms, and dashboards across hundreds of clients with minimal bundle size.",
        "monetization": "$12/seat/mo team collaboration SaaS."
    },
    {
        "id": "idea-19",
        "title": "Visual Node-Graph Workflow Builder & 3D Data Explorer",
        "domain": "Visual Programming & 3D",
        "tagline": "Browser-based infinite canvas and WebGL engine for building visual pipelines and 3D twins",
        "primary_slot": "slot_canvas_dataviz",
        "slots": ["slot_canvas_dataviz", "slot_js_ts_core", "slot_workflow_queue"],
        "architecture": "Renders interactive 2D node graphs and 3D WebGL scenes in the browser while compiling user node connections directly into executable backend job pipelines.",
        "monetization": "$49/mo visual automation and digital twin platform."
    },
    {
        "id": "idea-20",
        "title": "Cross-Platform Offline-First Field Service Mobile Suite",
        "domain": "Mobile & Desktop Apps",
        "tagline": "Native iOS, Android, and desktop app with local SQLite sync and on-device barcode/OCR scanning",
        "primary_slot": "slot_mobile_cross",
        "slots": ["slot_mobile_cross", "slot_sqlite_edge", "slot_computer_vision"],
        "architecture": "Built with cross-platform mobile/desktop toolchains, storing all forms and media in an embedded SQLite engine that automatically syncs diffs when connectivity returns.",
        "monetization": "$35/field-technician/mo B2B fleet subscription."
    },
    {
        "id": "idea-21",
        "title": "Distributed Graph + Columnar Cloud Database Platform",
        "domain": "Database Infrastructure",
        "tagline": "Managed PostgreSQL platform uniting Cypher graph queries, columnar analytics, and zero-downtime clones",
        "primary_slot": "slot_postgres_sql",
        "slots": ["slot_postgres_sql", "slot_observability", "slot_terraform_iac"],
        "architecture": "Enhances standard PostgreSQL with graph traversal extensions, columnar compression for OLAP workloads, parallel migration tools, and automated point-in-time backups.",
        "monetization": "Usage-based cloud DBaaS ($99–$1,500/mo per cluster)."
    },
    {
        "id": "idea-22",
        "title": "Zero-Config Browser-to-Edge SQLite Analytics Workbench",
        "domain": "Local-First Data & Edge",
        "tagline": "Inspect, query, and visualize multi-gigabyte SQLite & DuckDB files directly on the edge or desktop",
        "primary_slot": "slot_sqlite_edge",
        "slots": ["slot_sqlite_edge", "slot_canvas_dataviz", "slot_rust_zig"],
        "architecture": "Combines native SQLite/DuckDB database managers with vector search extensions and streaming browser report processors for instant zero-server analytics.",
        "monetization": "$39 one-time pro desktop license + $15/mo team sync."
    },
    {
        "id": "idea-23",
        "title": "Sub-Millisecond Reactive Cache & Live Query Subscription Engine",
        "domain": "High-Speed Caching",
        "tagline": "Multi-threaded Redis/Valkey drop-in replacement that pushes live UI updates whenever keys change",
        "primary_slot": "slot_redis_kv",
        "slots": ["slot_redis_kv", "slot_realtime_api", "slot_go_systems"],
        "architecture": "Leverages modern multi-core KV engines with Raft consensus and reactive query subscriptions so web clients automatically receive real-time state diffs without polling.",
        "monetization": "$99–$499/mo managed real-time state cloud for gaming and fintech."
    },
    {
        "id": "idea-24",
        "title": "High-Throughput gRPC / REST API Gateway & SSE Push Hub",
        "domain": "APIs & Realtime Messaging",
        "tagline": "Type-safe Go API router with automatic OpenAPI docs, gRPC introspection, and live event broadcasting",
        "primary_slot": "slot_realtime_api",
        "slots": ["slot_realtime_api", "slot_go_systems", "slot_auth_identity"],
        "architecture": "Unites idiomatic Go HTTP/gRPC routers with a Server-Sent Events hub to power sub-10ms live notifications, chat widgets, and streaming telemetry.",
        "monetization": "$49/mo realtime messaging & webhook gateway."
    },
    {
        "id": "idea-25",
        "title": "Fault-Tolerant Distributed Job Queue & Webhook Orchestrator",
        "domain": "Workflow Automation",
        "tagline": "Self-hosted background task engine with visual DAG retries, cron scheduling, and dead-letter replay",
        "primary_slot": "slot_workflow_queue",
        "slots": ["slot_workflow_queue", "slot_redis_kv", "slot_observability"],
        "architecture": "Guarantees at-least-once webhook delivery and long-running background task orchestration across microservices with live trace inspection.",
        "monetization": "$79/mo mission-critical background jobs platform."
    },
    {
        "id": "idea-26",
        "title": "Autonomous Kubernetes AIOps Copilot & GitOps Controller",
        "domain": "Cloud Native & Kubernetes",
        "tagline": "AI cluster diagnostics that detects pod crashes and opens automated GitOps pull requests to fix them",
        "primary_slot": "slot_k8s_cloud",
        "slots": ["slot_k8s_cloud", "slot_observability", "slot_ai_gateway"],
        "architecture": "Watches Kubernetes events and eBPF traces, diagnoses root causes of OOMKills or crash loops using an LLM analyzer, and commits Helm/Flux fixes automatically.",
        "monetization": "$149/cluster/mo automated SRE platform."
    },
    {
        "id": "idea-27",
        "title": "Turn-Key Proxmox & Multi-Cloud Terraform PaaS",
        "domain": "Infrastructure as Code",
        "tagline": "Reverse-engineer existing cloud resources into Terraform and deploy self-hosted PaaS stacks in 1 click",
        "primary_slot": "slot_terraform_iac",
        "slots": ["slot_terraform_iac", "slot_docker_sandbox", "slot_selfhosted_apps"],
        "architecture": "Imports unmanaged AWS/GCP/Proxmox infrastructure into clean Terraform state and provisions pre-hardened Docker stacks behind automated Traefik SSL proxies.",
        "monetization": "$59/mo indie cloud control panel (Coolify / Terraform Cloud alternative)."
    },
    {
        "id": "idea-28",
        "title": "Self-Healing Container Patcher & Unikernel Sandbox Cloud",
        "domain": "Containers & Sandboxes",
        "tagline": "Patch container CVEs directly at the binary layer and execute untrusted code inside micro-unikernels",
        "primary_slot": "slot_docker_sandbox",
        "slots": ["slot_docker_sandbox", "slot_app_security", "slot_rust_zig"],
        "architecture": "Scans container images for OS vulnerabilities, injects binary patches without full Dockerfile rebuilds, and runs untrusted workloads inside hardware-isolated unikernels.",
        "monetization": "$249/mo DevSecOps automated patching & AI code sandbox API."
    },
    {
        "id": "idea-29",
        "title": "Zero-Instrumentation eBPF Observability & Privacy Analytics Suite",
        "domain": "Observability & Telemetry",
        "tagline": "Instant kernel-level microservice tracing and GDPR-compliant web analytics without SDK bloat",
        "primary_slot": "slot_observability",
        "slots": ["slot_observability", "slot_k8s_cloud", "slot_postgres_sql"],
        "architecture": "Captures HTTP/gRPC/SQL traffic directly from the Linux kernel via eBPF probes while running trace-based integration tests and lightweight visitor analytics.",
        "monetization": "$99/mo observability appliance with zero per-GB ingestion surprise bills."
    },
    {
        "id": "idea-30",
        "title": "Continuous API Pentesting, Bot Firewall & SOC2 Audit Appliance",
        "domain": "Cybersecurity & Compliance",
        "tagline": "Automated API vulnerability scanner paired with crowdsourced IP blocking and tamper-proof DB audit logs",
        "primary_slot": "slot_app_security",
        "slots": ["slot_app_security", "slot_realtime_api", "slot_postgres_sql"],
        "architecture": "Continuously fuzzes REST/GraphQL endpoints for broken auth, blocks malicious botnets at the edge, and records immutable PostgreSQL audit trails for compliance.",
        "monetization": "$199/mo automated security & compliance readiness suite."
    },
    {
        "id": "idea-31",
        "title": "Collaborative Browser Terminal Workbench & TUI Command Center",
        "domain": "Terminal & CLI Power Tools",
        "tagline": "Share terminal sessions over WebSockets with integrated AI command completion and GitHub Actions TUIs",
        "primary_slot": "slot_terminal_tui",
        "slots": ["slot_terminal_tui", "slot_git_devtools", "slot_docker_sandbox"],
        "architecture": "Streams interactive TUI dashboards and shell sessions to any web browser with resilient roaming connections, smart multi-device clipboards, and inline AI help.",
        "monetization": "$15/seat/mo cloud bastion & pair-debugging workspace."
    },
    {
        "id": "idea-32",
        "title": "Apple Silicon / Linux Hardware Telemetry & Embedded AI Lab",
        "domain": "Systems, OS & Embedded",
        "tagline": "Customizable macOS/Linux status bars, ARM64 assembly tools, and microcontroller AI runtimes",
        "primary_slot": "slot_macos_linux",
        "slots": ["slot_macos_linux", "slot_rust_zig", "slot_terminal_tui"],
        "architecture": "Bridges low-level kernel/hardware telemetry with customizable desktop HUDs and deploys ultra-compact AI inference onto ESP32/ARM64 edge devices.",
        "monetization": "$29 pro power-user system utility bundle."
    },
    {
        "id": "idea-33",
        "title": "Local GitHub Actions Runner, Code Quality & Polyglot Compiler Suite",
        "domain": "Developer Productivity",
        "tagline": "Test CI/CD pipelines locally, enforce cross-language linting, and benchmark build performance",
        "primary_slot": "slot_git_devtools",
        "slots": ["slot_git_devtools", "slot_terminal_tui", "slot_ai_coding"],
        "architecture": "Wraps Git workflow automation, static analysis linters, and CI pipeline emulators into a unified developer CLI that catches broken builds before git push.",
        "monetization": "$12/dev/mo velocity toolkit for engineering orgs."
    },
    {
        "id": "idea-34",
        "title": "One-Click Self-Hosted Business & Household Cloud Appliance",
        "domain": "Self-Hosted Products",
        "tagline": "Pre-packaged suite of open-source ERP, customer live chat, CMS, and media servers on a single domain",
        "primary_slot": "slot_selfhosted_apps",
        "slots": ["slot_selfhosted_apps", "slot_terraform_iac", "slot_sqlite_edge"],
        "architecture": "Bundles self-hosted groceries/inventory ERP, live customer chat widgets, and content management systems with automated backups and single sign-on.",
        "monetization": "$19/mo managed private cloud hosting for families and indie businesses."
    },
    {
        "id": "idea-35",
        "title": "Zero-Overhead PHP Flamegraph Profiler & High-Speed Runtime",
        "domain": "PHP Performance & Tooling",
        "tagline": "Production-safe PHP profiling extension with interactive flamegraphs and containerized Nginx stacks",
        "primary_slot": "slot_php_modern",
        "slots": ["slot_php_modern", "slot_laravel_core", "slot_docker_sandbox"],
        "architecture": "Attaches a low-overhead C profiler to PHP-FPM/Octane workers to capture per-request CPU and memory flamegraphs in production without slowing down users.",
        "monetization": "$39/mo Blackfire.io alternative for Laravel and Symfony teams."
    },
    {
        "id": "idea-36",
        "title": "Ultra-Low-Latency Go Microservice Chassis & Network Proxy",
        "domain": "Go Systems Engineering",
        "tagline": "Battle-tested Go concurrency primitives, zero-allocation routers, and secure file/tunnel servers",
        "primary_slot": "slot_go_systems",
        "slots": ["slot_go_systems", "slot_realtime_api", "slot_observability"],
        "architecture": "Compiles into a single static Go binary providing high-concurrency request routing, built-in WebDAV/HTTP file sharing, and Prometheus/eBPF metrics.",
        "monetization": "Open-core enterprise support & managed edge binary distribution."
    },
    {
        "id": "idea-37",
        "title": "Blazing-Fast Rust & Zig WebAssembly Compute Engine",
        "domain": "Rust, Zig & Systems",
        "tagline": "Memory-safe systems components and Zig HTTP backends capable of millions of requests per second",
        "primary_slot": "slot_rust_zig",
        "slots": ["slot_rust_zig", "slot_docker_sandbox", "slot_redis_kv"],
        "architecture": "Harnesses zero-cost abstractions in Rust, Zig, and C++ to build ultra-fast HTTP gateways, custom storage engines, and WebAssembly plugin hosts.",
        "monetization": "High-frequency serverless edge compute platform."
    },
    {
        "id": "idea-38",
        "title": "Automated Python Data Engineering & Financial Quant Pipeline",
        "domain": "Python & Data Science",
        "tagline": "End-to-end Python ingestion, algorithmic analysis, and browser-streamed reporting",
        "primary_slot": "slot_python_data",
        "slots": ["slot_python_data", "slot_ml_training", "slot_postgres_sql"],
        "architecture": "Automates data cleaning, statistical modeling, and ML inference in Python while exporting interactive notebooks and streaming large reports.",
        "monetization": "$99/mo automated data analyst & quant research SaaS."
    },
    {
        "id": "idea-39",
        "title": "Universal TypeScript SDK Generator & Edge Runtime Toolkit",
        "domain": "TypeScript & Node.js Ecosystem",
        "tagline": "Isomorphic TypeScript libraries running seamlessly across Node.js, Bun, Deno, and browser workers",
        "primary_slot": "slot_js_ts_core",
        "slots": ["slot_js_ts_core", "slot_react_nextjs", "slot_realtime_api"],
        "architecture": "Provides end-to-end type safety, schema validation, and zero-dependency utilities for full-stack TypeScript applications.",
        "monetization": "Pro SDK generator & cloud preview environments ($29/mo)."
    },
    {
        "id": "idea-40",
        "title": "Interactive Engineering Playbook, System Design & Onboarding Portal",
        "domain": "Architecture & Developer Education",
        "tagline": "Turn curated awesome lists, system design roadmaps, and coding guides into an interactive team academy",
        "primary_slot": "slot_curated_playbooks",
        "slots": ["slot_curated_playbooks", "slot_pdf_docs", "slot_terminal_tui"],
        "architecture": "Transforms static Markdown roadmaps and reference architectures into interactive skill trees with hands-on browser terminal labs and AI quizzes.",
        "monetization": "$25/seat/mo engineering onboarding & internal developer portal."
    }
]

def assign_repos_to_slots(repos):
    slot_buckets = defaultdict(list)
    repo_to_slot = {}

    for r in repos:
        text = f"{r['full_name']} {r.get('description', '')} {' '.join(r.get('topics', []))}".lower()
        topics_lower = set(t.lower() for t in r.get("topics", []))
        matched_slot = None
        best_score = 0

        for slot_id, slot_name, icon, kws in SPECIFIC_SLOTS:
            score = 0
            for kw in kws:
                if kw in topics_lower:
                    score += 4
                elif re.search(r'\b' + re.escape(kw) + r'\b', text):
                    score += 2
            if score > best_score:
                best_score = score
                matched_slot = slot_id

        if not matched_slot:
            lang = r.get("language", "").lower()
            for slot_id, slot_name, icon, kws in FALLBACK_SLOTS:
                if lang in kws or any(kw in topics_lower for kw in kws) or any(re.search(r'\b' + re.escape(kw) + r'\b', text) for kw in kws):
                    matched_slot = slot_id
                    break

        if not matched_slot:
            matched_slot = "slot_curated_playbooks"

        slot_buckets[matched_slot].append({
            "full_name": r["full_name"],
            "url": r["url"],
            "description": r.get("description", ""),
            "language": r.get("language", "General"),
            "role": r.get("role", ""),
            "category_id": r.get("category_id", ""),
            "_score": best_score,
        })
        repo_to_slot[r["full_name"]] = matched_slot

    for slot_id, bucket in slot_buckets.items():
        bucket.sort(key=lambda x: (-x["_score"], 0 if (x.get("description") or "").strip() else 1, x["full_name"].lower()))
        for item in bucket:
            item.pop("_score", None)

    return slot_buckets, repo_to_slot

def build_ideas_payload(repos):
    slot_buckets, repo_to_slot = assign_repos_to_slots(repos)

    slots_meta = {}
    for slot_id, slot_name, icon, kws in ALL_SLOTS:
        bucket = slot_buckets[slot_id]
        slots_meta[slot_id] = {
            "id": slot_id,
            "name": slot_name,
            "icon": icon,
            "count": len(bucket),
            "repos": bucket
        }

    enriched_ideas = []
    for idea in PRODUCT_IDEAS:
        p_slot = slots_meta[idea["primary_slot"]]
        slot_details = []
        for s_id in idea["slots"]:
            s_info = slots_meta[s_id]
            default_repo = s_info["repos"][0] if s_info["repos"] else None
            slot_details.append({
                "slot_id": s_id,
                "slot_name": s_info["name"],
                "slot_icon": s_info["icon"],
                "total_alternatives": s_info["count"],
                "default_repo": default_repo
            })
        enriched_ideas.append({
            **idea,
            "primary_slot_name": p_slot["name"],
            "primary_slot_icon": p_slot["icon"],
            "primary_repo_count": p_slot["count"],
            "slot_details": slot_details
        })

    return {
        "total_repos_covered": len(repo_to_slot),
        "total_slots": len(ALL_SLOTS),
        "total_ideas": len(enriched_ideas),
        "slots": slots_meta,
        "ideas": enriched_ideas
    }

def generate_ideas_markdown(payload):
    lines = [
        "# 💡 Complete Product Ideas & Swap Matrix (100% Repository Coverage)",
        "",
        f"> **Every single one of the {payload['total_repos_covered']} starred repositories** is mapped into **{payload['total_ideas']} Product Ideas** and **{payload['total_slots']} Interchangeable Functional Slots**.",
        "> You can swap any repository with a similar alternative in the same slot, or combine multiple ideas into an entirely new super-product!",
        "",
        "**Interactive Idea Swapper & Combiner:** [Open Live in index.html](https://bikramtuladhar.github.io/awesome-list/) ✨",
        "",
        "---",
        "",
        "## 🧭 Quick Overview: 40 Product Ideas & Covered Repositories",
        "",
        "| # | Product Idea | Domain | Primary Swappable Slot | Alternatives in Your Stars |",
        "| :--- | :--- | :--- | :--- | :---: |"
    ]

    for idx, idea in enumerate(payload["ideas"], 1):
        lines.append(
            f"| {idx} | **[{idea['title']}](#{idea['id']})** | `{idea['domain']}` | {idea['primary_slot_icon']} {idea['primary_slot_name']} | **{idea['primary_repo_count']} repos** |"
        )

    lines.extend(["", "---", ""])

    for idx, idea in enumerate(payload["ideas"], 1):
        p_slot = payload["slots"][idea["primary_slot"]]
        lines.extend([
            f"## <a id=\"{idea['id']}\"></a>{idx}. {idea['primary_slot_icon']} {idea['title']}",
            "",
            f"> **{idea['tagline']}**",
            "",
            f"- **Domain:** `{idea['domain']}`",
            f"- **Architecture Blueprint:** {idea['architecture']}",
            f"- **Monetization Model:** {idea['monetization']}",
            "",
            "### 🔄 Modular Stack (Swap any component with your starred alternatives):",
            ""
        ])

        for s_det in idea["slot_details"]:
            s_id = s_det["slot_id"]
            s_meta = payload["slots"][s_id]
            top_examples = ", ".join([f"[`{r['full_name']}`]({r['url']})" for r in s_meta["repos"][:5]])
            more_count = max(0, s_meta["count"] - 5)
            more_txt = f" *(+{more_count} more swappable options below)*" if more_count > 0 else ""
            lines.append(f"- **{s_meta['icon']} {s_meta['name']} ({s_meta['count']} options):** {top_examples}{more_txt}")

        lines.extend([
            "",
            f"<details>",
            f"<summary><b>📦 View all {p_slot['count']} Swappable Repositories for {p_slot['icon']} {p_slot['name']}</b></summary>",
            "",
            "| Repository | Language | Description |",
            "| :--- | :--- | :--- |"
        ])

        for r in p_slot["repos"]:
            desc = (r.get("description") or "Open-source building block").replace("|", "\\|").strip()
            lines.append(f"| **[{r['full_name']}]({r['url']})** | `{r.get('language', 'General')}` | {desc} |")

        lines.extend([
            "",
            "</details>",
            "",
            "---",
            ""
        ])

    return "\n".join(lines)

def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    repos = data.get("repos", [])

    payload = build_ideas_payload(repos)

    with open(IDEAS_JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"✅ Saved {IDEAS_JSON_FILE} covering {payload['total_repos_covered']} repositories across {payload['total_ideas']} ideas!")

    md_content = generate_ideas_markdown(payload)
    with open(IDEAS_MD_FILE, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"✅ Generated {IDEAS_MD_FILE} ({len(md_content)} bytes)")

if __name__ == "__main__":
    main()
