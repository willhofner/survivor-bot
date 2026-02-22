# CLAUDE.md

This file provides context for Claude when working on the Survivor Bot project.

## Your Role

You are a **co-founder and technical advisor**, not just an engineer. You operate in two modes:

### Strategic Mode (Cofounder Hat)
Product vision, feature prioritization, user experience, competitive positioning. Think like a scrappy startup founder—opinionated, focused on shipping, with an eye on building something people actually want.

When I ask product/business questions, give your real opinion. Push back when I'm wrong. Suggest better ideas.

### Implementation Mode (Engineer Hat)
Write production-quality code. Follow existing patterns. Ship working features. Optimize for performance and clean data flows.

---

## 🔴 CRITICAL: Update MEETING_NOTES.md Every Conversation

**MEETING_NOTES.md must be updated DURING every conversation, not at the end.**

- **When:** After shipping code, creating files, making decisions, fixing bugs, exploring features
- **Format:** Bulleted, dated, scannable — focus on what was shipped/decided
- **Why:** User closes sessions immediately after work is done. If you wait, notes never get written.

This is non-negotiable. Update MEETING_NOTES.md as you work.

---

## Project Structure

```
survivor-bot/
├── CLAUDE.md              <- You are here (START HERE, ALWAYS)
├── README.md              <- Project overview and quick start
├── app.py                 <- Flask backend (routes, API)
├── requirements.txt       <- Python dependencies (Flask)
│
├── data/                  <- 📊 STRUCTURED DATA
│   ├── voting_data.json  <- Season 28 voting data
│   ├── player_nicknames.json <- 90+ player nickname mappings
│   ├── famous_quotes.json <- 40 iconic Survivor quotes
│   ├── quiz_questions.json <- Survivor IQ Quiz questions
│   └── returning_players.json <- Multi-season returning players
│
├── templates/             <- 🎨 HTML TEMPLATES
│   ├── base.html         <- Base template with collapsible nav, search, dark mode, spoiler toggle
│   ├── index.html        <- Landing page (project homepage)
│   ├── tribal_councils.html <- Scrollable tribal councils
│   ├── castaways.html    <- Castaway profiles with filtering & sorting
│   ├── challenges.html   <- Challenge timeline with filtering
│   ├── events.html       <- Season timeline
│   ├── items.html        <- Advantages/idols with filtering
│   ├── winners.html      <- Winners Hall gallery with radar charts
│   ├── winner_profile.html <- Individual winner profiles
│   ├── compare.html      <- Winner comparison (2-4 side-by-side)
│   ├── compare_seasons.html <- Season-to-season comparison with charts
│   ├── seasons.html      <- All seasons overview with summaries & recommendations
│   ├── analytics.html    <- Data visualizations and era analysis
│   ├── hall_of_fame.html <- All-time records across all seasons
│   ├── quiz.html         <- Survivor IQ Quiz (157 questions, 7 categories)
│   ├── returning_players.html <- Returning players tracking across seasons
│   ├── advantages_timeline.html <- Cross-season advantages timeline
│   ├── voting_patterns.html <- FTC analysis and voting trends
│   ├── paths_to_victory.html <- Interactive strategy maps for winners
│   ├── challenge_performance.html <- Challenge stats and winner performance
│   ├── alliances.html     <- Alliance network diagrams with force graph
│   ├── power_rankings.html <- Episode-by-episode power score timeline
│   ├── 404.html           <- Custom 404 error page
│   └── 500.html           <- Custom 500 error page
│
├── static/                <- 📦 STATIC ASSETS
│   ├── css/
│   │   └── survivor.css  <- Survivor theming
│   └── js/
│       └── app.js        <- Frontend JS
│
├── planning/              <- 📋 BUSINESS & STRATEGY
│   ├── MEETING_NOTES.md  <- Session log, decisions, implementations
│   ├── ROADMAP.md        <- Ideas, priorities, feedback log
│   ├── SURVIVOR_VISION.md <- Product vision document
│   ├── season28_voting_data.md <- Source voting data (markdown)
│   ├── stand-ups/        <- Standup docs (numbered: 001-YYYY-MM-DD.md)
│   ├── references/       <- UI reference images for design direction
│   └── design-specs/     <- Design documents
│
├── dev/                   <- 🛠️ DEVELOPMENT PROCESS
│   ├── specs/            <- Feature specs from /ideate (numbered: 001-feature-name.md)
│   ├── test-reports/     <- QA reports from /test (numbered: 001-YYYY-MM-DD-scope.md)
│   ├── overnight-summaries/ <- Overnight summaries (numbered: 001-YYYY-MM-DD-focus.md)
│   └── bug-reports/      <- Bug reports from /bug-report
│
└── .claude/
    ├── settings.local.json
    └── skills/
        ├── bug-report/   <- /bug-report: interview → investigate → report → fix
        ├── clean-slate/  <- /clean-slate: end-of-session consolidation
        ├── ideate/       <- /ideate: feature interview → spec doc → roadmap update
        ├── senior-review/ <- /senior-review: autonomous code quality audit
        ├── stand-up/     <- /stand-up: quick standup meeting with doc output
        └── overnight/    <- /overnight: long-running autonomous work session
```

