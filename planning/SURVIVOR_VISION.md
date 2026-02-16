# Survivor Data Visualization Platform — Vision Document

**Last Updated**: 2026-02-15

---

## One-Liner

"The complete visual history of every Survivor season — explore alliances, blindsides, and winning strategies through interactive gameplay analysis."

---

## The Vision

An interactive web application that lets Survivor fans explore the strategic gameplay of every season, episode, and contestant. Track alliances, visualize voting patterns, analyze challenge performance, and understand what separates winners from losers.

### What Makes This Unique

Unlike existing Survivor databases (which are mostly tables and stats), this platform will:
1. **Visualize the social game** — Alliance networks, voting blocs, betrayals
2. **Grade player performance** — Was that move smart or dumb? Did they vote with their alliance?
3. **Track strategic evolution** — How did a player's game change episode-by-episode?
4. **Make the data shareable** — Screenshot-worthy visualizations of iconic moments
5. **Compare eras and strategies** — Old school vs new school gameplay analysis

---

## The Game of Survivor: Core Mechanics

### Pre-Merge Phase
- Multiple tribes compete against each other
- Losing tribe attends Tribal Council
- Immunity challenges determine which tribe is safe
- Reward challenges can provide advantages, food, etc.
- Players form alliances within their tribe

### Post-Merge Phase
- All remaining players join one tribe
- Individual immunity challenges (one winner gets immunity necklace)
- Everyone attends Tribal Council
- Cross-tribe alliances and voting blocs emerge
- Jury begins forming (voted-out players)

### Tribal Council
- Players vote to eliminate one contestant
- Hidden immunity idols can nullify votes
- Advantages can give extra votes, steal votes, etc.
- Person with most votes (after idols played) is eliminated
- Eliminated players join the jury

### Final Tribal Council & Jury Vote
- Final 2 or 3 players plead their case to the jury
- Jury votes for the winner
- Jury consists of recently eliminated contestants

### Old Era vs New Era

| Aspect | Old Era (S1-S40) | New Era (S41+) |
|--------|------------------|----------------|
| Season Length | 39 days | 26 days |
| Episode Count | 13-16 episodes | 13 episodes |
| Idols/Advantages | Basic hidden immunity idols | Many advantages: extra votes, vote steal, shot in the dark, beware advantages, knowledge is power, etc. |
| Gameplay Pace | Slower, social-focused | Fast-paced, advantage-heavy |
| Strategic Complexity | Alliance-based | Multi-layered with constant twists |

---

## Data Sources

### Primary: survivoR R Package
**GitHub**: https://github.com/doehm/survivoR
**Format**: JSON-ready R package with comprehensive data

**Available Datasets:**
- `castaways` — Full contestant info (name, age, city, occupation, result, jury status)
- `castaway_details` — Full results including vote history and order voted out
- `vote_history` — Complete voting record (who voted for who, when, idols played)
- `challenge_results` — Immunity and reward challenge winners by episode
- `jury_votes` — Final Tribal Council votes
- `season_summary` — Season metadata (location, filming dates, number of days)
- `viewers` — Episode ratings and viewership

**Survivor Stats DB**: https://survivorstatsdb.com/
Built on survivoR package, provides interactive web interface. Data available for download.

### Secondary Sources
- **True Dork Times**: https://truedorktimes.com/survivor/boxscores/data.htm
  Episode-by-episode scoring data in Google Sheets format

- **Survivor Wiki**: https://survivor.fandom.com
  Comprehensive wiki with detailed episode summaries, challenge descriptions

- **Kaggle Dataset**: https://www.kaggle.com/datasets/justinveiner/survivor-cbs-dataset
  Alternative dataset, may have different data structure

---

## User Experience Goals

### Three Core Exploration Modes

#### 1. Season Explorer
Navigate through a complete season chronologically:
- Episode-by-episode timeline
- See challenge results, vote outcomes, eliminations
- Watch alliances form and dissolve
- Identify blindsides and big moves

