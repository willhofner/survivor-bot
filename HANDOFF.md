# Survivor Bot - Project Handoff Document

**Last Updated:** 2026-02-15
**Status:** Season Analyzer 2.0 fully operational for Season 28
**App URL:** http://localhost:8000

---

## Executive Summary

Built a comprehensive Survivor Season 28 (Cagayan) analyzer web app with voting data, challenge results, idol tracking, and episode grading. All features shipped in one session using parallel subagent execution.

**Current State:**
- ✅ Season 28 fully functional with 7 major features
- ⚠️ Data pipeline scalable for challenges/votes, NOT scalable for advantages (manual research)
- 🎯 Next priority: Multi-season support OR advantage data pipeline

---

## Architecture Overview

### Tech Stack
- **Backend:** Python 3 + Flask (port 8000 to avoid macOS AirPlay on 5000)
- **Frontend:** Bootstrap 5 + Custom Survivor-themed CSS
- **Data:** JSON files (voting, challenges, advantages, timeline)

### Application Structure

```
survivor-bot/
├── app.py                  # Flask backend (156 lines)
│   ├── Data loading (4 JSON files)
│   ├── Helper functions (voting accuracy, challenge stats, episode grading)
│   ├── Data enrichment (calculates stats on startup)
│   └── 6 routes + 2 API endpoints
│
├── data/                   # ALL DATA FILES
│   ├── voting_data.json           # Voting history (manual entry for S28)
│   ├── season28_challenges.json   # Challenge results (from survivoR package)
│   ├── season28_advantages_idols.json  # Idol/advantage tracking (manual research)
│   └── season28_timeline.json     # Key events (manual research)
│
├── templates/              # Jinja2 HTML templates
│   ├── base.html          # Nav + layout (5 nav links)
│   ├── index.html         # Landing page
│   ├── tribal_councils.html  # Scrollable tribal timeline
│   ├── castaways.html     # Player profiles (enhanced with stats)
│   ├── challenges.html    # Challenge timeline
│   ├── events.html        # Key events timeline
│   └── items.html         # Idol/advantage tracker
│
└── static/
    └── css/survivor.css   # ~1000 lines, Survivor-themed (torch animations, tribal colors)
```

---

## Routes & Features

| Route | Feature | Data Source |
|-------|---------|-------------|
| `/` | Landing page | Static |
| `/tribal-councils` | 16 tribal councils, scrollable, drama scores | voting_data.json + advantages |
| `/castaways` | 18 player profiles, voting accuracy %, challenge stats | voting_data.json + challenges |
| `/challenges` | 23 challenges timeline | season28_challenges.json |
| `/events` | Season timeline (swaps, merge, twists) | season28_timeline.json |
| `/items` | 6 idols/advantages tracker | season28_advantages_idols.json |

---

## Key Algorithms

### 1. Voting Accuracy Calculation
```python
accuracy = (correct_votes / total_votes) * 100
```
- Correct vote = voted for person who was actually eliminated
- Excludes self-votes (when player votes for themselves at elimination)

### 2. Episode Grading (Drama Score)
```python
score = 5.0  # Base
score += 2.0 if merge
score += 1.0 * advantages_played
score += 1.0 if vote_spread <= 2 (close vote)
score += 0.5 * (unique_targets - 2)  # Multiple targets
return min(score, 10.0)
```
Displayed as flame emojis: 🔥🔥🔥🔥🔥 (1-10 scale)

### 3. Challenge Beast Metrics
```python
immunity_wins = count where player in challenge.winners and 'Immunity' in type
reward_wins = count where player in challenge.winners and 'Reward' in type
total = immunity_wins + reward_wins
```

---

## Data Sources & Scalability

### ✅ SCALABLE (All 49 seasons)

**1. Challenge Results**
- **Source:** survivoR R Package (GitHub: `doehm/survivoR`)
- **File:** `dev/json/challenge_results.json`
- **Coverage:** ALL seasons
- **Method:** Filter by season number, extract to JSON
- **Agent used:** Subagent extracted in 3 minutes

**2. Voting Data** (potentially)
- **Source:** survivoR package has vote history data
- **File:** `dev/json/vote_history.json`
- **Status:** Not yet integrated (Season 28 was manual entry)

### ❌ NOT SCALABLE (Manual research required)

**1. Advantages/Idols**
- **Current:** Manual web research (15+ searches per season)
- **Coverage:** Season 28 only (6 idols documented)
- **Bottleneck:** No structured database exists
- **Time:** ~30-60 minutes per season