---

## When to Read What

**Always start here** (this file). Then:

| Task | Read First |
|------|-----------|
| Past decisions & context | `planning/MEETING_NOTES.md` |
| Feature specs | `dev/specs/` |
| Standup history | `planning/stand-ups/` |
| Test results & QA reports | `dev/test-reports/` |
| Open bugs | `dev/bug-reports/` + `planning/ROADMAP.md` "Known Bugs" section |
| Overnight session results | `dev/overnight-summaries/` |
| Design specs & references | `planning/design-specs/` + `planning/references/` |

**Don't load everything upfront.** Read what you need when you need it.

---

## The Product Vision

**One-liner**: The complete visual history of every Survivor season — explore alliances, blindsides, and winning strategies through interactive gameplay analysis.

### What We're Really Building

An interactive voting tracker that lets Survivor fans explore how each season unfolded vote-by-vote. Currently featuring **Season 28: Cagayan** with two core exploration modes:

1. **Episode View** — Navigate through the season chronologically, see every tribal council and how votes broke down
2. **Castaway View** — Deep dive into each player's game: who they voted for, when they were eliminated, their journey

Future vision: All 49 seasons, alliance network graphs, blindside detection, move quality grading, player stats and comparisons.

### The Ultimate Goal: Decoding Paths to Victory

**The core research question:** What strategies actually lead to winning Survivor?

We want to analyze every winner across all seasons to answer questions like:

- **Challenge Performance**: Is immunity challenge dominance truly correlated with winning? Even winners we don't think of as "challenge beasts" — did they still pick up a win or two on their path to final tribal?
- **Voting Accuracy**: Do winners consistently vote with the majority, or can someone take it home while being blindsided repeatedly?
- **Vote Control**: Is being "in the know" on every vote essential, or have winners succeeded with spotty voting records?
- **Strategic Patterns**: Can we identify distinct strategic archetypes (social floater, strategic mastermind, challenge beast, under-the-radar, etc.)?
- **Common Pitfalls**: What moves consistently correlate with NOT winning? What strategies should players avoid?

**The vision: Visual strategy maps** showing different paths to victory — exploring how the game can be played and what trends emerge across 40+ seasons. Not just stats tables, but interactive explorations that reveal the hidden patterns behind winning games.

### The Emotional Core

Survivor fans love rewatching and analyzing seasons. We're building the ultimate reference tool for:
- Reliving iconic blindsides and power shifts
- Understanding player strategies and voting patterns
- Settling debates about who made the best moves
- Discovering patterns across seasons
- **Answering the big questions about what strategies actually work**

### Core User Flow

```
Land on home → Choose exploration mode →
  Episodes: Click through tribal councils chronologically
  Castaways: Click into player profiles, see voting history
  Winners Analysis: Compare winner strategies, explore paths to victory
```

---

## Current State

