# Season Analyzer 2.0 — Comprehensive Season Analysis

**Spec:** 001
**Date:** 2026-02-15
**Status:** Draft

## Overview

Transform the voting tracker into a comprehensive season analyzer with 7 new features: scrollable tribal councils, voting accuracy metrics, challenge outcomes, episode grading, challenge beast stats, key events timeline, and item/advantage tracking. Ship everything possible with existing data (survivoR package), manually curate items/advantages for Season 28.

## User Story

As a Survivor fan, I want to explore every dimension of Season 28 (tribal councils, challenges, advantages, key moments) in one place so I can understand how the season unfolded and analyze player strategies.

## Detailed Behavior

### 1. Scrollable Tribal Councils View (Replaces Episode View)

**Current:** Episode view with pagination (click arrows to navigate episodes)
**New:** Single scrollable page showing all 16 tribal councils in chronological order

- Remove episode grouping and pagination
- Display all tribal councils vertically in one continuous timeline
- Each tribal council shows: Day, Tribe, Eliminated player, Vote breakdown
- Visual separators between tribal councils
- Sticky header showing current position (e.g., "Tribal Council 8 of 16")

### 2. Voting Accuracy % (Castaway Profiles)

Add "Voting Accuracy" stat to each castaway's profile showing:
- **Correct Votes:** How many times they voted for the person who actually got eliminated
- **Total Votes Cast:** Total tribal councils they attended
- **Accuracy %:** `(Correct Votes / Total Votes) × 100`

Display as: "Voting Accuracy: 75% (9/12 votes)"

**Edge case:** If player was voted out (so voted for themselves in final vote), exclude that vote from calculation.

### 3. Challenge Outcomes View

New page: `/challenges`

Show all challenges for the season in chronological order:
- **Challenge type:** Immunity or Reward
- **Day:** When it occurred
- **Winner(s):** Individual or tribe
- **Challenge description:** Brief text (from survivoR data if available, else "Immunity Challenge")

Layout: Scrollable timeline similar to tribal councils

**Data source:** survivoR package `challenge_results` dataset

### 4. Episode Grading

Add "Drama Score" to each episode (displayed on tribal councils view):

**Grading algorithm:**
- Base score: 5/10
- +2 points: Merge episode
- +1 point per advantage/idol played
- +1 point if vote spread is close (within 2 votes)
- +0.5 points per unique person receiving votes (beyond 2 people)

Display as flame emoji rating: 🔥🔥🔥🔥🔥 (1-10 scale, half flames for .5 scores)

### 5. Challenge Beast Metrics (Castaway Profiles)

Add to each castaway's profile:
- **Individual Immunity Wins:** Count of individual immunity challenges won
- **Reward Challenge Wins:** Count of reward challenges won
- **Total Challenge Wins:** Sum of both
- **Challenge Beast Score:** If they won immunity when they were likely the target (voted out immediately after losing immunity)

Display as: "Challenge Wins: 4 immunity, 2 reward (6 total) 💪"

**Data source:** Cross-reference challenge winners with elimination data

### 6. Key Events Timeline

New page: `/events`

Scrollable timeline showing:
- **Tribe formations:** Day 1 (Aparri, Luzon, Solana)
- **Tribe swaps:** Day 14 (if applicable)
- **Merge:** Day 19 (Solarrion formed)
- **Advantages found/played:** Each idol/advantage event
- **Special twists:** Any unique season mechanics

Each event shows:
- Day number
- Event type (icon: 🔄 swap, 🤝 merge, 💎 advantage, 🎯 twist)
- Description
- Impact (who was affected)

**Data source:**
- Tribe swaps/merge: survivoR `tribe_mapping` data
- Advantages: Manual entry for Season 28

### 7. Item/Advantage Tracking

New page: `/items`