**Example Flow:**
```
Select Season 40 (Winners at War)
  → Episode 1: "The Greatest of the Greats"
    → Immunity Challenge: Red tribe wins
    → Tribal Council: Natalie voted out 4-2-1
    → Alliance Network: Cops-R-Us forms
  → Episode 2: "It's Like a Survivor Economy"
    → Reward Challenge: Blue tribe wins fishing gear
    → Immunity Challenge: Red tribe wins
    → Tribal Council: Amber voted out 6-1
    → First blindside: Alliance fractures
```

#### 2. Player Deep Dive
Click into any contestant to see their complete journey:
- Episode-by-episode performance metrics
- Challenge win/loss record (immunity & reward)
- Voting history (who they voted for, who voted for them)
- Alliance map (who they worked with, who betrayed them)
- Performance grade: did they make good moves?
- Key moments: blindsides executed/survived, idols played, immunity wins

**Metrics to Track:**
- Days survived
- Challenge wins (individual & tribal)
- Votes against (total)
- Idols found/played
- Alliances formed/maintained/broken
- Blindsides executed vs survived
- Jury votes received (if finalist)

**Performance Grading:**
- **Good moves**: Voting with the majority, successful blindsides, idol plays that worked
- **Bad moves**: Voting in the minority, failed idol plays, getting blindsided
- **Neutral**: Voting with clear majority, no immunity at stake

#### 3. Episode Analyzer
Zoom into a specific episode to see everything that happened:
- Challenge winners (immunity & reward)
- Vote breakdown (who voted for who)
- Idols/advantages played
- Alliances involved
- Did a blindside occur?
- Who was in danger but survived?

**Visualization Ideas:**
- Sankey diagram of votes (flow from voters to voted)
- Alliance network graph (nodes = players, edges = alliances)
- Timeline of episode events
- Before/after alliance state

---

## Key Features to Build

### Phase 1: Data Infrastructure
- [ ] Ingest survivoR package data (all seasons)
- [ ] Build database schema (seasons, episodes, contestants, votes, challenges, alliances)
- [ ] Create API endpoints for querying data
- [ ] Data validation and cleaning pipeline

### Phase 2: Core Visualizations
- [ ] Season timeline view (episode-by-episode)
- [ ] Player journey view (contestant deep dive)
- [ ] Episode detail view (challenges, votes, eliminations)
- [ ] Voting visualization (Sankey or chord diagram)
- [ ] Alliance network graph

### Phase 3: Analysis & Grading
- [ ] Blindside detection algorithm
- [ ] Alliance tracking (who worked with who, when)
- [ ] Move quality grading (good/bad/neutral)
- [ ] Challenge performance metrics
- [ ] "What if" scenarios (if X voted differently)

### Phase 4: Shareability
- [ ] Screenshot-worthy stat cards
- [ ] "Your Survivor Style" quiz (which player archetype are you?)
- [ ] Season superlatives (biggest blindside, best social game, etc.)
- [ ] Player comparison tool

---

## Data Structure (Initial Schema)

### Seasons
```json
{
  "season_id": 40,
  "season_name": "Winners at War",
  "location": "Fiji",
  "filming_dates": "2019-05-20 to 2019-06-27",
  "days": 39,
  "episodes": 14,
  "num_castaways": 20,
  "winner": "Tony Vlachos",
  "runner_ups": ["Natalie Anderson", "Michele Fitzgerald"]
}
```

### Episodes
```json
{
  "episode_id": "S40E01",
  "season_id": 40,
  "episode_num": 1,
  "title": "The Greatest of the Greats",
  "air_date": "2020-02-12",
  "immunity_challenge": {
    "winner": "Dakal (red tribe)",
    "challenge_type": "tribal"
  },
  "reward_challenge": {
    "winner": "Sele (blue tribe)",
    "reward": "Flint"
  },
  "tribal_council": {
    "eliminated": "Natalie Anderson",
    "vote_count": {"Natalie": 4, "Jeremy": 2, "Denise": 1},
    "idols_played": []
  }
}
```