**2. Key Events/Timeline**
- **Current:** Manual research (Survivor Wiki, episode summaries)
- **Coverage:** Season 28 only
- **Partial:** survivoR has swap/merge data, missing twists/advantages

---

## Season 28 Data Inventory

### Challenges (23 total)
- 12 immunity-only
- 8 reward-only
- 3 combined immunity+reward
- Challenge beasts: Tasha (3 immunity), Spencer (3 immunity), Woo (2)

### Idols/Advantages (6 total)
1. Garrett - Luzon idol (Day 1) - Not played, voted out holding it
2. Tony - Aparri idol (Day 3) - Played on LJ at merge
3. LJ - Solana idol (Day 7) - Played on Tony at merge
4. Spencer - Post-merge idol (Day 20) - Wasted play
5. Tony - Tyler Perry Super Idol (Day 26) - Never played, psychological weapon
6. Tony - Auction idol (Day 29) - Played at Final 5

**Unique fact:** 0 of 4 idol plays negated any votes (unprecedented)

### Key Events
- Tribe formations (Day 1): Aparri, Luzon, Solana
- Tribe swap (Day 12): Luzon disbanded
- Lindsey quit (Day 14)
- Merge (Day 17): Solarrion tribe formed
- Tyler Perry Idol introduced (Day 17)
- Survivor Auction (Day 29)
- Tony's idol bluff (Day 37)

---

## Critical Technical Details

### Port Configuration
**NEVER use port 5000 on macOS** - conflicts with Apple AirPlay Receiver
- App runs on port 8000
- See `CLAUDE.md` for documentation on this

### Data Loading
All JSON files loaded at startup (lines 6-17 in app.py):
```python
voting_data = json.load('data/voting_data.json')
challenge_data = json.load('data/season28_challenges.json')
advantages_data = json.load('data/season28_advantages_idols.json')
timeline_data = json.load('data/season28_timeline.json')
```

### Data Enrichment (Startup)
Lines 97-109 calculate all derived stats:
- Voting accuracy for all 18 castaways
- Challenge beast metrics for all castaways
- Drama scores for all 16 tribal councils
- Flame ratings (emoji conversion)

### Navigation Update Required
If adding new routes, update `templates/base.html` lines 18-24

---

## Known Issues & Limitations

### Current Limitations
1. **Single season only** - Season 28 hardcoded
2. **No season switcher** - UI doesn't support multi-season
3. **Manual advantage data** - Doesn't scale to 49 seasons
4. **No search/filter** - Can't search by player name or event
5. **No alliances** - Deferred feature

### Technical Debt
- No database (all JSON files)
- No caching (recalculates on every request)
- No tests
- No error handling for missing data

---

## Data Pipeline for Multi-Season Support

### What's Ready
1. **survivoR package** already cloned (contains all 49 seasons)
2. **Challenge data extraction** - proven scalable (3-min subagent task)
3. **Vote data extraction** - available in survivoR package
4. **Architecture** - supports multiple JSON files per season

### What's Needed for Season X
```bash
# Automated (5 min):
1. Extract challenge_results for season X from survivoR
2. Extract vote_history for season X from survivoR
3. Build tribal council structure from votes

# Manual (30-60 min):
4. Research advantages/idols for season X
5. Research key events for season X
6. Create season X JSON files
```

### Recommended Approach
**Option A:** Ship 5-10 popular seasons manually (28, 20, 40, 16, 31)
**Option B:** Build Survivor Wiki scraper for advantages
**Option C:** Crowdsource advantage data (build template, community contribution)

---

## Files Modified This Session

### Created
- `dev/specs/001-season-analyzer-2.md` (feature spec)
- `data/season28_challenges.json` (23 challenges)
- `data/season28_advantages_idols.json` (6 idols)
- `data/season28_timeline.json` (season events)
- `templates/tribal_councils.html`
- `templates/challenges.html`
- `templates/events.html`
- `templates/items.html`
- Added ~400 lines to `static/css/survivor.css`

### Modified
- `app.py` - Added 3 helper functions, 4 routes, data enrichment
- `templates/base.html` - Updated nav (5 links)
- `templates/castaways.html` - Added voting accuracy + challenge stats
- `planning/MEETING_NOTES.md` - Session documentation
- `planning/ROADMAP.md` - Updated priorities

---

## Next Steps (Recommended Priority Order)

### Immediate Wins
1. **Update README.md** - Reflect new features (currently shows old Episode View)
2. **Update index.html** - Link to new views, update stats
3. **Add season selector** - Dropdown to switch between seasons (prep for multi-season)

### Short-term (Next Session)
4. **Add Season 40 (Winners at War)** - Popular, high idol count, good test case
5. **Build advantage data template** - Standardize manual entry
6. **Extract votes from survivoR** - Automate voting data for all seasons