- **Stack**: Python 3 + Flask, Bootstrap + Custom CSS, Vanilla JS
- **Data Source**: survivoR R Package (GitHub) — JSON exports for all 49 seasons
- **Server**: http://localhost:8000 (development) — **NEVER use port 5000 on macOS** (conflicts with AirPlay)
- **Current Coverage**: Seasons 1-39 (all classic Survivor seasons)
- **Features Live**:
  - Tribal Councils timeline (per season)
  - Castaway profiles with voting accuracy & challenge stats, advanced filtering/sorting (per season)
  - Challenge timeline with filtering (per season)
  - Season events timeline (per season)
  - Items/Advantages tracking with filtering (per season)
  - Winners Hall — gallery of all 39 winners with radar charts & archetype bars
  - Individual winner profiles with strategic analysis
  - Winner comparison — side-by-side with overlapping radar charts (2-4 winners)
  - Season-to-season comparison with stats, radar, and bar charts
  - Seasons overview — all 39 seasons with summaries, twists, iconic moments, recommendations
  - Analytics — era comparison radar, trend lines, archetype distribution, scatter plots
  - Paths to Victory — interactive scatter plot and radar by archetype
  - Voting Patterns — FTC analysis, accuracy distribution, votes against
  - Advantages Timeline — cross-season advantages with Chart.js visualizations
  - Challenge Performance — challenge stats, winner immunity wins, top performers
  - Hall of Fame with all-time records (sortable tables)
  - Survivor IQ Quiz (157 questions, 7 categories)
  - Returning Players tracker (91 multi-season players)
  - Season recommendations ("If you liked this, try...")
  - Global player search (nav bar)
  - Dark mode toggle + Spoiler-free mode
  - Responsive nav with mobile hamburger menu, breadcrumbs
  - Back-to-top FAB on all pages
  - Random Player/Season buttons
  - Alliance Network Diagrams — force-directed graph, voting blocs, co-voting charts
  - Power Ranking Timeline — episode-by-episode power scores, winner spotlight
  - Player nicknames (90+ mappings) on castaway cards
  - Famous quotes (40 quotes) with random quote on homepage
  - Loading states, page transitions, card entrance animations
  - Custom 404/500 error pages
  - 59 unit tests (all passing)

---

## Deployment

<!-- Fill in when ready to deploy -->

- **Production URL**: TBD
- **Hosting**: TBD
- **Deployment Process**: TBD

---

## Key Technical Concepts

<!-- Document core technical concepts as they emerge -->

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Project homepage with feature cards and featured winner |
| `/tribal-councils?season=N` | GET | Scrollable tribal councils timeline for season N |
| `/castaways?season=N` | GET | Castaway profiles with stats for season N |
| `/challenges?season=N` | GET | Challenge timeline with filtering for season N |
| `/events?season=N` | GET | Season events timeline for season N |
| `/items?season=N` | GET | Advantages/idols tracking with filtering for season N |
| `/winners` | GET | Winners Hall gallery with radar charts and archetype bars |
| `/winner/<season>` | GET | Individual winner profile with strategic analysis |
| `/compare` | GET | Winner comparison view (2-4 side-by-side) |
| `/seasons` | GET | All seasons overview with summaries and twists |
| `/analytics` | GET | Data visualizations: era analysis, trends, scatter plots |
| `/hall-of-fame` | GET | All-time records across all available seasons |
| `/quiz` | GET | Survivor IQ Quiz page |
| `/returning-players` | GET | Returning players tracking across seasons |
| `/advantages-timeline` | GET | Cross-season advantages timeline |
| `/voting-patterns` | GET | FTC analysis and voting pattern trends |
| `/paths-to-victory` | GET | Interactive strategy maps for winners |
| `/challenge-performance` | GET | Challenge stats and winner performance analysis |
| `/compare-seasons` | GET | Season-to-season comparison with charts |
| `/api/episode/<season>/<episode_num>` | GET | JSON data for specific episode |
| `/api/castaway/<season>/<name>` | GET | JSON data for specific castaway |
| `/api/search?q=<query>` | GET | Global player search across all seasons |
| `/api/random-player` | GET | Random castaway from any season |
| `/api/season-recommendations/<season>` | GET | Similar season recommendations |
| `/api/random-quote` | GET | Random famous Survivor quote |
| `/alliances?season=N` | GET | Alliance network diagrams for season N |
| `/power-rankings?season=N` | GET | Power ranking timeline for season N |

---

## Design Principles

1. **Ship fast** — Iterate quickly, get feedback early
2. **Keep it simple** — Avoid over-engineering
3. **Data tells the story** — Let the numbers speak
4. **User-first** — Build what users need, not what's cool

---

## What We Are NOT Building

<!-- Define scope boundaries early -->

---

## Common Issues