### Players
```json
{
  "player_id": "tony-vlachos-s40",
  "name": "Tony Vlachos",
  "season": 40,
  "age": 45,
  "occupation": "Police Officer",
  "tribe": "Dakal",
  "days_lasted": 39,
  "placement": 1,
  "jury_votes": 12,
  "challenges_won": 5,
  "idols_found": 3,
  "votes_against": 6
}
```

### Votes
```json
{
  "vote_id": "S40E01-tribal",
  "episode": "S40E01",
  "voter": "Tony Vlachos",
  "voted_for": "Natalie Anderson",
  "vote_nullified": false,
  "alliance": "Cops-R-Us"
}
```

### Alliances
```json
{
  "alliance_id": "cops-r-us-s40",
  "season": 40,
  "name": "Cops-R-Us",
  "members": ["Tony Vlachos", "Sarah Lacina"],
  "formed_episode": "S40E01",
  "dissolved_episode": null,
  "betrayals": []
}
```

---

## UI/UX Inspiration

### Visual Style
- **Dark mode first** — Dramatic, torch-lit aesthetic
- **Tribal/survivalist theme** — Earthy colors, texture
- **Network graphs** — D3.js or similar for alliance visualization
- **Timeline scrubbing** — Horizontal episode timeline with key moments
- **Card-based layouts** — Player cards, episode cards, moment cards

### Interaction Patterns
- Click player → See their full journey
- Click episode → See all events in that episode
- Hover vote → Highlight alliance connections
- Scrub timeline → Watch alliances evolve over time
- Filter by era → Compare old school vs new school

### Shareable Moments
- "Your Survivor Archetype" results
- Player comparison cards (X vs Y)
- "Most shocking blindside" of a season
- Challenge win streaks
- Alliance betrayal graphs

---

## Technical Stack (Proposed)

### Backend
- **Python/Flask** — Existing stack from Fantasy Football project
- **Database** — SQLite or PostgreSQL for storing processed data
- **Data Pipeline** — survivoR R package → JSON → Python ingestion

### Frontend
- **Vanilla JS** — Keep it simple, existing pattern
- **D3.js** — Network graphs and visualizations
- **Canvas** — Potentially for alliance network rendering

### Deployment
- **Railway** — Existing hosting solution
- **Domain** — TBD (survivor-wrapped.com? survivor-viz.com?)

---

## Open Questions

1. **Alliance Detection**: How do we automatically detect alliances from vote data? May need manual curation for some seasons.

2. **Move Quality Grading**: What's the algorithm for "good" vs "bad" moves?
   - Did they vote with the majority? (safe move)
   - Did they execute a blindside? (aggressive move)
   - Did they get blindsided? (bad awareness)
   - Did they flip alliances successfully? (strategic move)

3. **Old vs New Era**: Should we separate these into different views or blend them?

4. **Data Completeness**: Does survivoR package have all 49 seasons? Need to verify coverage.

5. **Alliance Data**: Vote history tells us who voted together, but not who was "in an alliance." May need to infer from voting patterns or manually curate.

6. **UI Direction**: Timeline? Map-based (like Mario World)? Card-based? Network graph-centric?

---

## Success Metrics

- Users can explore any season and understand the strategic gameplay
- Users can follow a player's journey from start to finish
- Users can identify key moments (blindsides, idol plays, challenge streaks)
- Visualizations are shareable and screenshot-worthy
- Performance grading feels accurate and insightful

---

## Next Steps

1. **Verify survivoR data coverage** — Check if all 49 seasons are available
2. **Test data ingestion** — Pull one season's data and explore structure
3. **Prototype one visualization** — Start with voting Sankey diagram for one episode
4. **Define alliance detection rules** — Algorithm or manual curation?
5. **Sketch UI mockups** — What does the season explorer actually look like?

---

## Related Resources

- survivoR Package: https://github.com/doehm/survivoR
- Survivor Stats DB: https://survivorstatsdb.com/
- True Dork Times: https://truedorktimes.com/survivor/boxscores/data.htm
- Survivor Wiki: https://survivor.fandom.com
- Immunity Challenge Info: https://survivor.fandom.com/wiki/Immunity_Challenge
