#!/usr/bin/env python3
"""
Builds the enhanced index.html with 3 interactive tabs:
1. 📦 All Building Blocks (1,729+ tools)
2. 💡 Ideas List & Repo Swapper (40 Ideas covering 100% of 1,729 repos — swap any project with similar ones!)
3. 🧬 Super-Project Combiner (Combine 2+ ideas or custom slots into an entirely new product architecture!)
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "repos.json")
IDEAS_FILE = os.path.join(BASE_DIR, "data", "ideas.json")
INDEX_FILE = os.path.join(BASE_DIR, "index.html")

from update_and_classify import CATEGORIES, FEATURED_REMIX_RECIPES

def generate_html(repos_payload, ideas_payload):
    total_count = repos_payload["total_count"]
    repos_json = json.dumps(repos_payload)
    ideas_json = json.dumps(ideas_payload)
    categories_json = json.dumps(CATEGORIES)
    recipes_json = json.dumps(FEATURED_REMIX_RECIPES)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Awesome Product Remix, Idea Swapper & Super-Project Combiner</title>
  <meta name="description" content="1,729+ curated developer tools mapped to 40 swappable product ideas and a multi-project combiner.">
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
      background: rgba(255, 255, 255, 0.9);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(226, 232, 240, 0.85);
    }}
    .dark .glass-card {{
      background: rgba(15, 23, 42, 0.8);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(51, 65, 85, 0.65);
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
  <header class="border-b border-slate-200 dark:border-slate-800 bg-white/85 dark:bg-slate-900/85 backdrop-blur sticky top-0 z-40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
      <div class="flex items-center space-x-3">
        <span class="text-2xl p-2 bg-emerald-100 dark:bg-emerald-950/60 rounded-xl">⚡</span>
        <div>
          <h1 class="font-bold text-base sm:text-lg leading-tight tracking-tight flex items-center gap-2">
            Awesome Product Remix Studio
            <span class="hidden sm:inline-block bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 text-xs px-2.5 py-0.5 rounded-full font-semibold border border-emerald-500/20">100% Repo Coverage ({total_count} Tools)</span>
          </h1>
          <p class="text-xs text-slate-500 dark:text-slate-400">Swap Similar Projects • Combine Ideas into New Products</p>
        </div>
      </div>

      <!-- Primary Mode Navigation Tabs -->
      <div class="flex items-center bg-slate-100 dark:bg-slate-800/90 p-1 rounded-xl border border-slate-200 dark:border-slate-700">
        <button id="navTabIdeas" onclick="switchMainView('IDEAS')" class="main-nav-btn px-3 sm:px-4 py-1.5 rounded-lg text-xs sm:text-sm font-bold transition bg-emerald-600 text-white shadow-sm flex items-center gap-1.5">
          <span>💡 Ideas & Repo Swapper</span>
          <span class="bg-white/20 px-1.5 py-0.2 rounded text-[11px]">40 Ideas / {total_count} Repos</span>
        </button>
        <button id="navTabCombiner" onclick="switchMainView('COMBINER')" class="main-nav-btn px-3 sm:px-4 py-1.5 rounded-lg text-xs sm:text-sm font-bold transition text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white flex items-center gap-1.5">
          <span>🧬 Combine Projects</span>
          <span id="combinerBadge" class="bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 px-1.5 py-0.2 rounded text-[11px] font-mono">2</span>
        </button>
        <button id="navTabCatalog" onclick="switchMainView('CATALOG')" class="main-nav-btn px-3 sm:px-4 py-1.5 rounded-lg text-xs sm:text-sm font-bold transition text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white flex items-center gap-1.5">
          <span>📦 All Tools</span>
        </button>
      </div>

      <div class="flex items-center space-x-2">
        <button id="themeToggle" class="p-2 rounded-lg text-slate-500 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-slate-800 transition" title="Toggle Dark Mode">
          <i data-lucide="moon" class="w-5 h-5 dark:hidden"></i>
          <i data-lucide="sun" class="w-5 h-5 hidden dark:block"></i>
        </button>
        <a href="https://github.com/bikramtuladhar/awesome-list" target="_blank" rel="noopener noreferrer" class="hidden md:flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold bg-slate-900 hover:bg-slate-800 text-white dark:bg-white dark:text-slate-900 rounded-lg transition">
          <i data-lucide="github" class="w-4 h-4"></i>
          <span>GitHub</span>
        </a>
      </div>
    </div>
  </header>

  <!-- ========================================================================= -->
  <!-- VIEW 1: IDEAS LIST & SIMILAR REPO SWAPPER (Covers all 1,729 repositories) -->
  <!-- ========================================================================= -->
  <section id="viewIdeas" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <!-- Banner -->
    <div class="rounded-2xl p-6 bg-gradient-to-r from-emerald-700 via-teal-700 to-slate-900 text-white shadow-lg mb-6">
      <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div class="max-w-3xl">
          <div class="inline-flex items-center gap-2 bg-white/15 px-3 py-1 rounded-full text-xs font-semibold mb-2">
            <span>🔄 100% Starred Repository Coverage • Swap Any Component</span>
          </div>
          <h2 class="text-2xl sm:text-3xl font-extrabold tracking-tight">
            40 Product Ideas Covering Every Single Repository ({total_count} Tools)
          </h2>
          <p class="text-emerald-100 text-sm mt-1 leading-relaxed">
            Each product idea below is built from modular <strong>Functional Slots</strong>. Use the dropdowns inside any idea card to <strong>swap a repository with similar starred projects</strong>, randomize stacks, or click <strong>"+ Combine Idea"</strong> to fuse multiple ideas into a brand-new product!
          </p>
        </div>
        <div class="flex flex-wrap gap-2 shrink-0">
          <button onclick="randomizeAllIdeaSwaps()" class="px-4 py-2.5 bg-white text-slate-900 hover:bg-emerald-50 rounded-xl font-bold text-xs shadow-md transition flex items-center gap-2">
            <i data-lucide="shuffle" class="w-4 h-4 text-emerald-600"></i>
            <span>Shuffle All Repo Swaps</span>
          </button>
          <button onclick="switchMainView('COMBINER')" class="px-4 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 rounded-xl font-bold text-xs shadow-md transition flex items-center gap-2">
            <i data-lucide="sparkles" class="w-4 h-4"></i>
            <span>Open Project Combiner →</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Search & Domain Filter for Ideas -->
    <div class="flex flex-col md:flex-row gap-3 items-center justify-between mb-6">
      <div class="relative w-full md:w-96">
        <i data-lucide="search" class="w-4 h-4 absolute left-3.5 top-3 text-slate-400"></i>
        <input
          type="text"
          id="ideaSearchInput"
          placeholder="Search 40 ideas or any of the 1,729 repos to see which idea uses it..."
          class="w-full pl-10 pr-4 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-500 text-sm"
        />
      </div>

      <div class="flex items-center gap-3 w-full md:w-auto justify-between">
        <select id="slotFilterSelect" class="px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-xs font-semibold focus:outline-none focus:ring-2 focus:ring-emerald-500">
          <option value="ALL">All 40 Functional Slots ({total_count} Repos)</option>
        </select>
        <div class="text-xs font-mono bg-slate-100 dark:bg-slate-800 px-3 py-2 rounded-xl whitespace-nowrap">
          Ideas: <span id="visibleIdeasCount" class="font-bold text-emerald-600 dark:text-emerald-400">40</span> / 40
        </div>
      </div>
    </div>

    <!-- Ideas Grid -->
    <div id="ideasGrid" class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Dynamically rendered by JS -->
    </div>
  </section>

  <!-- ========================================================================= -->
  <!-- VIEW 2: SUPER-PROJECT COMBINER (Combine multiple ideas or custom repos)   -->
  <!-- ========================================================================= -->
  <section id="viewCombiner" class="hidden max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="rounded-2xl p-6 bg-gradient-to-br from-indigo-900 via-slate-900 to-emerald-950 text-white shadow-xl mb-6 border border-indigo-500/30">
      <div class="max-w-3xl">
        <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-indigo-500/20 text-indigo-200 border border-indigo-400/30 mb-2">
          🧬 Multi-Idea & Multi-Repo Synthesis Lab
        </span>
        <h2 class="text-2xl sm:text-3xl font-extrabold tracking-tight">
          Combine Projects to Create an Entirely New Super-Product
        </h2>
        <p class="text-indigo-100 text-sm mt-1 leading-relaxed">
          Select 2 or more Product Ideas (or mix & match any of the 40 functional slots) to synthesize a brand-new product architecture, complete with swappable repositories, unified data flow, and monetization strategy.
        </p>
      </div>

      <!-- Preset Super-Combinations -->
      <div class="mt-5 pt-4 border-t border-white/10 flex flex-wrap items-center gap-2">
        <span class="text-xs font-semibold text-indigo-200 mr-1">⚡ Quick Super-Merges:</span>
        <button onclick="loadSuperPreset(['idea-01', 'idea-09', 'idea-12'])" class="px-3 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-xs font-medium transition">
          📞 Autonomous Voice Sales + Scraper + ERP
        </button>
        <button onclick="loadSuperPreset(['idea-02', 'idea-10', 'idea-11'])" class="px-3 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-xs font-medium transition">
          🔒 Air-Gapped Local AI + Hybrid RAG + Contract Vault
        </button>
        <button onclick="loadSuperPreset(['idea-07', 'idea-14', 'idea-15'])" class="px-3 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-xs font-medium transition">
          💳 Turn-Key AI Cloud (Gateway + Passkey Auth + Token Billing)
        </button>
        <button onclick="loadSuperPreset(['idea-26', 'idea-28', 'idea-29'])" class="px-3 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-xs font-medium transition">
          ☸️ Self-Healing Autonomous Cloud (K8s AIOps + Unikernels + eBPF)
        </button>
        <button onclick="randomizeSuperCombination()" class="px-3 py-1.5 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs transition ml-auto">
          🎲 Surprise Super-Combination
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
      <!-- Left Column: Select Ideas to Combine -->
      <div class="lg:col-span-5 glass-card rounded-2xl p-5">
        <div class="flex items-center justify-between mb-3">
          <h3 class="font-bold text-base flex items-center gap-2">
            <span>1️⃣ Select Ideas to Fuse</span>
            <span class="text-xs font-normal text-slate-500">(Pick 2 to 5)</span>
          </h3>
          <button onclick="clearCombinedIdeas()" class="text-xs text-slate-400 hover:text-rose-500 transition">Clear All</button>
        </div>
        <div id="combinerIdeaSelector" class="space-y-2 max-h-[540px] overflow-y-auto custom-scroll pr-1">
          <!-- Checkboxes for all 40 ideas -->
        </div>
      </div>

      <!-- Right Column: Generated New Super-Product Blueprint -->
      <div class="lg:col-span-7 glass-card rounded-2xl p-6 flex flex-col justify-between border-2 border-emerald-500/40">
        <div id="superProductOutput">
          <!-- Populated dynamically -->
        </div>
      </div>
    </div>
  </section>

  <!-- ========================================================================= -->
  <!-- VIEW 3: ALL BUILDING BLOCKS CATALOG (Original 1,729 tool explorer)        -->
  <!-- ========================================================================= -->
  <section id="viewCatalog" class="hidden max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="flex flex-col md:flex-row gap-4 items-center justify-between mb-6">
      <div class="relative w-full md:w-96">
        <i data-lucide="search" class="w-4 h-4 absolute left-3.5 top-3.5 text-slate-400"></i>
        <input 
          type="text" 
          id="searchInput" 
          placeholder="Search all {total_count} tools by name, role, topic..."
          class="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-500 text-sm shadow-sm"
        />
      </div>

      <div class="flex items-center gap-3 w-full md:w-auto justify-between md:justify-end">
        <select id="langSelect" class="px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 shadow-sm">
          <option value="ALL">All Languages</option>
        </select>
        
        <div class="text-xs font-mono text-slate-500 dark:text-slate-400 whitespace-nowrap bg-slate-100 dark:bg-slate-800/80 px-3 py-2 rounded-xl">
          Showing <span id="visibleCount" class="font-bold text-slate-900 dark:text-white">0</span> of <span class="font-bold">{total_count}</span>
        </div>
      </div>
    </div>

    <div class="flex items-center gap-2 overflow-x-auto custom-scroll pb-3 mb-6" id="categoryTabs">
      <button data-cat="ALL" class="cat-tab active px-3.5 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition bg-emerald-600 text-white shadow-sm">
        All Building Blocks
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" id="toolGrid"></div>

    <div id="noResults" class="hidden text-center py-16">
      <h3 class="font-bold text-slate-700 dark:text-slate-300">No matching tools found</h3>
      <p class="text-sm text-slate-500">Try adjusting your search query or switching categories.</p>
    </div>
  </section>

  <!-- Repo / Slot Explorer Modal (View all swappable repos in a slot) -->
  <div id="slotModal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
    <div class="bg-white dark:bg-slate-900 rounded-2xl max-w-3xl w-full p-6 shadow-2xl border border-slate-200 dark:border-slate-800 max-h-[88vh] flex flex-col">
      <div class="flex items-start justify-between pb-4 border-b border-slate-200 dark:border-slate-800">
        <div>
          <span class="text-xs font-bold uppercase tracking-wider text-emerald-600 dark:text-emerald-400">Interchangeable Component Slot</span>
          <h2 id="slotModalTitle" class="text-xl font-bold text-slate-900 dark:text-white mt-0.5"></h2>
          <p id="slotModalSubtitle" class="text-xs text-slate-500 mt-0.5"></p>
        </div>
        <button onclick="closeSlotModal()" class="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 dark:hover:text-slate-200">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>
      <div class="my-3">
        <input type="text" id="slotModalSearch" placeholder="Filter interchangeable repositories in this slot..." class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs focus:outline-none focus:ring-2 focus:ring-emerald-500" />
      </div>
      <div id="slotModalList" class="overflow-y-auto custom-scroll space-y-2 flex-1 pr-1"></div>
    </div>
  </div>

  <footer class="mt-16 border-t border-slate-200 dark:border-slate-800 py-8 text-center text-xs text-slate-500">
    <p>Curated by <a href="https://github.com/bikramtuladhar" class="underline font-semibold">Bikram Tuladhar</a> • 40 Swappable Product Ideas Covering All {total_count} Starred Repositories.</p>
  </footer>

  <script>
    const DATA = {repos_json};
    const IDEAS_DATA = {ideas_json};
    const CATEGORIES = {categories_json};

    // State
    let activeMainView = 'IDEAS';
    let ideaSearchQuery = '';
    let selectedSlotFilter = 'ALL';
    // Track currently selected repo index per (idea_id, slot_id)
    const activeSlotSelections = {{}};
    // Track selected ideas for the Super-Project Combiner
    let combinedIdeaIds = new Set(['idea-01', 'idea-07']);

    // Initialize default selections for each idea's slots
    IDEAS_DATA.ideas.forEach((idea, idx) => {{
      idea.slots.forEach((slotId, sIdx) => {{
        const slotRepos = IDEAS_DATA.slots[slotId]?.repos || [];
        activeSlotSelections[`${{idea.id}}__${{slotId}}`] = (idx + sIdx) % Math.max(1, slotRepos.length);
      }});
    }});

    // Theme Setup
    const themeToggle = document.getElementById('themeToggle');
    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {{
      document.documentElement.classList.add('dark');
    }}
    themeToggle.addEventListener('click', () => {{
      document.documentElement.classList.toggle('dark');
      localStorage.theme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
      lucide.createIcons();
    }});

    // Main View Switcher
    window.switchMainView = function(view) {{
      activeMainView = view;
      document.getElementById('viewIdeas').classList.toggle('hidden', view !== 'IDEAS');
      document.getElementById('viewCombiner').classList.toggle('hidden', view !== 'COMBINER');
      document.getElementById('viewCatalog').classList.toggle('hidden', view !== 'CATALOG');

      const navMap = {{
        'IDEAS': document.getElementById('navTabIdeas'),
        'COMBINER': document.getElementById('navTabCombiner'),
        'CATALOG': document.getElementById('navTabCatalog')
      }};
      Object.entries(navMap).forEach(([k, btn]) => {{
        if (k === view) {{
          btn.className = 'main-nav-btn px-3 sm:px-4 py-1.5 rounded-lg text-xs sm:text-sm font-bold transition bg-emerald-600 text-white shadow-sm flex items-center gap-1.5';
        }} else {{
          btn.className = 'main-nav-btn px-3 sm:px-4 py-1.5 rounded-lg text-xs sm:text-sm font-bold transition text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white flex items-center gap-1.5';
        }}
      }});

      if (view === 'IDEAS') renderIdeasGrid();
      if (view === 'COMBINER') renderCombinerView();
      if (view === 'CATALOG') renderTools();
      lucide.createIcons();
    }};

    // Populate Slot Filter Dropdown
    const slotFilterSelect = document.getElementById('slotFilterSelect');
    Object.values(IDEAS_DATA.slots).forEach(slot => {{
      const opt = document.createElement('option');
      opt.value = slot.id;
      opt.textContent = `${{slot.icon}} ${{slot.name}} (${{slot.count}} repos)`;
      slotFilterSelect.appendChild(opt);
    }});

    slotFilterSelect.addEventListener('change', (e) => {{
      selectedSlotFilter = e.target.value;
      renderIdeasGrid();
    }});

    document.getElementById('ideaSearchInput').addEventListener('input', (e) => {{
      ideaSearchQuery = e.target.value.toLowerCase().trim();
      renderIdeasGrid();
    }});

    // Swap a repository inside an Idea's slot
    window.onSlotRepoChange = function(ideaId, slotId, newIndex) {{
      activeSlotSelections[`${{ideaId}}__${{slotId}}`] = parseInt(newIndex, 10);
      renderIdeasGrid();
    }};

    // Cycle to next similar project in the slot
    window.cycleSlotRepo = function(ideaId, slotId) {{
      const slot = IDEAS_DATA.slots[slotId];
      if (!slot || !slot.repos.length) return;
      const key = `${{ideaId}}__${{slotId}}`;
      const cur = activeSlotSelections[key] || 0;
      activeSlotSelections[key] = (cur + 1) % slot.repos.length;
      renderIdeasGrid();
    }};

    // Shuffle all swaps across all 40 ideas
    window.randomizeAllIdeaSwaps = function() {{
      IDEAS_DATA.ideas.forEach(idea => {{
        idea.slots.forEach(slotId => {{
          const slot = IDEAS_DATA.slots[slotId];
          if (slot && slot.repos.length) {{
            activeSlotSelections[`${{idea.id}}__${{slotId}}`] = Math.floor(Math.random() * slot.repos.length);
          }}
        }});
      }});
      renderIdeasGrid();
    }};

    // Render the 40 Ideas Grid with interactive Repo Swappers
    function renderIdeasGrid() {{
      const grid = document.getElementById('ideasGrid');
      grid.innerHTML = '';

      const filteredIdeas = IDEAS_DATA.ideas.filter(idea => {{
        const matchesSlot = selectedSlotFilter === 'ALL' || idea.slots.includes(selectedSlotFilter) || idea.primary_slot === selectedSlotFilter;
        if (!matchesSlot) return false;
        if (!ideaSearchQuery) return true;

        // Check idea title, domain, tagline, or ANY repo inside its primary slot or active slots
        const ideaText = `${{idea.title}} ${{idea.domain}} ${{idea.tagline}} ${{idea.architecture}}`.toLowerCase();
        if (ideaText.includes(ideaSearchQuery)) return true;

        // Also check if any repo in its primary slot matches the search query!
        const pSlot = IDEAS_DATA.slots[idea.primary_slot];
        if (pSlot && pSlot.repos.some(r => r.full_name.toLowerCase().includes(ideaSearchQuery) || (r.description || '').toLowerCase().includes(ideaSearchQuery))) {{
          return true;
        }}
        return false;
      }});

      document.getElementById('visibleIdeasCount').textContent = filteredIdeas.length;

      filteredIdeas.forEach((idea, index) => {{
        const pSlot = IDEAS_DATA.slots[idea.primary_slot];
        const isSelectedForCombine = combinedIdeaIds.has(idea.id);

        // Build the 3 swappable slot rows
        let slotsHtml = '';
        idea.slots.forEach(slotId => {{
          const slot = IDEAS_DATA.slots[slotId];
          if (!slot) return;

          // If user searched for a specific repo name, auto-select the matching repo in this slot
          let selectedIdx = activeSlotSelections[`${{idea.id}}__${{slotId}}`] || 0;
          if (ideaSearchQuery) {{
            const matchIdx = slot.repos.findIndex(r => r.full_name.toLowerCase().includes(ideaSearchQuery));
            if (matchIdx !== -1) selectedIdx = matchIdx;
          }}
          const activeRepo = slot.repos[selectedIdx] || slot.repos[0];

          const optionsHtml = slot.repos.map((r, idx) => {{
            const shortDesc = (r.description || '').slice(0, 48);
            return `<option value="${{idx}}" ${{idx === selectedIdx ? 'selected' : ''}}>${{r.full_name}} (${{r.language}}) — ${{shortDesc}}</option>`;
          }}).join('');

          slotsHtml += `
            <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/70 border border-slate-200/80 dark:border-slate-700/70">
              <div class="flex items-center justify-between gap-2 mb-1.5">
                <span class="text-[11px] font-bold uppercase tracking-wider text-emerald-700 dark:text-emerald-400 flex items-center gap-1">
                  <span>${{slot.icon}}</span>
                  <span>${{slot.name}}</span>
                </span>
                <div class="flex items-center gap-1.5">
                  <button onclick="openSlotModal('${{slot.id}}', '${{idea.id}}')" class="text-[11px] font-semibold text-indigo-600 dark:text-indigo-400 hover:underline">
                    Browse all ${{slot.count}}
                  </button>
                  <button onclick="cycleSlotRepo('${{idea.id}}', '${{slot.id}}')" class="px-2 py-0.5 rounded bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-700 dark:text-emerald-300 text-[11px] font-semibold transition flex items-center gap-1" title="Swap with next similar project">
                    <span>🔄 Swap</span>
                  </button>
                </div>
              </div>

              <select onchange="onSlotRepoChange('${{idea.id}}', '${{slot.id}}', this.value)" class="w-full px-2.5 py-1.5 rounded-lg text-xs font-mono bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 focus:outline-none focus:ring-2 focus:ring-emerald-500">
                ${{optionsHtml}}
              </select>

              <div class="mt-2 flex items-center justify-between text-xs text-slate-600 dark:text-slate-400">
                <p class="truncate pr-2" title="${{(activeRepo?.description || '').replace(/"/g, '&quot;')}}">
                  ${{activeRepo?.description || 'Open-source building block'}}
                </p>
                <a href="${{activeRepo?.url || '#'}}" target="_blank" rel="noopener noreferrer" class="shrink-0 font-semibold text-slate-800 dark:text-slate-200 hover:text-emerald-500">
                  GitHub ↗
                </a>
              </div>
            </div>
          `;
        }});

        const card = document.createElement('div');
        card.className = 'glass-card rounded-2xl p-6 flex flex-col justify-between hover:border-emerald-500/50 transition-all shadow-sm';
        card.innerHTML = `
          <div>
            <div class="flex items-start justify-between gap-3 mb-2">
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border border-emerald-500/20">
                  ${{idea.domain}}
                </span>
                <span class="text-xs font-mono text-slate-500 dark:text-slate-400">
                  Covers ${{pSlot.count}} similar repos
                </span>
              </div>
              <button onclick="toggleCombineIdea('${{idea.id}}')" class="px-3 py-1 rounded-lg text-xs font-bold transition ${{isSelectedForCombine ? 'bg-indigo-600 text-white' : 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-indigo-500/20'}}">
                ${{isSelectedForCombine ? '✓ In Combiner' : '+ Combine Idea'}}
              </button>
            </div>

            <h3 class="text-lg font-extrabold text-slate-900 dark:text-white mt-1">
              ${{idea.primary_slot_icon}} ${{idea.title}}
            </h3>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5 mb-4">
              ${{idea.tagline}}
            </p>

            <!-- Swappable Component Slots -->
            <div class="space-y-2.5 my-3">
              ${{slotsHtml}}
            </div>
          </div>

          <div class="mt-4 pt-3.5 border-t border-slate-200/70 dark:border-slate-800 space-y-2 text-xs">
            <div>
              <span class="font-bold text-slate-700 dark:text-slate-300">Architecture:</span>
              <span class="text-slate-600 dark:text-slate-400"> ${{idea.architecture}}</span>
            </div>
            <div class="flex items-center justify-between pt-1">
              <span class="font-semibold text-emerald-700 dark:text-emerald-400">💰 ${{idea.monetization}}</span>
              <button onclick="openSlotModal('${{idea.primary_slot}}', '${{idea.id}}')" class="text-xs font-bold underline text-slate-700 dark:text-slate-300 hover:text-emerald-500">
                View all ${{pSlot.count}} repos →
              </button>
            </div>
          </div>
        `;
        grid.appendChild(card);
      }});

      lucide.createIcons();
    }}

    // Open Modal showing ALL repositories inside a functional slot (so user can inspect & swap any of the 1,729 repos)
    let currentModalSlotId = null;
    let currentModalIdeaId = null;

    window.openSlotModal = function(slotId, ideaId) {{
      currentModalSlotId = slotId;
      currentModalIdeaId = ideaId;
      const slot = IDEAS_DATA.slots[slotId];
      if (!slot) return;

      document.getElementById('slotModalTitle').textContent = `${{slot.icon}} ${{slot.name}} (${{slot.count}} Swappable Projects)`;
      document.getElementById('slotModalSubtitle').textContent = `Click "Use in Idea" on any repository below to swap it into the product stack.`;
      document.getElementById('slotModalSearch').value = '';
      renderSlotModalItems('');
      document.getElementById('slotModal').classList.remove('hidden');
      lucide.createIcons();
    }};

    window.closeSlotModal = function() {{
      document.getElementById('slotModal').classList.add('hidden');
    }};

    document.getElementById('slotModalSearch').addEventListener('input', (e) => {{
      renderSlotModalItems(e.target.value.toLowerCase().trim());
    }});

    function renderSlotModalItems(query) {{
      const slot = IDEAS_DATA.slots[currentModalSlotId];
      if (!slot) return;
      const list = document.getElementById('slotModalList');
      list.innerHTML = '';

      slot.repos.forEach((repo, idx) => {{
        const text = `${{repo.full_name}} ${{repo.description}} ${{repo.language}}`.toLowerCase();
        if (query && !text.includes(query)) return;

        const row = document.createElement('div');
        row.className = 'p-3 rounded-xl border border-slate-200 dark:border-slate-800 hover:border-emerald-500/50 flex items-center justify-between gap-3 bg-slate-50/50 dark:bg-slate-800/40';
        row.innerHTML = `
          <div class="min-w-0">
            <div class="flex items-center gap-2">
              <a href="${{repo.url}}" target="_blank" rel="noopener noreferrer" class="font-bold text-sm text-slate-900 dark:text-white hover:text-emerald-500 truncate">
                ${{repo.full_name}}
              </a>
              <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300">
                ${{repo.language || 'General'}}
              </span>
            </div>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5 line-clamp-1">
              ${{repo.description || 'Open-source building block'}}
            </p>
          </div>
          <button onclick="selectRepoFromModal(${{idx}})" class="shrink-0 px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition">
            Swap Into Idea
          </button>
        `;
        list.appendChild(row);
      }});
    }}

    window.selectRepoFromModal = function(repoIndex) {{
      if (currentModalIdeaId && currentModalSlotId) {{
        activeSlotSelections[`${{currentModalIdeaId}}__${{currentModalSlotId}}`] = repoIndex;
        closeSlotModal();
        renderIdeasGrid();
      }}
    }};

    // =========================================================================
    // SUPER-PROJECT COMBINER LOGIC (Fuse 2+ Ideas into a brand-new product)
    // =========================================================================
    window.toggleCombineIdea = function(ideaId) {{
      if (combinedIdeaIds.has(ideaId)) {{
        combinedIdeaIds.delete(ideaId);
      }} else {{
        combinedIdeaIds.add(ideaId);
      }}
      document.getElementById('combinerBadge').textContent = combinedIdeaIds.size;
      if (activeMainView === 'IDEAS') renderIdeasGrid();
      if (activeMainView === 'COMBINER') renderCombinerView();
    }};

    window.clearCombinedIdeas = function() {{
      combinedIdeaIds.clear();
      document.getElementById('combinerBadge').textContent = '0';
      renderCombinerView();
    }};

    window.loadSuperPreset = function(ids) {{
      combinedIdeaIds = new Set(ids);
      document.getElementById('combinerBadge').textContent = combinedIdeaIds.size;
      renderCombinerView();
    }};

    window.randomizeSuperCombination = function() {{
      const shuffled = [...IDEAS_DATA.ideas].sort(() => 0.5 - Math.random());
      combinedIdeaIds = new Set(shuffled.slice(0, 3).map(i => i.id));
      document.getElementById('combinerBadge').textContent = combinedIdeaIds.size;
      renderCombinerView();
    }};

    function renderCombinerView() {{
      const selector = document.getElementById('combinerIdeaSelector');
      selector.innerHTML = '';

      IDEAS_DATA.ideas.forEach(idea => {{
        const checked = combinedIdeaIds.has(idea.id);
        const item = document.createElement('div');
        item.onclick = () => toggleCombineIdea(idea.id);
        item.className = `p-3 rounded-xl border cursor-pointer transition flex items-center justify-between gap-2 ${{
          checked
            ? 'bg-indigo-500/10 border-indigo-500 text-slate-900 dark:text-white'
            : 'bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:border-slate-400'
        }}`;
        item.innerHTML = `
          <div class="min-w-0">
            <div class="font-bold text-xs truncate">${{idea.primary_slot_icon}} ${{idea.title}}</div>
            <div class="text-[11px] opacity-75 truncate">${{idea.domain}} • ${{idea.primary_repo_count}} repos</div>
          </div>
          <div class="w-5 h-5 rounded-md flex items-center justify-center text-xs font-bold ${{checked ? 'bg-indigo-600 text-white' : 'border border-slate-300 dark:border-slate-700'}}">
            ${{checked ? '✓' : ''}}
          </div>
        `;
        selector.appendChild(item);
      }});

      const output = document.getElementById('superProductOutput');
      const selectedIdeas = IDEAS_DATA.ideas.filter(i => combinedIdeaIds.has(i.id));

      if (selectedIdeas.length < 2) {{
        output.innerHTML = `
          <div class="text-center py-20">
            <p class="text-lg font-bold text-slate-600 dark:text-slate-300">Select at least 2 Ideas on the left to synthesize a new Super-Product!</p>
            <p class="text-xs text-slate-400 mt-1">Or click one of the Quick Super-Merges above.</p>
          </div>
        `;
        return;
      }}

      // Synthesize a new combined product from the selected ideas
      const domains = selectedIdeas.map(i => i.domain);
      const combinedTitle = `Unified ${{selectedIdeas.map(i => i.title.split('&')[0].replace(/^(On-Premise|Offline|Universal|Autonomous|Automated|Autopilot|Reverse|No-Code|Real-Time|Air-Gapped|Encrypted|White-Label|Rapid|Passkey-First|Usage-Based|Generative|Edge-Rendered|Reactive|Visual|Cross-Platform|Distributed|Zero-Config|Sub-Millisecond|High-Throughput|Fault-Tolerant|Turn-Key|Self-Healing|Zero-Instrumentation|Continuous|Collaborative|Apple|Local|One-Click|Zero-Overhead|Ultra-Low-Latency|Blazing-Fast|Interactive)\\s+/i, '').trim()).slice(0, 3).join(' + ')}} Platform`;

      // Collect unique primary slots from each selected idea + their secondary slots
      const uniqueSlots = [];
      selectedIdeas.forEach(idea => {{
        idea.slots.forEach(sId => {{
          if (!uniqueSlots.includes(sId)) uniqueSlots.push(sId);
        }});
      }});

      let combinedSlotsHtml = '';
      uniqueSlots.slice(0, 6).forEach(slotId => {{
        const slot = IDEAS_DATA.slots[slotId];
        const selIdx = activeSlotSelections[`super__${{slotId}}`] || 0;
        const activeRepo = slot.repos[selIdx] || slot.repos[0];

        const opts = slot.repos.map((r, idx) => `<option value="${{idx}}" ${{idx === selIdx ? 'selected' : ''}}>${{r.full_name}} (${{r.language}})</option>`).join('');

        combinedSlotsHtml += `
          <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700">
            <div class="flex items-center justify-between text-[11px] font-bold text-indigo-600 dark:text-indigo-400 mb-1">
              <span>${{slot.icon}} ${{slot.name}} (${{slot.count}} options)</span>
              <a href="${{activeRepo.url}}" target="_blank" class="underline">GitHub ↗</a>
            </div>
            <select onchange="activeSlotSelections['super__${{slotId}}'] = parseInt(this.value, 10); renderCombinerView();" class="w-full px-2 py-1.5 rounded bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-xs font-mono">
              ${{opts}}
            </select>
            <p class="text-[11px] text-slate-500 mt-1 truncate">${{activeRepo.description || ''}}</p>
          </div>
        `;
      }});

      const synergeticFlow = selectedIdeas.map((idea, idx) => `
        <li class="flex items-start gap-2">
          <span class="font-bold text-emerald-500">Phase ${{idx + 1}} (${{idea.domain}}):</span>
          <span>${{idea.architecture}}</span>
        </li>
      `).join('');

      output.innerHTML = `
        <div>
          <div class="flex flex-wrap items-center gap-2 mb-2">
            <span class="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30">
              ✨ Synthesized Super-Product (${{selectedIdeas.length}} Ideas Fused)
            </span>
            <span class="text-xs font-mono text-slate-400">
              ${{domains.join(' × ')}}
            </span>
          </div>

          <h3 class="text-xl sm:text-2xl font-extrabold text-slate-900 dark:text-white mt-1">
            🚀 ${{combinedTitle}}
          </h3>
          <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Fusing: ${{selectedIdeas.map(i => `<strong>${{i.title}}</strong>`).join(' + ')}}
          </p>

          <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400 mt-5 mb-2">
            🔄 Swappable Super-Stack Architecture (Swap any project below):
          </h4>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            ${{combinedSlotsHtml}}
          </div>

          <div class="mt-5 p-4 rounded-xl bg-indigo-500/5 border border-indigo-500/20">
            <h4 class="text-xs font-bold uppercase tracking-wider text-indigo-600 dark:text-indigo-400 mb-2">
              ⚡ End-to-End Unified System Dataflow
            </h4>
            <ul class="space-y-2 text-xs text-slate-700 dark:text-slate-300 leading-relaxed">
              ${{synergeticFlow}}
            </ul>
          </div>

          <div class="mt-4 p-3.5 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-between">
            <div class="text-xs">
              <span class="font-bold text-emerald-800 dark:text-emerald-300">💰 Combined Revenue Strategy:</span>
              <span class="text-slate-700 dark:text-slate-300"> Enterprise Multi-Module Suite ($299–$999/mo) combining ${{selectedIdeas.map(i => i.domain).join(', ')}}.</span>
            </div>
          </div>
        </div>
      `;
    }}

    // =========================================================================
    // VIEW 3: ALL TOOLS CATALOG LOGIC
    // =========================================================================
    let currentCategory = 'ALL';
    let currentLanguage = 'ALL';
    let searchQuery = '';

    const toolGrid = document.getElementById('toolGrid');
    const searchInput = document.getElementById('searchInput');
    const langSelect = document.getElementById('langSelect');
    const categoryTabs = document.getElementById('categoryTabs');
    const visibleCount = document.getElementById('visibleCount');
    const noResults = document.getElementById('noResults');

    CATEGORIES.forEach(cat => {{
      const count = DATA.repos.filter(r => r.category_id === cat.id).length;
      const btn = document.createElement('button');
      btn.dataset.cat = cat.id;
      btn.className = 'cat-tab px-3.5 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-300 hover:border-emerald-500';
      btn.innerHTML = `${{cat.icon}} ${{cat.name}} <span class="ml-1 opacity-60">(${{count}})</span>`;
      btn.onclick = () => {{
        currentCategory = cat.id;
        renderTools();
      }};
      categoryTabs.appendChild(btn);
    }});

    const languages = Array.from(new Set(DATA.repos.map(r => r.language).filter(l => l && l !== 'General'))).sort();
    languages.forEach(lang => {{
      const opt = document.createElement('option');
      opt.value = lang;
      opt.textContent = lang;
      langSelect.appendChild(opt);
    }});

    function renderTools() {{
      const q = searchQuery.toLowerCase().trim();
      const filtered = DATA.repos.filter(repo => {{
        const matchesCat = (currentCategory === 'ALL' || repo.category_id === currentCategory);
        const matchesLang = (currentLanguage === 'ALL' || repo.language === currentLanguage);
        const textToSearch = `${{repo.full_name}} ${{repo.role}} ${{repo.description}} ${{(repo.topics || []).join(' ')}}`.toLowerCase();
        const matchesQuery = !q || textToSearch.includes(q);
        return matchesCat && matchesLang && matchesQuery;
      }});

      visibleCount.textContent = filtered.length;
      noResults.classList.toggle('hidden', filtered.length > 0);
      toolGrid.innerHTML = '';

      filtered.slice(0, 120).forEach(repo => {{
        const cat = CATEGORIES.find(c => c.id === repo.category_id) || {{ icon: '📦', name: 'DevTools' }};
        const card = document.createElement('div');
        card.className = 'glass-card p-5 rounded-2xl flex flex-col justify-between hover:border-emerald-500/50 transition';
        card.innerHTML = `
          <div>
            <div class="flex items-start justify-between gap-2 mb-2">
              <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border border-emerald-500/20">
                <span>${{cat.icon}}</span>
                <span class="truncate max-w-[160px]">${{repo.role}}</span>
              </span>
              <span class="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400">
                ${{repo.language || 'General'}}
              </span>
            </div>
            <h3 class="font-bold text-base text-slate-900 dark:text-white truncate">${{repo.full_name}}</h3>
            <p class="text-xs text-slate-600 dark:text-slate-400 line-clamp-2 mt-1.5">${{repo.description || 'Open source building block.'}}</p>
          </div>
          <div class="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-end">
            <a href="${{repo.url}}" target="_blank" rel="noopener noreferrer" class="text-xs font-semibold text-emerald-600 dark:text-emerald-400 hover:underline">
              View on GitHub ↗
            </a>
          </div>
        `;
        toolGrid.appendChild(card);
      }});
      lucide.createIcons();
    }}

    searchInput.addEventListener('input', (e) => {{
      searchQuery = e.target.value;
      renderTools();
    }});

    langSelect.addEventListener('change', (e) => {{
      currentLanguage = e.target.value;
      renderTools();
    }});

    // Initial render
    renderIdeasGrid();
    lucide.createIcons();
  </script>
</body>
</html>
"""

def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        repos_payload = json.load(f)
    with open(IDEAS_FILE, "r", encoding="utf-8") as f:
        ideas_payload = json.load(f)

    html = generate_html(repos_payload, ideas_payload)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Updated {INDEX_FILE} with Ideas List Swapper & Super-Project Combiner ({len(html)} bytes)")

if __name__ == "__main__":
    main()
