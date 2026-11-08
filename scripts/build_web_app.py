#!/usr/bin/env python3
"""
Builds index.html — the interactive "Awesome Remix" web app.

The UI lives in scripts/web/template.html (vanilla HTML/CSS/JS, no build step).
This script only prepares a compact, de-duplicated data payload and injects it
into the template at the `__APP_DATA__` placeholder.

Views in the generated app:
  1. Product Ideas  – 40 product ideas; every stack layer can be swapped for a
                      similar starred repo.
  2. Combine        – pick 2–5 ideas and get one merged product blueprint.
  3. Browse tools   – search/filter all starred repos and see where each is used.
"""

import os
import json
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "repos.json")
IDEAS_FILE = os.path.join(BASE_DIR, "data", "ideas.json")
INDEX_FILE = os.path.join(BASE_DIR, "index.html")
TEMPLATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web", "template.html")

from update_and_classify import CATEGORIES


def build_payload(repos_payload, ideas_payload):
    """Create a compact payload: every repo is stored exactly once and
    referenced by index from slots and ideas."""
    repos = repos_payload.get("repos", [])
    index_by_name = {}
    compact_repos = []
    for r in repos:
        name = r.get("full_name") or ""
        if not name or name in index_by_name:
            continue
        index_by_name[name] = len(compact_repos)
        compact_repos.append({
            "n": name,
            "d": (r.get("description") or "").strip(),
            "l": r.get("language") or "",
            "c": r.get("category_id") or "",
            "s": "",
        })

    slots = {}
    for slot_id, s in ideas_payload.get("slots", {}).items():
        idxs = []
        for r in s.get("repos", []):
            name = r.get("full_name")
            if name not in index_by_name:
                # repo only known to ideas.json — add it so nothing is lost
                index_by_name[name] = len(compact_repos)
                compact_repos.append({
                    "n": name,
                    "d": (r.get("description") or "").strip(),
                    "l": r.get("language") or "",
                    "c": r.get("category_id") or "",
                    "s": "",
                })
            i = index_by_name[name]
            compact_repos[i]["s"] = slot_id
            idxs.append(i)
        slots[slot_id] = {"name": s.get("name", slot_id), "icon": s.get("icon", ""), "r": idxs}

    # Ideas sharing a slot start on different repos so the catalog feels varied.
    slot_usage = {}
    ideas = []
    for idea in ideas_payload.get("ideas", []):
        defaults = []
        for slot_id in idea.get("slots", []):
            n = len(slots.get(slot_id, {}).get("r", [])) or 1
            k = slot_usage.get(slot_id, 0)
            slot_usage[slot_id] = k + 1
            defaults.append(k % n)
        ideas.append({
            "id": idea["id"],
            "t": idea.get("title", ""),
            "dm": idea.get("domain", ""),
            "tg": idea.get("tagline", ""),
            "sl": idea.get("slots", []),
            "df": defaults,
            "a": idea.get("architecture", ""),
            "m": idea.get("monetization", ""),
        })

    categories = [
        {"id": c["id"], "name": c["name"], "icon": c.get("icon", ""), "desc": c.get("description", "")}
        for c in CATEGORIES
    ]

    generated = repos_payload.get("generated_at") or datetime.now(timezone.utc).isoformat()
    return {
        "generated": generated[:10],
        "repos": compact_repos,
        "slots": slots,
        "ideas": ideas,
        "categories": categories,
    }


def generate_html(repos_payload, ideas_payload):
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template = f.read()
    payload = build_payload(repos_payload, ideas_payload)
    data_json = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    # Make the JSON safe to embed inside a <script> element.
    data_json = data_json.replace("<", "\\u003c")
    html = template.replace("__APP_DATA__", data_json, 1)
    html = html.replace("__REPO_COUNT__", f"{len(payload['repos']):,}")
    html = html.replace("__IDEA_COUNT__", str(len(payload["ideas"])))
    return html


def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        repos_payload = json.load(f)
    with open(IDEAS_FILE, "r", encoding="utf-8") as f:
        ideas_payload = json.load(f)

    html = generate_html(repos_payload, ideas_payload)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Updated {INDEX_FILE} ({len(html.encode('utf-8')):,} bytes)")


if __name__ == "__main__":
    main()
