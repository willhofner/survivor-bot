# Survivor Bot

Interactive web app to explore Survivor voting data. Currently featuring **Season 28: Cagayan**.

## Features

- 🔥 **Episode View** — Click through tribal councils chronologically (keyboard navigation with ←/→)
- ⚔️ **Castaway View** — Explore each player's voting history and journey
- 🎨 **Tribe Filtering** — Filter by Brawn, Brains, or Beauty
- 📊 **Vote Breakdowns** — See who voted for whom at every tribal council
- 🏝️ **Survivor-Themed UI** — Torch animations, tribal colors, tropical aesthetic

## Getting Started

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run the app
python3 app.py
```

Then open: **http://localhost:8000**

## Documentation

- **[CLAUDE.md](CLAUDE.md)** — Project context for Claude Code
- **[planning/ROADMAP.md](planning/ROADMAP.md)** — Feature roadmap and priorities
- **[planning/MEETING_NOTES.md](planning/MEETING_NOTES.md)** — Development log

## Skills

This project uses [Claude Code custom skills](.claude/skills/) for workflow automation:

- `/bug-report` — Bug investigation and tracking
- `/ideate` — Feature ideation and spec creation
- `/senior-review` — Code quality audit
- `/stand-up` — Quick status check
- `/overnight` — Autonomous work session
- `/clean-slate` — End-of-session consolidation

See [CLAUDE.md](CLAUDE.md) for details.
