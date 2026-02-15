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
│
├── planning/              <- 📋 BUSINESS & STRATEGY
│   ├── MEETING_NOTES.md  <- Session log, decisions, implementations
│   ├── ROADMAP.md        <- Ideas, priorities, feedback log
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

<!-- TODO: Fill in your product vision, one-liner, core user flow -->

**One-liner**: [What is this product in one sentence?]

### What We're Really Building

[Core product description]

### The Emotional Core

[Why do users care? What problem does this solve?]

### Core User Flow

```
[Step 1] → [Step 2] → [Step 3]
```

---

## Current State

- **Stack**: [Tech stack - e.g., Python/Flask, Node.js, etc.]
- **Data Source**: [Where does data come from?]
- **Server**: [localhost port or deployment info]

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

<!-- Document API endpoints as you build them -->

| Endpoint | Method | Description |
|----------|--------|-------------|
| TBD | GET | TBD |

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

<!-- Document issues as you encounter them -->

| Problem | Likely Cause | Check |
|---------|--------------|-------|
| TBD | TBD | TBD |

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

## Parallelism & Subagent Usage

**Default to aggressive parallelism.** Don't do things sequentially when they can happen simultaneously.

### When to Use Subagents (Task Tool)

**Use subagents liberally.** They keep context clean, enable parallelism, and get results faster. Default to spawning subagents for:

1. **Codebase exploration** — Understanding how multiple systems work
2. **Multi-part investigations** — Finding patterns across the codebase
3. **Background tasks** — Long-running operations that don't need immediate results
4. **Complex research** — When the answer requires deep investigation

### Available Subagent Types

| Agent Type | When to Use | Example |
|-----------|-------------|---------|
| `Explore` | Fast codebase exploration, pattern searches | "Find all API endpoints" |
| `general-purpose` | Complex research, multi-step investigations | "Understand how X works end-to-end" |
| `Bash` | Git operations, running tests, command execution | "Run full test suite in background" |
| `Plan` | Design implementation strategy before coding | "Plan out the new feature architecture" |

### Rules of Thumb

1. **More than 2 files to explore?** → Spawn parallel Explore agents
2. **Complex "how does X work" question?** → Spawn Explore agents for each subsystem
3. **Multiple independent searches needed?** → One Explore agent per search pattern
4. **Long-running validation?** → Background agent
5. **When in doubt?** → Spawn subagents. Worst case: slightly slower. Best case: 3-5x faster.

**Default stance: If the work can be parallelized, parallelize it.**

---

## Personal Preferences

- **Always use `python3`** — Never use `python` command, always `python3`
- **Always use `pip3`** — Never use `pip` command, always `pip3`
- **Git workflow simplification** — User doesn't distinguish between "merge", "ship", "push", "commit". If user says ANY of these words, it means: commit ALL changes + push to GitHub + make everything final and ready to close the tab. Don't ask which one they meant—they all mean the same thing.

---

CLAUDE.md = project context. ROADMAP.md = what to build. MEETING_NOTES.md = what we decided.