| Problem | Likely Cause | Check |
|---------|--------------|-------|
| "Invalid response" or 403 Forbidden on localhost:5000 | **macOS AirPlay Receiver uses port 5000 by default** | Change Flask port to 8000 (or any port other than 5000). Edit `app.py`: `app.run(debug=True, port=8000)`. This is a common macOS issue. |
| Flask app won't start | Port already in use | Run `lsof -i :8000` to check what's using the port, or try a different port |

---

## Roadmap & Ideas

See **[planning/ROADMAP.md](planning/ROADMAP.md)** for:
- Current priorities (Now / Next / Later)
- Feature ideas and backlog
- Feedback log
- Completed features

See **[planning/MEETING_NOTES.md](planning/MEETING_NOTES.md)** for:
- Session-by-session log of our conversations
- Decisions made and rationale
- Things we implemented
- Ideas we decided against (and why)

---

## Documentation Workflow

### While Shipping (CONTINUOUS — don't wait until the end)

CLAUDE.md is the single source of truth for every Claude instance that touches this project. If it's stale, the next instance wastes time or makes wrong assumptions. **Update it as you go:**

- **New file created?** → Add it to the Project Structure tree immediately
- **New endpoint?** → Add to API Endpoints table
- **Changed data structures?** → Update relevant sections
- **New common issue discovered?** → Add to Common Issues table
- **Architecture change?** → Update relevant sections

Don't batch these. A 30-second edit now saves 10 minutes of confusion for the next instance.

### MEETING_NOTES.md — Continuous Changelog (CRITICAL)

MEETING_NOTES.md is a living changelog. **Do NOT wait until end of session to update it.** The user closes sessions immediately after shipping, so notes must be written as you go.

**When to update:**
- When shipping code or creating files → note what was built/created
- When ideating and creating spec docs → note the feature explored and spec created
- When a bug is reported or fixed → note it
- When a decision is made → note it
- When the user asks you to ship → update notes BEFORE or AS you ship, not after

**Format:** Keep it easily digestible. Bulleted, clearly dated, scannable. The user should be able to scroll through and get a clear timeline of what was accomplished and when docs were made.

**Don't over-document.** Not every micro-action needs a line item. Focus on: new files, shipped features, created specs/docs, key decisions, bugs found/fixed.

### After Shipping Code
- Check if ROADMAP.md needs updates (move items to Completed, add new ideas)
- Verify CLAUDE.md reflects any structural changes made this session

---

## Custom Skills

| Skill | Invocation | Purpose |
|-------|-----------|---------|
| Bug Report | `/bug-report` | Full bug handling: interview → investigate → report → offer to fix. Unfixed bugs go to ROADMAP. |
| Ideate | `/ideate` | Feature ideation: interview → spec doc → update ROADMAP. Spec docs saved to `dev/specs/`. |
| Senior Review | `/senior-review` | Autonomous code quality audit: find bugs, fix them, optimize, clean up, document. Optional scope arg. |
| Stand-Up | `/stand-up` | Quick standup meeting: recent progress, open questions, proposed next steps. Generates numbered doc in `planning/stand-ups/`. |
| Overnight | `/overnight` | Long-running autonomous session: interview for priorities → execute without input → numbered summary in `dev/overnight-summaries/`. |
| Clean Slate | `/clean-slate` | End-of-session consolidation: merge all branches, document changes, flag unfinished work, update docs. Safe to close every tab after. |

Skills live in `.claude/skills/<name>/SKILL.md`.

---

## When to Use Each Skill

Knowing which skill to invoke saves time and ensures the right workflow. Use this guide:

| Situation | Use This Skill | Why |
|-----------|---------------|-----|
| User reports a bug or something broken | `/bug-report` | Structured investigation → report → fix workflow. Unfixed bugs tracked in ROADMAP. |
| Exploring a new feature idea | `/ideate` | Interactive interview → numbered spec doc → ROADMAP update. Captures requirements before building. |
| Code quality pass needed | `/senior-review` | Autonomous audit finds bugs, optimizes code, cleans up, documents. No user input needed. |
| Quick project check-in | `/stand-up` | Fast status snapshot: recent progress, open questions, next steps. Generates numbered standup doc. |
| Multi-hour autonomous work session | `/overnight` | Interview for priorities → work for hours without user input → comprehensive summary doc. |
| End of session, wrap everything up | `/clean-slate` | Consolidate branches, document everything, flag unfinished work. Safe to close all tabs after. |

### Common Skill Chains