Show every advantage/idol in the season:
- **Item type:** Hidden Immunity Idol, Extra Vote, Steal-a-Vote, etc.
- **Found by:** Player name
- **Found on:** Day acquired
- **Used on:** Day played (if played)
- **Result:** Successful (saved someone) / Unsuccessful (wasted) / Not played
- **Voted out with it:** If player was eliminated holding the advantage

Display as cards with timeline:
```
💎 Hidden Immunity Idol
Found: Tony (Day 11)
Played: Day 22 ✓ Successfully saved Trish
```

**Data source:** Manual entry for Season 28 (research each advantage from episode summaries)

## Design & UX

### Navigation Structure

Update nav bar to:
```
Home | Tribal Councils | Castaways | Challenges | Events | Items
```

### Visual Consistency

- Maintain current Survivor theme (torch orange, bamboo borders, jungle green)
- Scrollable pages use same tribal-council card style
- Timeline events use consistent icon system (🔥 tribal, 🏆 challenge, 🔄 swap, 💎 advantage)

### Scrolling Philosophy

All views should be scrollable timelines except:
- **Home page:** Dashboard/overview (no scrolling needed)
- **Castaways:** Grid view with filters (already implemented)

## Technical Approach

### Data Requirements

**Existing data (voting_data.json):**
- ✅ Tribal councils, votes, castaways

**New data needed:**

1. **Challenge results** — Get from survivoR package
   - API: `challenge_results.json` for Season 28
   - Fields: `challenge_type`, `winners`, `day`, `episode`

2. **Items/advantages** — Manual research for Season 28
   - Structure:
   ```json
   {
     "items": [
       {
         "type": "Hidden Immunity Idol",
         "found_by": "Tony",
         "found_day": 11,
         "played_day": 22,
         "played_on": "Trish",
         "result": "successful",
         "voted_out_with": false
       }
     ]
   }
   ```

3. **Key events** — Partially from survivoR, partially manual
   - Tribe swaps: `tribe_mapping` dataset
   - Merge day: Episode 6, Day 19
   - Special twists: Manual entry

### Architecture

**Backend (app.py):**
- Add routes: `/challenges`, `/events`, `/items`
- Add route: `/tribal-councils` (replaces `/episodes`)
- Update data loading to include challenge results and items
- Add voting accuracy calculation function
- Add episode grading calculation function
- Add challenge beast metric calculation

**Frontend:**
- `templates/tribal_councils.html` — Replaces episodes.html, scrollable layout
- `templates/challenges.html` — New scrollable challenge timeline
- `templates/events.html` — New key events timeline
- `templates/items.html` — New advantage tracking view
- Update `templates/castaways.html` — Add voting accuracy, challenge beast metrics
- Update `templates/base.html` — New nav links

**Data files:**
- `data/challenges_s28.json` — Challenge results from survivoR
- `data/items_s28.json` — Manually curated advantages
- `data/events_s28.json` — Key events timeline

### Key Implementation Details

**Voting Accuracy Calculation:**
```python
def calculate_voting_accuracy(castaway_votes, eliminations):
    correct = 0
    total = len(castaway_votes)

    for vote in castaway_votes:
        tc_elimination = get_elimination_for_tc(vote['tc'], eliminations)
        if vote['voted_for'] == tc_elimination:
            correct += 1

    return (correct / total * 100) if total > 0 else 0
```

**Episode Grading Algorithm:**
```python
def grade_episode(tribal_council, items_played):
    score = 5.0  # Base

    if tribal_council['tribe'] == 'Merged':
        score += 2.0

    score += len(items_played) * 1.0

    vote_counts = [v['count'] for v in tribal_council['votes']]
    if len(vote_counts) >= 2 and abs(vote_counts[0] - vote_counts[1]) <= 2:
        score += 1.0

    unique_targets = len(tribal_council['votes'])
    if unique_targets > 2:
        score += (unique_targets - 2) * 0.5

    return min(score, 10.0)  # Cap at 10
```