### Medium-term
7. **Multi-season architecture** - URL structure (`/season/28/tribal-councils`)
8. **Season comparison view** - Compare stats across seasons
9. **Player search** - Search by name across all seasons

### Long-term
10. **Survivor Wiki scraper** - Automate advantage extraction
11. **Alliance tracking** - Network graphs, voting blocs
12. **Advanced visualizations** - Sankey diagrams for vote flows
13. **Production deployment** - Host publicly

---

## Research Sources Used

### Automated Data
- **survivoR Package:** https://github.com/doehm/survivoR
  - Challenge results: `dev/json/challenge_results.json`
  - Vote history: `dev/json/vote_history.json`
  - Tribe mapping: `dev/json/tribe_mapping.json`

### Manual Research (Season 28)
- Survivor Wiki: https://survivor.fandom.com/wiki/Survivor:_Cagayan
- TrueDorkTimes: https://www.truedorktimes.com/s28/
- Wikipedia: Season overview
- Episode recaps: Individual episode articles
- 12+ additional sources cross-referenced

---

## Agent Execution Summary

This session used **aggressive parallel execution**:

### Subagent Team (3 agents, ran simultaneously)
1. **Agent A (Bash):** Extracted challenge data from survivoR → 23 challenges
2. **Agent B (general-purpose):** Researched idols → 6 idols fully documented
3. **Agent C (general-purpose):** Researched timeline → Complete season events

**Execution time:** ~3-5 minutes (all parallel)

### Main Thread (while agents worked)
- Implemented 3 calculation algorithms
- Created 4 HTML templates
- Added 4 Flask routes
- Updated existing templates
- Added ~400 lines CSS

**Total implementation time:** ~30 minutes

---

## Testing Status

✅ **All routes tested (HTTP 200):**
```
/ ✅
/tribal-councils ✅
/castaways ✅
/challenges ✅
/events ✅
/items ✅
```

**Manual testing needed:**
- Cross-browser compatibility
- Mobile responsiveness
- Large screen layouts
- Data validation (check accuracy calculations)

---

## Key Decisions Made

1. **Skip alliances** - Too complex, manual curation, deferred
2. **Prioritize advantages** - User's highest priority
3. **One comprehensive spec** - Not separate specs per feature
4. **Scrolling UX** - All timelines scrollable, not paginated
5. **Flame rating system** - Visual drama scores (emojis)
6. **Port 8000** - Avoid macOS AirPlay conflict

---

## Critical Context for Next Agent

### User Preferences (from CLAUDE.md)
- Always use `python3` (not `python`)
- Always use `pip3` (not `pip`)
- NEVER use port 5000 (macOS AirPlay conflict)
- User wants to "move fast" and iterate
- User is a co-founder (strategic thinking, not just engineering)

### What User Cares About
- Advantages/idols (highest priority)
- Scalability to all 49 seasons
- Moving fast, shipping features
- NOT interested in alliances right now
- NOT focused on shareability yet

### What Works Well
- Parallel subagent execution (3+ agents simultaneously)
- survivoR package as primary data source
- Manual research for Season 28 advantages was thorough

### What Needs Improvement
- Advantage data pipeline (manual doesn't scale)
- Multi-season architecture (hardcoded for Season 28)
- README/index.html out of date

---

## Quick Start for Next Agent

1. **Read this file first** (you're doing it!)
2. **Read CLAUDE.md** - Project context, user preferences
3. **Read planning/MEETING_NOTES.md** - Full session history
4. **Check planning/ROADMAP.md** - Current priorities
5. **Review dev/specs/001-season-analyzer-2.md** - Feature spec

**To run the app:**
```bash
cd /Users/willhofner/Desktop/survivor-bot
python3 app.py
# Open http://localhost:8000
```

**To add a new season:**
1. Extract challenges from survivoR package (spawn subagent)
2. Extract votes from survivoR package (spawn subagent)
3. Research advantages (spawn subagent with web search)
4. Create `data/seasonXX_*.json` files
5. Update app.py to load season data

---

## Contact & Resources

- **GitHub:** https://github.com/willhofner/survivor-bot
- **survivoR Package:** https://github.com/doehm/survivoR
- **Survivor Wiki:** https://survivor.fandom.com/wiki/Main_Page
- **TrueDorkTimes:** https://www.truedorktimes.com/

---

**End of Handoff Document**

*Next agent: You have everything you need. Ship features, iterate fast, use subagents aggressively. The user is results-driven and wants to see progress. Good luck!* 🔥