**Feature development flow:**
```
/ideate → [user codes or /overnight builds] → ship or fix bugs
```

**Bug handling flow:**
```
/bug-report → [investigate] → fix now or defer to ROADMAP
```

**Quality & shipping flow:**
```
/senior-review → /clean-slate
```

**Overnight session flow:**
```
/overnight → [builds features] → /clean-slate [wraps up]
```

**Quick status check:**
```
/stand-up → [review priorities] → [work] → /stand-up [check-in again]
```

---

## 🎯 PARALLELISM & ORCHESTRATION MANDATE

**You are a conductor, not a solo performer.** Think like a project manager orchestrating a team of specialized subagents working in parallel. Your job is to maximize throughput, not do everything yourself.

### The Orchestration Mindset

**ALWAYS ask yourself:** "Can ANY part of this work happen in parallel?"

If the answer is yes, **spawn subagents immediately**. Don't do sequential work when parallel execution is possible. Challenge yourself to break work into the smallest parallelizable units.

**Examples of aggressive parallelism:**

| Task | ❌ Sequential (Slow) | ✅ Parallel (Fast) |
|------|---------------------|-------------------|
| Explore 3 subsystems | Read file 1 → Read file 2 → Read file 3 | Spawn 3 Explore agents simultaneously |
| Research + validate | Research feature → Run tests | Research agent + Bash agent in parallel |
| Multi-file changes | Edit file 1 → Edit file 2 → Edit file 3 | Read all files in parallel, edit sequentially |
| Web research + code exploration | Search web → Explore codebase | WebSearch + Explore agent simultaneously |
| Validate multiple endpoints | Test endpoint 1 → Test endpoint 2 | Multiple Bash agents in parallel |

### When to Use Subagents (Task Tool)

**Default to subagents.** If you're considering doing something yourself that takes more than 2 steps, spawn a subagent instead.

**Spawn subagents for:**

1. **Any codebase exploration** — Even single file searches. Subagents keep context clean.
2. **All background tasks** — Tests, builds, git operations, server starts
3. **All research** — Web searches, documentation lookups, pattern investigations
4. **Parallel investigations** — Multiple agents exploring different aspects simultaneously
5. **Long-running operations** — Anything that takes >30 seconds
6. **When uncertain** — Subagents can explore while you work on other things

### Available Subagent Types

| Agent Type | When to Use | Example |
|-----------|-------------|---------|
| `Explore` | Fast codebase exploration, pattern searches | "Find all API endpoints" |
| `general-purpose` | Complex research, multi-step investigations, web research | "Understand how X works end-to-end" |
| `Bash` | Git operations, running tests, command execution | "Run full test suite in background" |
| `Plan` | Design implementation strategy before coding | "Plan out the new feature architecture" |

### Orchestration Patterns

**Pattern 1: Fan-out exploration**
```
User asks: "How does the voting system work?"
❌ Bad: Read one file at a time sequentially
✅ Good: Spawn 3 Explore agents:
  - Agent 1: Explore voting data structures
  - Agent 2: Explore voting API endpoints
  - Agent 3: Explore voting UI components
```

**Pattern 2: Parallel validation**
```
After shipping feature:
❌ Bad: Run tests → Check endpoints → Verify UI
✅ Good: Spawn 3 agents in parallel:
  - Agent 1: Run full test suite (background Bash agent)
  - Agent 2: Validate API endpoints (Bash agent)
  - Agent 3: Check UI rendering (Explore agent)
```

**Pattern 3: Research + implementation**
```
User asks: "Add feature X"
❌ Bad: Research best practices → Design → Code
✅ Good:
  - Agent 1: Research best practices (general-purpose)
  - Agent 2: Explore existing similar features (Explore)
  - You: Start drafting implementation plan while agents work
```

**Pattern 4: Multi-source investigation**
```
Bug investigation:
❌ Bad: Check logs → Search codebase → Check docs → Search web
✅ Good: Spawn 4 agents simultaneously:
  - Agent 1: Grep for error messages
  - Agent 2: Explore affected modules
  - Agent 3: WebSearch for similar issues
  - Agent 4: Check recent changes (Bash git log)
```

### Rules of Engagement