**Challenge Beast Detection:**
```python
def calculate_challenge_beast_score(castaway, challenges, tribal_councils):
    immunity_wins = [c for c in challenges if c['winner'] == castaway['name'] and c['type'] == 'immunity']

    # Check if they were voted out immediately after losing immunity
    clutch_wins = 0
    for tc in tribal_councils:
        if castaway['name'] in [v for vote in tc['votes'] for v in vote['voters']]:
            # They received votes - check if they had immunity
            prev_challenge = get_previous_challenge(tc['day'], challenges)
            if prev_challenge and prev_challenge['winner'] == castaway['name']:
                clutch_wins += 1

    return {
        'immunity_wins': len(immunity_wins),
        'clutch_wins': clutch_wins
    }
```

## Files to Create/Modify

| File | Action | What |
|------|--------|------|
| `app.py` | Modify | Add routes for /tribal-councils, /challenges, /events, /items. Add calculation functions. |
| `data/challenges_s28.json` | Create | Challenge results from survivoR package |
| `data/items_s28.json` | Create | Manually curated advantage tracking |
| `data/events_s28.json` | Create | Key events timeline |
| `templates/tribal_councils.html` | Create | Scrollable tribal council view with episode grading |
| `templates/challenges.html` | Create | Challenge outcomes timeline |
| `templates/events.html` | Create | Key events timeline |
| `templates/items.html` | Create | Advantage/idol tracking view |
| `templates/castaways.html` | Modify | Add voting accuracy %, challenge beast metrics |
| `templates/base.html` | Modify | Update navigation with new links |
| `static/css/survivor.css` | Modify | Add styles for new views, flame rating system |

## Edge Cases & Constraints

**Voting Accuracy:**
- Exclude vote where player votes for themselves (final vote before elimination)
- Handle ties/revotes (count original vote, not revote)

**Challenge Data:**
- survivoR might not have detailed challenge descriptions — use generic "Immunity Challenge" if missing
- Some challenges are team-based pre-merge — attribute wins to all tribe members

**Items/Advantages:**
- Season 28 might have fewer advantages than modern seasons (older season)
- Some advantages might be found but never mentioned until played
- Research needed: Watch season or read episode summaries to capture all advantages

**Episode Grading:**
- Max score capped at 10
- Tribal councils without items/close votes might score low (5-6 range) — this is okay

**Key Events:**
- Not all seasons have tribe swaps — check Season 28 timeline
- Special twists are season-specific — research needed

## Open Questions

1. **survivoR data access:** Do we clone the repo and extract JSON, or is there an API? (Previous session showed we cloned the repo successfully)
2. **Items research:** Should we watch the season or read episode summaries to catalog advantages? (Suggest: Read Survivor Wiki episode summaries for Season 28)
3. **Future seasons:** This spec is Season 28-focused. When adding more seasons, do we generalize the data pipeline or manually curate each?

## Out of Scope

- **Alliance tracking** — Skipped per user request
- **Detailed challenge descriptions** — Just show type and winner, not play-by-play
- **Full drama narratives for items** — Just facts (who, when, result), not storytelling
- **Shareability features** — Not a priority yet, focus on data visualization
- **Multiple seasons** — Start with Season 28, expand later
- **Advanced visualizations** — No Sankey diagrams or network graphs yet, keep it simple scrollable timelines

---

## Implementation Plan

**Phase 1: Quick Wins (Ship Today)**
1. Scrollable tribal councils view
2. Voting accuracy % on castaways
3. Episode grading (can calculate with existing vote data, before adding items)

**Phase 2: Challenge Integration (Ship This Week)**
1. Extract challenge data from survivoR
2. Build /challenges view
3. Add challenge beast metrics to castaways

**Phase 3: Manual Curation (Ship Next Week)**
1. Research Season 28 advantages/idols
2. Build /items view
3. Build /events timeline
4. Update episode grading to include items