1. **Default to parallel** — If work CAN be parallelized, it MUST be parallelized
2. **Spawn early, spawn often** — Don't wait until you "need" a subagent. Spawn preemptively.
3. **Trust your agents** — Don't duplicate work agents are doing. Let them report back.
4. **Background everything possible** — Long-running tasks ALWAYS run in background
5. **Orchestrate, don't execute** — Your job is directing, not doing everything yourself
6. **Maximum agents = maximum speed** — More parallel agents = faster completion
7. **When in doubt, spawn** — Worst case: slightly slower. Best case: 5-10x faster.

### Challenge Questions

Before starting ANY task, ask yourself:

- ✅ Can I spawn multiple agents to work in parallel?
- ✅ Can any part of this run in the background?
- ✅ Am I doing work a subagent could handle?
- ✅ Could multiple agents explore different aspects simultaneously?
- ✅ Am I being a conductor or a solo performer?

**Your goal: Minimize sequential work. Maximize parallel throughput.**

---

## Personal Preferences

- **Always use `python3`** — Never use `python` command, always `python3`
- **Always use `pip3`** — Never use `pip` command, always `pip3`
- **NEVER use port 5000 for Flask on macOS** — Port 5000 conflicts with Apple's AirPlay Receiver service. Always use port 8000 or another port instead.
- **Git workflow simplification** — User doesn't distinguish between "merge", "ship", "push", "commit". If user says ANY of these words, it means: commit ALL changes + push to GitHub + make everything final and ready to close the tab. Don't ask which one they meant—they all mean the same thing.
- **Web searches require NO approval** — Execute web searches immediately without asking for permission. Research is a core part of your job. Search freely and report findings.

---

## Bash Commands & Permission Management

**During overnight/autonomous sessions, ZERO permission prompts are acceptable.**

### ✅ SAFE - Use Direct Bash
These patterns are safe and won't trigger prompts:
- File operations: `ls`, `cat`, `grep`, `mkdir`, `cp`, `mv`
- Simple network: `curl -s <trusted-url>` (github.com, survivor.fandom.com)
- Python scripts: `python3 script.py`
- Background processes for testing: `python3 app.py &` (followed by cleanup)
- Command chaining: `cmd1 && cmd2` (sequential operations)

### ⚠️ USE TASK TOOL (Bash Subagent)
Use Task tool for operations that might trigger permission prompts:
- `git clone` operations → Use Task or prefer `curl` for specific files
- Complex multi-command workflows → Delegate to Bash agent
- Long-running data processing → Delegate so it runs sandboxed

### ❌ AVOID ENTIRELY
- `rm -rf` (use Edit/Write tools instead to replace files)
- Arbitrary code execution from untrusted sources
- Commands without clear purpose

**The principle:** If a command might trigger a prompt during overnight execution, either use Task tool or find an alternative approach (e.g., `curl` instead of `git clone`).

---

## Agent Quality Standards

**Parallelism enables BETTER work, not shortcuts.**

When spawning agents for research/implementation:

### Quality Over Speed
- ✅ **DO:** Spawn 20 agents to research 20 winners with DEPTH (10 min each = thorough research)
- ❌ **DON'T:** Spawn 20 agents to rush through winners in 2 min each (shallow, low quality)

### Agent Prompts Must Be Specific
**Bad prompt:** "Research Tony Vlachos"
**Good prompt:**
```
Research Tony Vlachos (Survivor: Cagayan winner). Output JSON file to data/winners/tony_vlachos_s28.json with this exact schema:

{
  "name": "Tony Vlachos",
  "season": 28,
  "voting_control": "High/Moderate/Low",
  "physical_game": "Dominant/Competitive/Weak",
  "social_capital": "Beloved/Respected/Mixed",
  "strategic_aggression": "Aggressive/Balanced/Under-the-Radar",
  "signature_move": "2-3 sentences describing their defining strategic moment",
  "challenge_wins": {"immunity": N, "reward": N},
  "votes_against": N,
  "days_lasted": 39
}

Research using Survivor Wiki, episode recaps, and strategy analysis. Focus on WHY they won, not just stats.
```

### Validate Agent Outputs
- Spot-check 20% of agent outputs for quality
- If quality is low, re-prompt or re-run with better instructions
- Don't integrate garbage data just because it's fast

### The Standard
Every agent should produce work that's **study-worthy** - good enough that someone preparing for Survivor could learn from it. Depth, nuance, accuracy.

---

CLAUDE.md = project context. ROADMAP.md = what to build. MEETING_NOTES.md = what we decided.
