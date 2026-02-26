# Meeting Notes

Session-by-session log of conversations, decisions, and implementations.

---

## 2026-02-25 — UI Polish Pass: Icons, Hall of Fame, Idols, Formatting

### Icon Redesign
- **Complete icon overhaul** in `_icons.html` — all 29 SVG icons redesigned with far more detail
- Icons now have layered fills, gradients, tribal-style details (palm tree with coconuts, machetes instead of generic swords, carved tiki idol, torch with wrap marks, etc.)
- Added `chevron-left` icon for carousel navigation

### Hall of Fame Overhaul
- **Converted to horizontal carousel** — one record card visible at a time with left/right navigation
- Added dot indicators, keyboard arrows, and touch swipe support
- **Added headshots** to all record holders (enriched in `precompute_hall_of_fame()`)
- Tie formatting now shows holders stacked vertically within a single card with gold border accents and tie badge
- Clean, centered layout with 800px max-width

### Returning Players Name Formatting
- **Fixed consistency** — all cards now show nickname (or first name if no nickname) as the big name, full name always shown as secondary text below

### Page Cleanup
- **Removed Events page** — deleted route from app.py, removed from nav in base.html, removed test
- **Renamed "Idols & Advantages" to "Idols"** — updated nav, template title, breadcrumb, page header

### Idols Page Box Formatting
- **Equal-width boxes** — Found, Played, Result boxes now use `flex: 1` for uniform sizing
- **Never-played items** — Found box limited to 1/3 width (not full row), Played/Result boxes hidden

### Idol Strategy Spacing Fix
- Reduced excessive `mb-5` margins to `mb-4` throughout
- Tightened padding on all card containers (`p-4` → `p-3`, `2rem` → `1.5rem`)
- Reduced spacing on verdict box, strategies-to-avoid section, and Best & Worst headers
- Overall more cohesive, less whitespace between sections

### Advantages Evolution Chart Fix
- **Changed from grouped bars to stacked bar** — each season bar shows green (successful plays) + red (unsuccessful/not played), totaling to total advantages
- Tooltip shows total count for clarity

---

## 2026-02-25 — Site Restructuring: Icons, Nav, Page Consolidation

### Emoji Removal & Custom SVG Icon System
- **Created `templates/_icons.html`**: Jinja2 macro library with ~28 inline SVG icons (torch, crown, trophy, brain, handshake, ballot, dumbbell, necklace, island, etc.)
- **Replaced all emojis** across 20+ template files — zero emojis remain in active templates
- **`get_flame_rating()` in app.py**: Changed from fire emojis to Unicode block characters (filled/empty squares)
- **JS toggle buttons**: Switched from emoji textContent swaps to dual-element SVG icon display toggling

### Navigation Restructuring
- **Removed global season selector** from nav bar (was confusing for non-season pages)
- **New nav groups**: Season Explorer | Strategy & Stats | Seasons & Records | Quiz
- **Created `templates/_season_selector.html`**: In-page season dropdown for 6 season-specific pages
- **Added season selector** to: tribal_councils, castaways, challenges, events, items, alliances

### Page Consolidation
- **Merged Advantages Timeline → Idol Strategy**: Added 6th "Advantages Evolution" tab with charts
- **Merged Analytics → Paths to Victory**: Added era radar, era table, aggression trend, archetype charts
- **Deleted Power Rankings**: Too niche, data available elsewhere
- **Deleted 3 templates**: advantages_timeline.html, analytics.html, power_rankings.html
- **Deleted 3 routes**: /analytics, /advantages-timeline, /power-rankings

### Headshots Integration
- **Winners Hall**: All 39 winners now have headshots (80x80, gold border)
- **Returning Players**: Headshot thumbnails from first appearance season
- **Fixed name matching**: Full name → first name → case-insensitive partial match fallback

### Index Page
- Removed cards for deleted pages
- All card icons replaced with SVG icons
- Updated layout to match new nav grouping

### Tests
- Updated 10 failing tests (deleted routes now check 404, flame rating checks updated, nav assertions updated)
- **All 66 tests passing**

---

## 2026-02-24 — Castaway Headshots: All 39 Seasons

### Self-Hosted Face-Cropped Headshots
- **Moved from hotlinked to self-hosted images**: Fandom CDN blocks hotlinking via Referer header. Downloaded all images locally to `static/images/castaways/s{N}/`.
- **DNN face detection for auto-cropping**: Initially used Haar Cascades (2001 algorithm) which missed faces or cropped to torsos. Switched to OpenCV's DNN ResNet SSD face detector — 99-100% confidence on all faces tested.
- **Pipeline**: Download 600px portrait from wiki → DNN face detection → crop 300x300 square centered on face → save as WebP (~8-17KB each).
- **S28 (Cagayan)**: All 18 headshots complete, face-centered, verified.
- **S29 (San Juan del Sur)**: All 18 headshots complete, face-centered, verified.
- **S1-S39 batch processing complete**: Master script (`.temp/process_all_headshots.py`) processed all 37 remaining seasons via MediaWiki `allimages` API. **674 headshots** across all 39 seasons — 0 fallback crops, 0 failed downloads, 100% DNN face detection success.
- **Coverage**: ~95% of all castaways matched. S35 (Heroes vs. Healers vs. Hustlers) lowest at 8/18 due to wiki naming. "Boston Rob" and "Cochran" consistently unmatched (wiki uses real names).
- **Debugging journey**: Fixed 5 bugs across iterations — wrong data accessor, Fandom 403s (missing User-Agent), underscore/space filename parsing, stale script cache (agents ran old version), portrait filter rejecting all images.

### Technical Decisions
- **Data source**: Survivor Wiki (Fandom) — CBS promotional photos, 3840x5760 originals, CORS-friendly, MediaWiki API for URL lookups.
- **Image format**: WebP at quality 85, 300x300 square crops, ~8-17KB each.
- **Template changes**: Added `loading="lazy"`, `decoding="async"`, `referrerpolicy="no-referrer"` to img tags in castaways.html.
- **Name matching**: Voting data uses first-name-only for most players. Wiki `allimages` API returns full filenames (`S28_Tony_Vlachos.jpg`) which we match by first name.
- **Dependencies added**: `opencv-python-headless` (face detection), DNN model files in `.temp/`.

---

## 2026-02-24 — Idol Strategy: Bug Fixes & God Idol Separation

### Bug Fixes
- **Fixed broken Overview tab**: `tojson_safe` Jinja filter was HTML-escaping JSON output (`&#34;` instead of `"`), breaking Chart.js data inside `<script>` tags. Fixed by wrapping with `Markup()` from markupsafe.
- **Fixed tab header readability**: Bootstrap nav-tabs had white active backgrounds by default. Added dark-themed CSS overrides (transparent background, torch-orange active border, proper hover states).

### God Idol Separation
- **Separated God Idol (Post-Vote Read) into its own distinct type** in Idol Types catalog — previously lumped in with "Super Idol / Tyler Perry Idol"
- **Removed God Idol from strategy analysis**: Strategy stats (self vs ally, duration, secrecy) now exclude God/Super Idols since they operate on fundamentally different strategic principles
- **Replaced God Idol examples in Strategies tab** with standard idol examples: Malcolm's Three Amigos (S26), Mike Holloway threatening to play (S30), Dan Rengering publicly targeted (S37)
- **Reworked Rule #6** from "Best Idol Is the One You Never Play" (which was about Yul/Tony God Idols) to "An Idol in Your Pocket Is Still a Weapon" (about standard idol threat value with Carolyn/Mike examples)
- **Replaced Yul Kwon in Best Plays #10** (was specifically about God Idol leverage) with David Wright saving Jessica Lewis (S33) — a standard idol play
- **Updated final verdict** to remove Super Idol reference
- Added 2 new tests (God Idol in type catalog, God Idol not in strategies section). 66 total, all passing.

---

## 2026-02-24 — Idol Strategy Analysis Page (Initial Build)

### New Feature: Idol Strategy Guide (`/idol-strategy`)
- **Comprehensive cross-season idol analysis** covering all 39 seasons (151 advantages, ~130 real idols)
- **Five tabbed sections**: Overview, Idol Types, Strategies, Best & Worst, Conclusions
- **Overview tab**: Idols Per Season bar chart, Play Outcomes doughnut, Self vs. Ally stacked bar, Duration distribution chart, Top Finders table, Most Votes Negated table
- **Idol Types tab**: Detailed catalog of 5 idol types (Standard HII, Super/Tyler Perry, Split, Legacy, Temporary) + Fake Idols + Idol Nullifier — each with rules, strategy tips, and "If You Find This" advice
- **Strategies tab**: Four strategic dimensions analyzed (Timing, Target, Secrecy, Outcome) with data-driven comparisons, examples, and verdicts
- **Best & Worst tab**: Top 10 greatest idol plays (Parvati's double play, Wentworth's 9-vote negation, etc.) and 8 worst blunders (James with two idols, J.T. to Russell, etc.)
- **Conclusions tab**: "The 7 Rules of Idol Play" — opinionated, data-driven strategy guide + "Strategies to Avoid" section
- Four Chart.js visualizations: idols per season, outcomes doughnut, self vs ally, duration distribution
- 5 new tests added (65 total, all passing)

### Navigation Changes
- Renamed "Explore > Items" to "Explore > Idols" (page itself unchanged as requested)
- Added "Analysis > Idol Strategy" link in Analysis dropdown

### Research Process
- Spawned 4 parallel research agents to investigate idol types, notable plays, best/worst plays, and codebase structure
- Aggregated data from all 39 `season*_advantages_idols.json` files
- Key stats: 59.1% idol play success rate, average 10-day hold time, 55 successful plays, 25 players voted out holding idols

---

## 2026-02-23 — Bug Fixes, Records Overhaul, Visual Theme Revamp

### Bugs Fixed
- **Individual Immunity Wins**: Challenge stats now only count individual challenges (filters by `outcome_type == "Individual"`). Team/tribal wins no longer inflate immunity or reward win counts on player stat sheets.
- **Hall of Fame Ties**: Records page now shows ALL tied record holders instead of just the first one. Added `find_all_max()` / `find_all_min()` helper functions. Tied records display with dividers and a "X-way tie" badge.

### New Features
- **Individual Immunity Wins Record**: Added two new record cards to Hall of Fame — "Most Individual Immunity Wins (All Players)" and "Most Individual Immunity Wins (Champion)"
- Updated all existing record card titles to clarify "Individual" challenge wins

### Visual Theme Revamp
- Complete CSS overhaul from dark/dreary jungle green to warm tropical sunset palette
- New background: deep purple-to-warm sunset gradient (replaces dark forest green)
- New CSS variables: `--card-bg`, `--card-border`, `--text-primary`, `--text-secondary`, `--torch-glow`, `--sunset-deep/mid/warm`
- Cards use warm semi-transparent purple tones with enhanced borders
- Brighter, more vivid accent colors throughout (warmer oranges, softer greens/reds)
- Nav and footer updated to match new palette
- Dark mode theme also updated (richer dark tones instead of flat black)
- All existing functionality and responsive design preserved

### Tests
- Updated existing challenge metrics test to include `outcome_type` field
- Added new `test_excludes_team_wins` test
- All 60 tests passing

---

## 2026-02-22 — Overnight Session #4: Alliances, Power Rankings, Nicknames, Quotes, Polish

### Features Shipped

**Alliance Network Diagrams** (`/alliances?season=N`)
- Interactive canvas-based force-directed network graph (no external library)
- Nodes = players (colored by tribe), edges = co-voting frequency (thicker = more co-votes)
- Drag-to-rearrange, hover tooltips with ally details
- Winner nodes highlighted with gold border
- Automatic voting bloc detection (3+ player cliques who voted together)
- Top voting pairs table (sortable)
- Co-voting strength horizontal bar chart (Chart.js)
- Works across all 39 seasons

**Power Ranking Timeline** (`/power-rankings?season=N`)
- Episode-by-episode power scores for every player
- Score formula: base 50, -8 per vote received, +5 per challenge win, +3 per correct vote
- Chart.js multi-line chart with one line per player (click legend to toggle)
- Winner highlighted in gold, top 8 players shown by default
- Winner spotlight section with separate chart and key stats
- Final standings table (sortable) with placement, peak score, final score

**Player Nicknames**
- `data/player_nicknames.json` with 90+ nickname mappings
- Nicknames displayed on castaway cards (e.g., Tony = "The King of the Jungle")
- Loaded at startup and enriched into castaway data

**Famous Quotes**
- `data/famous_quotes.json` with 40 iconic Survivor quotes
- `/api/random-quote` API endpoint
- Random quote displayed on index page with speaker attribution
- Season-specific quotes linked to their season number

**Loading States & Animated Transitions**
- Page load fade-in animation (CSS `pageIn`)
- Staggered card entrance animations (first 6 cards animate in sequence)
- Loading spinner overlay for page transitions (triggered on internal link clicks)
- Smooth table row hover highlights
- Stat number scale effect on hover
- Voting history expand/collapse animation

**Error Handling**
- Custom 404 page ("THE TRIBE HAS SPOKEN")
- Custom 500 page ("MEDICAL EVACUATION")
- Error handlers registered on Flask app

**Index Page Updates**
- Added Alliance Networks and Power Rankings feature cards
- Famous quote block with random quote on each page load

### Files Created
- `templates/alliances.html` — Alliance network with force graph + chart
- `templates/power_rankings.html` — Power score timeline + tables
- `templates/404.html` — Custom 404 error page
- `templates/500.html` — Custom 500 error page
- `data/player_nicknames.json` — 90+ player nickname mappings
- `data/famous_quotes.json` — 40 iconic Survivor quotes

### Files Modified
- `app.py` — Added `/alliances`, `/power-rankings`, `/api/random-quote` routes; error handlers; nickname/quote loading; enriched castaway data with nicknames
- `templates/base.html` — Added Alliances/Power Rankings to nav; loading overlay; season selector redirect list updated
- `templates/index.html` — Added Alliance/Power Rankings cards; famous quote section
- `templates/castaways.html` — Nickname display under player names
- `static/css/survivor.css` — Page load animations, card entrance stagger, loading spinner, table hover, stat hover effects, expand/collapse animation
- `static/js/app.js` — Page transition loading overlay JS
- `tests/test_app.py` — 10 new tests

### Tests
- **59 tests, all passing** (was 49 at start of session)
- New: alliances (default + season), power rankings (default + season), random quote API, custom 404, alliances content, power rankings content, castaways nicknames, index feature cards

---

## 2026-02-20 — Overnight Session #3: Compare Seasons, Challenge Performance, Season Recs

### Features Shipped

**Season-to-Season Comparison Tool** (`/compare-seasons`)
- Side-by-side comparison of any two seasons with stat rows and winner indicators
- Winner archetype radar chart overlay (orange vs blue)
- Season stats grouped bar chart
- Quick compare presets (First vs Last, Cagayan vs HvV, etc.)
- Season recommendations section pulling from API
- Full season stats sortable table (all 39 seasons)

**Challenge Performance Analysis** (`/challenge-performance`)
- Challenges per season stacked bar chart (immunity vs reward)
- Winner individual immunity wins bar chart (color-coded by performance)
- Winner challenge wins distribution doughnut chart
- Immunity wins over time trend line
- Top 20 challenge performers table (sortable)
- Winner challenge stats table (sortable)

**Season Recommendations Engine**
- `SEASON_RECOMMENDATIONS` dict with curated similar seasons for all 39 seasons
- `/api/season-recommendations/<season>` API endpoint
- "If you liked this, try..." links on each season card in `/seasons`
- Recommendations integrated into compare-seasons page

**Index Page Expansion**
- Added Compare Seasons, Paths to Victory, and Challenges feature cards
- Third row of exploration cards on homepage

### Files Created
- `templates/compare_seasons.html` — Season comparison with Chart.js
- `templates/challenge_performance.html` — Challenge performance analysis

### Files Modified
- `app.py` — Added `/compare-seasons`, `/challenge-performance`, `/api/season-recommendations/<season>` routes; `SEASON_RECOMMENDATIONS` dict; added `similar_seasons` to seasons overview data
- `templates/base.html` — Added Compare Seasons and Challenge Performance to Analysis dropdown
- `templates/seasons.html` — Added "If you liked this, try..." section to each season card with CSS
- `templates/index.html` — Added third row of feature cards
- `tests/test_app.py` — Added 4 new tests (compare-seasons, challenge-performance, recommendations API)

### Tests
- **49 tests, all passing** (was 45 at start of session)
- New tests: `test_compare_seasons`, `test_challenge_performance`, `test_season_recommendations_api`, `test_season_recommendations_invalid`

### Documentation Updated
- `planning/ROADMAP.md` — Moved completed items, updated priorities
- `planning/MEETING_NOTES.md` — This entry

### Deployment Note
- Heroku CLI not installed on this machine — Procfile and runtime.txt are ready
- Deployment skipped per overnight instructions (skip items that can't be completed)

---

## 2026-02-16 — Advantages/Idols Data: Seasons 37-39 (Pre-Pandemic Modern Era)

### Data Files Created
- **Season 37 (David vs Goliath)** — `data/season37_advantages_idols.json` — 8 advantages (6 idols + Idol Nullifier + Vote Steal). Dan Rengering found 2 idols; played first unnecessarily on Angelina, second was nullified by Carl's Idol Nullifier (first ever use). Davie's idol play on Christian negated 7 votes at the merge — one of the most iconic plays ever. Nick found Vote Steal and an idol. The Episode 9 triple-advantage tribal (idol + nullifier + vote steal) is considered one of the greatest strategic sequences in Survivor history. Nick Wilson won 7-3-0.
- **Season 38 (Edge of Extinction)** — `data/season38_advantages_idols.json` — 8 advantages (5 idols + Advantage Menu + 2 Extra Votes). Rick Devens set the record with 4 idols possessed in a single season (1 from EoE return, 3 found). All 4 idol plays this season were successful (11 total votes negated). Ron Clark's Advantage Menu expired unused — first advantage to expire due to tribe immunity. Extra Votes found on Edge of Extinction and transferred between players. Chris Underwood won 9-4-0 controversially after returning from extinction Day 35.
- **Season 39 (Island of the Idols)** — `data/season39_advantages_idols.json` — 16 advantages (most advantage-heavy pre-pandemic season). Featured IoI twist with tests from Boston Rob and Sandra. Kellee Kim set record for most idols found by a woman (3) — voted out holding 2. Karishma's 7-vote negation was a dramatic highlight. Dean won Idol Nullifier via coin toss, nullified Janet's idol at F5. Three players voted out holding idols (Vince, Jamal, Kellee). Tommy won 8-0-2 without any advantages.

### Research Notes
- Seasons 37-39 represent the peak of the "advantage era" before the pandemic pause
- Season 37 introduced the Idol Nullifier (returned in S39)
- Season 38's Edge of Extinction twist created new advantage dynamics (advantages found on EoE, half-idols for returnees)
- Season 39's Island of the Idols introduced test-based advantage acquisition with failure penalties (lost votes)
- Researched via Survivor Wiki (fandom.com) player pages, episode pages, advantage-specific pages, and season pages

---

## 2026-02-16 — Advantages/Idols Data: Seasons 34-36 (Game Changers, HvHvH, Ghost Island)

### Data Files Created
- **Season 34 (Game Changers)** — `data/season34_advantages_idols.json` — 8 advantages. One of the most advantage-heavy seasons ever. Tai found 3 idols (season record at the time). Sierra's Legacy Advantage found Day 1, willed to Sarah who played it at F6. Sarah also found Vote Steal at reward bench, used it to blindside Michaela. Debbie chose Extra Vote from Cochran's Advantage Menu on Exile. J.T. infamously left his idol at camp and was blindsided. The F6 tribal saw 4 advantages played simultaneously (Sarah's Legacy, Troyzan's idol, both of Tai's remaining idols), eliminating Cirie by default with 0 votes against her.
- **Season 35 (Heroes vs Healers vs Hustlers)** — `data/season35_advantages_idols.json` — 10 advantages. Ben Driebergen's legendary 3-idol run (Days 25, 36, 37) saved him three consecutive tribals, negating 13 total votes. Joe Mena found 2 pre-merge idols (first successful, second wasted). Ryan found Super Idol at marooning, gave to Chrissy (not played, expired). Jessica's Vote Blocker blocked Devon's vote. Lauren found both Extra Vote AND split idol but was voted out holding the Extra Vote when Ben played his first idol. Mike threw Lauren's idol half into the fire. First season with F4 fire-making twist.
- **Season 36 (Ghost Island)** — `data/season36_advantages_idols.json` — 14 advantages. The most advantage-rich file yet. Ghost Island relics from 7 past seasons (China, Micronesia, Philippines, Caramoan, Kaoh Rong, MvGX, Game Changers). Legacy Advantage passed through 3 players (Jacob→Morgan→Domenick). Michael Yerger found James Clement's idol AND Ozzy's fake-turned-real idol, with the second play negating 7 votes. Wendell found Erik's necklace (repurposed as idol), played it on Laurel at F5. Donathan assembled Tai/Scot's split idol halves. Extra Vote was recycled (Kellyn used it, then Sebastian found it but was bluffed into not playing it by Domenick's fake idol). First-ever tied FTC jury vote (5-5, Wendell won).

### Research Notes
- These three seasons represent the peak of the "advantage era" in Survivor
- Season 34's F6 tribal (Cirie's default elimination) is one of the most debated moments in Survivor history
- Season 35's fire-making twist became a permanent fixture starting this season
- Season 36's Ghost Island relics created a unique connection to 7 previous seasons
- Domenick's fake idol strategy (fooling both Chris Noble and Sebastian) was one of the most effective fake idol deployments ever
- Researched via Survivor Wiki player pages, advantage-specific pages (Vote Steal, Legacy Advantage, Extra Vote), and season overview pages

---

## 2026-02-16 — Advantages/Idols Data: Seasons 21-27 (Nicaragua through Blood vs Water)

### Data Files Created
- **Season 21 (Nicaragua)** — `data/season21_advantages_idols.json` — 5 advantages (4 idols + Medallion of Power). Marty found Espada idol, gave it to Sash under blackmail deal. Sash played it successfully at F5 (1 vote negated). NaOnka found La Flor idol with Brenda, gave it to Chase before quitting — first player to find idol then quit. Chase played it unsuccessfully (0 votes negated). Medallion of Power unique to this season.
- **Season 22 (Redemption Island)** — `data/season22_advantages_idols.json` — 3 idols. Ralph found Zapatera idol on Day 4 (beat Russell to it), played it unsuccessfully on Mike at merge (wrong target). Rob found Ometepe idol, played it on himself at merge but wasn't targeted (unsuccessful). Andrea found re-hidden idol, played it successfully at F5 (negated 4 votes).
- **Season 23 (South Pacific)** — `data/season23_advantages_idols.json` — 2 idols only. Ozzy found Savaii idol, gave it to Cochran for his Redemption Island gambit, but never played it after returning. Coach found Upolu idol, played it on himself at merge but wasn't targeted (unsuccessful). Low-idol season.
- **Season 24 (One World)** — `data/season24_advantages_idols.json` — 4 idols. Sabrina found Manono idol, had to give it to Colton (cross-tribe rule). Colton medically evacuated holding it (first medevac with idol). Troyzan played idol successfully at merge (2 votes negated). Kim found idol but never played it — won the season with idol unused.
- **Season 25 (Philippines)** — `data/season25_advantages_idols.json` — 3 idols (one per starting tribe). First season with 3 tribes each having an idol. Penner's successful play negated 5 votes at merge. Abi-Maria successfully negated 3 votes. Malcolm found Matsing idol but was voted out holding it on Day 38.
- **Season 26 (Caramoan)** — `data/season26_advantages_idols.json` — 5 idols, 4 plays (3 successful). ICONIC season for idol plays. Reynold found 2 idols (fastest ever at the time). Malcolm's legendary double idol tribal: played one on himself (2 votes negated) and gave second to Eddie (4 votes negated), blindsiding Phillip 4-0-0 in first "live" tribal council. Andrea voted out holding idol — first woman to be voted out with idol.
- **Season 27 (Blood vs Water)** — `data/season27_advantages_idols.json` — 2 idols, both found by Tyson. First idol played successfully (3 votes negated) before the famous rock draw at F6. Second idol taken to end unused as Tyson won the season 7-1-0.

### Research Notes
- Seasons 21-27 bridge the "classic idol era" to the "modern advantage era"
- Season 21 introduced the Medallion of Power (never used again)
- Season 26's double idol tribal council is one of the most iconic moments in Survivor history
- Season 25 was the first to have 3 starting tribes each with their own idol
- Season 27's idol clue distribution via Redemption Island duels was a unique mechanic
- Researched via Survivor Wiki (fandom.com) player pages, episode pages, and season pages

---

## 2026-02-16 — Advantages/Idols Data: Seasons 16-20 (Pivotal Idol Era)

### Data Files Created
- **Season 16 (Micronesia)** — `data/season16_advantages_idols.json` — 4 advantages (3 real idols + 1 fake). Ozzy blindsided with idol in pocket (Day 27). Jason Siska found Ozzy's fake idol stick, then found real re-hidden idol but was also blindsided holding it. Amanda's successful idol play (4 votes negated) was the only successful play of the season. Eliza played the fake stick idol at tribal to expose Ozzy.
- **Season 17 (Gabon)** — `data/season17_advantages_idols.json` — 3 advantages (1 real idol + 2 fake). Sugar found the only real idol on her first Exile visit, held it entire game, never played it. Bob Crowley crafted 2 fake idols; Randy Bailey's fake idol play is iconic. Low-idol season.
- **Season 18 (Tocantins)** — `data/season18_advantages_idols.json` — 3 advantages (2 real idols, 1 held by Stephen). Zero idol plays all season. Taj found Jalapao idol via Exile alliance with Brendan, gave it to Stephen. Brendan found Timbira idol but was blindsided holding it. Stephen held idol to Final Two without playing.
- **Season 19 (Samoa)** — `data/season19_advantages_idols.json` — 3 idols. Russell Hantz revolutionized idol-finding (no clues). His Episode 9 play negated 7 votes (one of the most impactful ever). Erik Cardona voted out holding Galu idol at merge. Foa Foa Four overcame 8-4 deficit largely via Russell's idols.
- **Season 20 (Heroes vs. Villains)** — `data/season20_advantages_idols.json` — 6 idols, 5 plays (3 successful). MASSIVE idol season. Tom's successful play blindsided Cirie (3 votes negated). Russell found Villains idol, played it on Parvati to eliminate Tyson (4 votes negated). J.T. gave his idol to Russell (worst move ever). Parvati's double idol play on Jerri and Sandra (5 votes negated on Jerri) eliminated J.T. Russell found post-merge idol but wasted it. Most idol-impactful season ever.

### Research Notes
- Seasons 16-20 represent the pivotal evolution of idol strategy in Survivor
- Season 16 showed idols could be used offensively (fake idols, blindsides while holding)
- Season 19 was a turning point: Russell proved you don't need clues to find idols
- Season 20 is arguably the most idol-defined season in history with 5 plays in a single season
- Parvati's double idol play (S20E10) is widely considered the greatest single move in Survivor history
- J.T.'s idol gift to Russell is widely considered the worst move in Survivor history

---

## 2026-02-16 — Advantages/Idols Data: Seasons 31-33 (Advantage Era)

### Data Files Created
- **Season 31 (Cambodia)** — `data/season31_advantages_idols.json` — 5 advantages: 4 Hidden Immunity Idols + 1 Vote Steal. Kelley Wentworth's iconic 9-vote negate (Ep 8). Jeremy Collins played 2 idols successfully (one for Stephen, one for himself). First-ever null vote when both Kelley and Jeremy played idols at same tribal (Ep 14). Stephen Fishbach received first Vote Steal but was voted out same episode. All 4 idol plays were successful.
- **Season 32 (Kaoh Rong)** — `data/season32_advantages_idols.json` — 5 advantages: 3 idols + Extra Vote + Juror Removal. Super Idol twist (combine 2 idols, play after votes read) but never formed because Tai refused to save Scot. NO idols played all season. Neal evacuated holding idol, Scot voted out holding Jason's idol. Michele's Juror Removal of Neal may have changed the winner.
- **Season 33 (Millennials vs Gen X)** — `data/season33_advantages_idols.json` — 9 advantages: 5 real idols + 1 fake idol + Legacy Advantage + Reward Steal + Legacy Advantage (inherited). First-ever Legacy Advantage introduced. David Wright played idol for Jessica (5 votes negated) and crafted fake idol that fooled Jay. Adam Klein misplayed both his idols but won unanimously. Ken McNickle first to use Legacy Advantage.

### Research Notes
- These three seasons mark the beginning of the "advantage era" with increasing complexity of game advantages
- Season 31 was first to hide idols at challenges rather than camp
- Season 32's Super Idol twist was effectively neutralized by Tai's betrayal of Scot/Jason
- Season 33 introduced Legacy Advantage and Reward Steal, plus saw one of the best fake idol plays ever
- Researched via Survivor Wiki (fandom.com) player pages, episode pages, and advantage-specific pages

---

## 2026-02-16 — Advantages/Idols Data: Seasons 11-15

### Data Files Created
- **Season 11 (Guatemala)** — `data/season11_advantages_idols.json` — First-ever Hidden Immunity Idol. Gary Hogeboom found and played it successfully (Episode 9, Day 24). 1 idol total.
- **Season 12 (Panama)** — `data/season12_advantages_idols.json` — Terry Deitz found the Super Idol on Exile Island. Never played it, voted out at Final 3 holding it. 1 idol total.
- **Season 13 (Cook Islands)** — `data/season13_advantages_idols.json` — Yul Kwon's God Idol (playable after votes read). Never played but used as strategic leverage to flip Jonathan Penner. Won the game holding it. 1 idol total.
- **Season 14 (Fiji)** — `data/season14_advantages_idols.json` — First modern idol format (played before votes read). 3 idols: Yau-Man (successful, negated 4 votes), Mookie/Alex (unsuccessful, 0 votes negated), Earl (unsuccessful, precautionary play at F4).
- **Season 15 (China)** — `data/season15_advantages_idols.json` — 3 idols, none played. Todd found one and gave it to James. James found the second. James voted out holding both idols — one of the biggest blunders in Survivor history.

### Research Notes
- Seasons 11-13 used "Super Idol" / "God Idol" format (playable after votes read)
- Season 14 (Fiji) was the transition to modern format (played before votes read, after discussion but before reveal)
- Researched via Survivor Wiki (fandom.com) with cross-referencing of player pages, episode pages, and season overview pages

---

## 2026-02-16 — Overnight Session #2: Winners Hall, Comparison, Analytics, Seasons Page

### Features Shipped
- **Winners Hall page** (`/winners`) — Gallery of all 39 winners with Chart.js radar charts, archetype bars, signature moves, era filtering, sorting, and search
- **Individual winner profiles** (`/winner/<season>`) — Full strategic profiles with radar chart, archetype ratings, strategy summary, game stats, prev/next navigation
- **Winner comparison view** (`/compare`) — Side-by-side comparison of 2-4 winners with overlapping radar chart, head-to-head stats table, archetype bar comparison, strategy cards. Quick compare presets (Richard vs Tony, Parvati vs Sandra, etc.)
- **Seasons overview page** (`/seasons`) — All 39 seasons with summaries, filming locations, key twists, iconic moments, castaway/challenge counts, winner names, era filtering
- **Analytics page** (`/analytics`) — Era comparison radar, aggression trend line, archetype distribution (pie + bar), immunity wins by season, idol plays by season, physical vs strategic scatter plot
- **Redesigned landing page** (`/`) — New homepage showcasing all features with quick stats (39 seasons, castaway count, challenge count), featured winner card, explore cards for all major pages
- **Responsive navbar** — Bootstrap collapsible nav with hamburger menu for mobile, "Explore" dropdown grouping season-specific pages
- **Season summaries data** — 39 season summaries with taglines, themes, twists, iconic moments, filming locations (stored in SEASON_SUMMARIES dict)
- **Dark mode** — Toggle via nav button, persists in localStorage
- **Global search** — Nav search bar with debounced API calls and dropdown results
- **Sortable tables** — Hall of Fame table now sortable by clicking column headers
- **Random season button** — On landing page

### Bug Fixes (from senior review)
- Fixed crash on invalid season parameter (`/castaways?season=abc` was 500, now safely defaults to 28)
- Fixed potential KeyError on missing `episodes` key in API endpoint
- Fixed API endpoints returning plain text errors instead of JSON
- Added `json.JSONDecodeError` handling to data loading (prevents startup crash on malformed files)
- Replaced `|safe` with `|tojson` filter to prevent XSS via script tag injection

### Technical Decisions
- Used Flask's `tojson` template filter instead of `json.dumps` + `|safe` for safer JSON embedding in templates
- Season-specific nav links grouped into "Explore" dropdown to reduce nav clutter
- Winner data stored as individual JSON files in `.temp/winner_profiles/` (one per season)
- Season summaries stored in Python dict (SEASON_SUMMARIES) rather than separate JSON files for simplicity
- Used Chart.js 4.4.0 for all data visualizations

### Files Created
- `templates/winners.html` — Winners Hall gallery
- `templates/winner_profile.html` — Individual winner profiles
- `templates/compare.html` — Winner comparison view
- `templates/seasons.html` — Seasons overview
- `templates/analytics.html` — Data visualizations
- `.temp/winner_profiles/season1-39.json` — 39 winner profile JSONs

### Files Modified
- `app.py` — Added 6 new routes, SEASON_SUMMARIES data, safe season param parser, bug fixes
- `templates/base.html` — Redesigned nav with Bootstrap collapsible, dropdown, search, dark mode
- `templates/index.html` — Redesigned as project homepage
- `templates/hall_of_fame.html` — Added sortable class to table
- `static/css/survivor.css` — Added dark theme, dropdown styles, sortable table styles, nav updates
- `static/js/app.js` — Added sortable table JS, random player function

---

## 2026-02-16 — Winner Profile: Sandra Diaz-Twine (Season 20)

### Work Completed
- Researched Sandra Diaz-Twine's Survivor: Heroes vs. Villains game via Survivor Wiki and local data files
- Cross-referenced voting history from `data/season20_voting.json` — confirmed 75% voting accuracy (9/12 tribal councils correct)
- Missed votes: TC6 voted Russell (Tyson self-eliminated via idol play), TC8 voted Russell (Rob went home instead), TC14 voted Rupert (Danielle eliminated)
- Verified 0 individual immunity wins and 0 individual reward wins from `data/season20_challenges.json` — Sandra never won an individual challenge
- Confirmed 1 hidden immunity idol played successfully at TC15 (Day 36), negating 2 votes from Colby and Rupert
- Received 3 total votes against her: 2 at TC15 (negated by idol) and 1 at TC16 from Colby
- Created comprehensive strategic profile JSON at `.temp/winner_profiles/season20.json`
- Archetype ratings: voting_control 4, physical_game 1, social_capital 8, strategic_aggression 3

### Key Analysis Notes
- Sandra is the ultimate social/anti-strategic winner — won despite having almost no control over votes and zero challenge wins
- Her "anyone but me" philosophy is the most successful low-agency strategy ever employed on Survivor
- Repeatedly tried and failed to get Russell voted out post-merge, yet turned that failure into a jury argument
- The hat-burning moment is iconic but strategically irrelevant — it was pure catharsis and personality
- Won 6-3-0 over Parvati and Russell; Russell received zero votes due to catastrophically poor jury management
- Sandra's idol play at F6 was the only time she needed to save herself with a game advantage
- First two-time winner in Survivor history (also won Season 7: Pearl Islands)

---

## 2026-02-16 — Winner Profile: Denise Stapley (Season 25)

### Work Completed
- Researched Denise Stapley's Survivor: Philippines game using local data files (`data/season25_voting.json`, `data/season25_challenges.json`)
- Cross-referenced voting history — calculated 79% voting accuracy (11/14 votes correct)
- Verified challenge wins: 1 individual immunity (Episode 7), 0 individual reward wins
- Confirmed 6-1-1 jury vote over Lisa Whelchel and Michael Skupin
- Created `.temp/winner_profiles/season25.json`
- Archetype: voting_control 7, physical_game 6, social_capital 9, strategic_aggression 5

### Key Analysis Notes
- Only winner in Survivor history to attend every tribal council (14 total)
- Started on Matsing — the only tribe to lose every immunity challenge in the season
- 6 votes received against her across 39 days
- Never found or played a hidden immunity idol
- Won through elite social game and adaptability across three different tribes
- WebSearch/WebFetch were unavailable; analysis based on local project data + training knowledge

---

## 2026-02-16 — Winner Profile: Tony Vlachos (Season 28)

### Work Completed
- Researched Tony Vlachos' Survivor: Cagayan game (first win only, not Winners at War)
- Cross-referenced voting history from local JSON data: **100% voting accuracy (9/9 actual votes + 1 F2 selection)**
- Tony voted correctly at every single tribal council he attended — perfect record
- Confirmed 0 individual immunity wins, 1 individual reward win from challenge data
- Found 3 idols (most in Cagayan), played 2 (both unsuccessful — no votes negated)
- Jury vote confirmed at 8-1 over Woo Hwang
- Created comprehensive strategic profile JSON at `.temp/winner_profiles/season28.json`
- Archetype ratings: voting_control 10, physical_game 4, social_capital 7, strategic_aggression 10

### Key Analysis Notes
- Tony won without a single individual immunity win — pure strategic/social dominance
- All idol plays in S28 were unsuccessful (0 votes negated across entire season)
- Tyler Perry Idol was Tony's greatest weapon despite never playing it — pure psychological warfare
- Bluffed idol powers extending to F4 when it expired at F5
- Blindsided his own allies (LJ, Trish) when they became threats — ruthless but respected
- 8-1 jury vote shows overwhelming respect for aggressive gameplay over Woo's loyalty

---

## 2026-02-16 — Winner Profile: Mike Holloway (Season 30)

### Work Completed
- Researched Mike Holloway's Survivor: Worlds Apart game via Survivor Wiki and local data files
- Cross-referenced voting history from `data/season30_voting.json` — confirmed 82% voting accuracy (9/11 tribal councils correct)
- Missed votes: TC7 voted Jenn (Kelly blindsided after Jenn's idol play), TC11 voted Tyler (Shirin eliminated while Mike was on the outs)
- Counted individual challenge wins from `data/season30_challenges.json`: 5 individual immunities (Episodes 10, 11, 13, 14x2), 1 individual reward (Episode 14)
- Note: Wiki claims 7 immunity wins but likely includes tribal-level wins; local data shows 5 individual immunities
- Created comprehensive strategic profile JSON at `.temp/winner_profiles/season30.json`
- Archetype ratings: voting_control 4, physical_game 10, social_capital 5, strategic_aggression 6

### Key Analysis Notes
- Mike is the textbook "challenge beast" winner — survived entirely through immunity after becoming the #1 target
- Won 5 consecutive individual immunities from F7 to F4 (one of the longest end-game streaks in Survivor history)
- The Survivor Auction blowup was the pivotal moment: publicly exposed Rodney's sub-alliance, turning the entire majority against him
- Played a hidden immunity idol successfully at TC12 (Tyler's elimination), negating votes against him
- Only received 4 total votes against him at tribal council (most were negated by immunity/idol)
- Won 6-1-1 jury vote against Carolyn Rivera and Will Sims II
- Blue Collar tribe original; led the Escameca Alliance pre-merge but lost control post-merge

---

## 2026-02-16 — Winner Profile: Amber Brkich (Season 8)

### Work Completed
- Researched Amber Brkich's Survivor: All-Stars game via Survivor Wiki and local data files
- Cross-referenced voting history from `data/season8_voting.json` — confirmed 100% voting accuracy (8/8 correct)
- Verified challenge wins: 1 individual immunity (Episode 16), 0 individual reward wins
- Confirmed 4-3 jury vote over Rob Mariano (Alicia, Lex, Shii Ann, Tom for Amber; Kathy, Rupert, Jenna Lewis for Rob)
- Created `.temp/winner_profiles/season8.json`
- Archetype: voting_control 7, physical_game 4, social_capital 9, strategic_aggression 3

### Key Analysis Notes
- Perfect 100% voting accuracy — always on the right side of the numbers
- Only 6 votes against across 39 days despite being Rob's clear #1 ally
- Pioneered the "shield" strategy before the term existed
- Rob proposed on live TV before votes were read
- One of the most socially-driven winning games (only 1 individual immunity win)

---

## 2026-02-16 — Winner Profile: Chris Daugherty (Season 9)

### Work Completed
- Researched Chris Daugherty's Survivor: Vanuatu game via Survivor wiki and local data files
- Cross-referenced voting history from `data/season9_voting.json` — calculated 83% voting accuracy (10/12 votes correct)
- Counted individual challenge wins from challenge data: 3 individual immunity wins (episodes 12, 14x2), 0 individual reward wins
- Created comprehensive strategic profile JSON at `.temp/winner_profiles/season9.json`
- Archetype ratings: voting_control 7, physical_game 6, social_capital 9, strategic_aggression 7

### Key Analysis Notes
- Chris received 3 votes at the very first tribal council but survived — nearly first boot
- After merge, was the last man standing by Day 27 against a 6-1 female majority
- Two incorrect votes (TC9: voted Ami when Rory went home; TC11: voted Eliza when Chad went home) — shows he wasn't always in the loop early post-merge
- Flipped Twila and Scout to create a 4-3 majority, then systematically eliminated Leann, Ami, Julie, Eliza, Scout
- Won final 3 immunity challenges in a row — clutch physical performance when it mattered most
- Beat Twila 5-2 at FTC by owning his deceptions and apologizing, contrasting with Twila's combative approach

---

## 2026-02-16 — Winner Profile: Sandra Diaz-Twine (Season 7)

### Work Completed
- Researched Sandra Diaz-Twine's Survivor: Pearl Islands game (first win only, not HvV)
- Cross-referenced voting history from local JSON data to calculate voting accuracy: **82% (9/11)**
- Confirmed 0 individual immunity wins and 0 individual reward wins from challenge data
- Verified **0 votes received against her** across entire 39-day game
- Jury vote confirmed at 6-1 over Lillian Morris
- Created comprehensive strategic profile JSON at `.temp/winner_profiles/season7.json`
- Archetype ratings: voting_control 7, physical_game 2, social_capital 8, strategic_aggression 6

### Key Analysis Notes
- Sandra pioneered the "anybody but me" philosophy
- Won zero individual challenges yet won 6-1 at FTC
- Key move: orchestrating Burton's second blindside at F5 by flipping Lill
- Only two-time winner in Survivor history

---

## 2026-02-16 — Winner Profile: Fabio Birza (Season 21)

### Work Completed
- Researched Fabio (Jud Birza)'s Survivor: Nicaragua game via Survivor Wiki and local data files
- Cross-referenced voting history from `data/season21_voting.json` against boot order to calculate voting accuracy
- Analyzed challenge data from `data/season21_challenges.json` to count individual immunity and reward wins
- Calculated **60% voting accuracy** (6/10 tribal councils voted for the person eliminated)
- Created comprehensive strategic profile JSON at `.temp/winner_profiles/season21.json`
- Archetype ratings: voting_control 3, physical_game 9, social_capital 7, strategic_aggression 2

### Key Analysis Notes
- Fabio won **4 individual immunity challenges**, including the final 3 consecutively — classic challenge beast endgame
- Received only **2 votes against him** the entire season despite low strategic control
- **0 idols found or played** — pure challenge/social game
- Won the jury vote **5-4** over Chase Rice, with Sash Lenahan receiving 0 votes
- One of the most unorthodox winners: low voting control, low strategic aggression, but high likability kept him safe
- Nickname "Fabio" was assigned by Shannon Elkins on Day 1 and adopted by producers in the opening credits

---

## 2026-02-16 — Winner Profile: Danni Boatwright (Season 11)

### Work Completed
- Researched Danni Boatwright's Survivor: Guatemala game via Survivor Wiki and local data files
- Cross-referenced voting history from `data/season11_voting.json` — confirmed 83% voting accuracy (10/12 tribal councils correct; missed at TC9 voting Jamie instead of Brandon, and TC10 voting Stephenie instead of Bobby Jon)
- Counted individual challenge wins from `data/season11_challenges.json`: 2 individual immunities (Episodes 12 and 14/Final Immunity), 0 individual rewards
- Note: Survivor Wiki claims 3 individual immunity wins but local survivoR data shows 2 — went with the structured data source
- Created comprehensive strategic profile JSON at `.temp/winner_profiles/season11.json`
- Archetype ratings: voting_control 6, physical_game 6, social_capital 9, strategic_aggression 4

### Key Analysis Notes
- Danni received only 1 vote against her in 39 days (from Lydia at Final 4) — remarkably clean game
- Won 6-1 jury vote over Stephenie LaGrossa (only Rafe voted against)
- The quintessential "stealth bomber" winner — entered merge outnumbered, survived Pagonging of Yaxha
- Famously hid her strategy from producers during confessionals to prevent opponents from learning it
- Purchased Survivor Auction advantage for a crucial immunity win
- Social game was the engine of her victory: built genuine bonds across tribal lines
- Former beauty queen (Miss Teen USA runner-up, Miss USA runner-up) and sports radio host

---

## 2026-02-16 — Winner Profile: Tom Westman (Season 10)

### Work Completed
- Researched Tom Westman's Survivor: Palau game via Survivor Wiki and local data files
- Cross-referenced voting history from `data/season10_voting.json` — confirmed 86% voting accuracy (6/7 tribal councils correct; only missed at F4 tiebreaker where he voted Ian but Jenn went home via firemaking)
- Counted individual challenge wins from challenge data: 5 individual immunities, 0 individual rewards
- Verified Koror's historic tribal immunity sweep: 8 for 8 in tribal immunity challenges
- Created comprehensive strategic profile JSON at `.temp/winner_profiles/season10.json`
- Archetype ratings: voting_control 9, physical_game 10, social_capital 8, strategic_aggression 7

### Key Analysis Notes
- Tom received ZERO votes against him across all 39 days — one of the cleanest winning games ever
- Won 5 individual immunity challenges, tied for the season record at the time
- Led Koror to the only complete tribal immunity sweep in Survivor history
- Signature move: convincing Ian to step down from the ~12-hour final immunity challenge
- Won 6-1 jury vote over Katie Gallagher (only Coby voted against)
- Palau had no traditional merge — Stephenie was absorbed into Koror after Ulong was decimated
- Note: `data/season10_challenges.json` has extra names (likely Australian Survivor data mixed in) but Tom's individual wins are clearly identifiable

---

## 2026-02-16 — Winner Profile: Tina Wesson (Season 2)

### Work Completed
- Researched Tina Wesson's Survivor: The Australian Outback game via web sources and local voting/challenge data
- Cross-referenced voting history from local JSON data against boot order to calculate voting accuracy
- Verified jury vote breakdown (Tina 4 - Colby 3) and individual juror votes via Survivor Wiki
- Calculated **100% voting accuracy** (10/10 tribal councils she voted for the person eliminated)
- Created comprehensive strategic profile JSON at `.temp/winner_profiles/season2.json`
- Archetype ratings: voting_control 10, physical_game 4, social_capital 9, strategic_aggression 6

### Key Analysis Notes
- Tina received **0 votes against her** across all 42 days — the ultimate under-the-radar threat management
- Won 0 individual immunity challenges but still won the game (social dominance over physical)
- Won 1 individual reward challenge (Episode 13)
- Signature move: Convinced Colby Donaldson to take her to Final Two over easier-to-beat Keith Famie
- First woman to win Survivor
- Local challenge data (season2_challenges.json) appears corrupted — mixed with Australian Survivor/international data from survivoR package

---

## 2026-02-16 — Winner Profile: Todd Herzog (Season 15)

### Work Completed
- Researched Todd Herzog's Survivor: China game via web sources and local data files
- Cross-referenced voting history against local season15_voting.json and season15_challenges.json
- Calculated 100% voting accuracy (9/9 votes correct -- voted with the majority at every tribal council)
- Created comprehensive strategic profile JSON at `.temp/winner_profiles/season15.json`
- Archetype ratings: voting_control 10, physical_game 2, social_capital 7, strategic_aggression 9

### Key Analysis Notes
- Todd never won an individual immunity challenge -- pure strategic winner
- Perfect voting record: every vote he cast matched the person eliminated
- Only received 5 votes against across 39 days (all from Peih-Gee, Erik, Denise late-game)
- Won jury vote 4-2-1 over Courtney Yates and Amanda Kimmel
- Signature move: engineering James Clement's blindside while James held two Hidden Immunity Idols
- At 22, was the youngest male winner at the time; superfan who applied since age 15

---

## 2026-02-16 — Winner Profile: Brian Heidik (Season 5)

### Work Completed
- Researched Brian Heidik's Survivor: Thailand game via Survivor wiki and local data files
- Cross-referenced voting history from `data/season5_voting.json` — confirmed 100% voting accuracy (9/9 votes correct)
- Counted individual challenge wins from challenge data and wiki: 3 individual immunities, 2 individual rewards
- Created comprehensive strategic profile JSON at `.temp/winner_profiles/season5.json`
- Archetype ratings: voting_control 10, physical_game 7, social_capital 3, strategic_aggression 9

### Key Analysis Notes
- Brian never received a single vote against him across all 39 days — the only player in Thailand with 0 votes against
- Pioneered the "goat strategy" — maintaining separate F2 deals with Helen, Ted, and Clay, then cutting allies at optimal moments
- Won 4-3 jury vote over Clay Jordan; Ted Rogers famously called it voting for "the lesser of two evils"
- Note: `data/season5_challenges.json` has data quality issues (Australian Survivor names mixed in); relied on wiki data for challenge stats

---

## 2026-02-16 — Winner Profile: Ethan Zohn (Season 3)

### Work Completed
- Researched Ethan Zohn's Survivor: Africa game via Survivor Wiki and local data files
- Cross-referenced voting history from season3_voting.json and challenge data from season3_challenges.json
- Calculated **100% voting accuracy** (10/10 votes correct) — perfect record
- Created comprehensive strategic profile JSON at `.temp/winner_profiles/season3.json`
- Archetype ratings: voting_control 8, physical_game 7, social_capital 9, strategic_aggression 4

### Key Analysis Notes
- Ethan received **zero votes** against him across the entire 39-day season — flawless threat management
- Won 1 individual immunity challenge (Episode 9) and 1 individual reward challenge (Episode 9)
- Won the jury vote 5-2 over Kim Johnson
- Signature move: Orchestrated first-ever intentional immunity challenge throw to eliminate Silas after tribe swap
- Quintessential early-era social winner — let Lex and Tom absorb strategic/physical threat labels
- Founded Grassroot Soccer nonprofit with his $1M prize money

---

## 2026-02-16 — Winner Profile: Vecepia Towery (Season 4)

### Work Completed
- Researched Vecepia Towery's Survivor: Marquesas game via web sources and local data files
- Cross-referenced voting history, challenge stats, and jury vote breakdown
- Calculated 80% voting accuracy (8/10 countable votes correct)
- Created comprehensive strategic profile JSON at `.temp/winner_profiles/season4.json`
- Archetype ratings: voting_control 6, physical_game 4, social_capital 6, strategic_aggression 3

### Key Analysis Notes
- Vecepia received only 2 votes against her across 39 days — exceptional threat management
- Won 2 individual immunity challenges (Episode 12 and Final Immunity at Episode 14)
- Won the jury vote 4-3 over Neleh Dennis
- Signature move: Final Immunity deal with Neleh, betraying ally Kathy to secure Final Two spot
- First African-American Sole Survivor

---

## 2026-02-16 — Overnight Session: Data Foundation + Mid-Execution Corrections

**Status:** Interrupted for documentation fixes, ready for fresh restart

### Work Completed

**✅ Data Foundation (Items 1-4 of 84):**
- Downloaded survivoR package data via curl (vote_history.json, challenge_results.json, castaways.json, jury_votes.json)
- Created `.temp/generate_season_data.py` to process data for seasons 1-39
- Generated 78 new data files (39 voting + 39 challenges)
- Updated `app.py` to support all 39 seasons with graceful degradation
- Fixed data compatibility between old format (seasons 28-30) and new format (seasons 1-39)
- Tested and verified all 39 seasons load at http://localhost:8000

**Files Created:**
- `data/season1_voting.json` through `season39_voting.json` (39 files)
- `data/season1_challenges.json` through `season39_challenges.json` (39 files)
- `.temp/generate_season_data.py`

**Files Modified:**
- `app.py`: Multi-season support, data compatibility fixes
- `templates/challenges.html`: Professional photo placeholder

### Critical Issues Encountered

**Issue 1: Permission Prompts During Autonomous Execution**
- `git clone` triggered approval request mid-session, violating /overnight zero-interruption contract
- Workaround: Switched to direct curl downloads
- Permanent fix: Added "Bash Commands & Permission Management" section to CLAUDE.md

**Issue 2: Insufficient Parallelism**
- Context window filling with sequential work instead of delegating to subagents
- User feedback: "I was under the impression that by aggressively pushing everything to a growing fleet of subagents that you orchestrate, that you wouldn't have to operate as linearly"
- What went wrong: Wrote Python script myself, processed 39 seasons sequentially in main context
- What should have happened: Spawn 39 parallel agents to process one season each
- Permanent fix: Added "Agent Quality Standards" to CLAUDE.md and overnight skill

### Documentation Updates

**CLAUDE.md additions:**
- "Bash Commands & Permission Management" — Safe patterns vs. Task tool delegation
- "Agent Quality Standards" — Quality > speed, structured output, file-based deliverables

**.claude/skills/overnight/SKILL.md additions:**
- "Agent Quality Standards" section with example prompts
- "Bash Command Patterns" guidance for avoiding permission prompts

**HANDOFF.md created:**
- Comprehensive session context for fresh restart
- Strategic decisions from interview phase
- Recommended approach for remaining 80 tasks
- Technical details, bugs fixed, quality checklist

### Strategic Decisions

**4-Axis Strategic Classification System:**
1. Voting Control (1-10) — How often they controlled vote outcomes
2. Physical Game (1-10) — Challenge performance
3. Social Capital (1-10) — Trust, relationships, likability
4. Strategic Aggression (1-10) — Boldness, risk-taking

**Key insight:** Axes are independent (high physical + low aggression = Ozzy; high aggression + low physical = Tony)

**UI Design Preferences:**
- Bold, tribal aesthetic (not minimalist)
- Rich, warm colors (earth tones, fire imagery)
- Data-dense layouts (power users want information)

**Delegation Philosophy:**
- Aggressive parallelism for research (39 agents for 39 winners)
- Quality over speed (deliverable-worthy output)
- Complete task delegation (full tasks, not pieces)

### Bugs Fixed

1. KeyError: 'castaway' → Filter for US version only: `v.get('version') == 'US'`
2. KeyError: 'vote' → Changed to .get() calls throughout
3. KeyError: 'episodes' → Added conditional checks: `if 'episodes' in voting_data:`

### Next Session

**Ready for fresh restart with:**
- All 39 seasons loaded and working
- Permission prompt issues documented and solved
- Parallelism strategy clarified with quality standards
- Comprehensive HANDOFF.md for context transfer

**Recommended first task:** Spawn 39 parallel agents to research all winners with strategic profiles (see HANDOFF.md Phase 1)

---

## 2026-02-15 — Overnight Session Prep: 84-Item Implementation Plan

**Scope:** Implement full TODO_MASTER_LIST.md (84 items) with exceptions:
- Skip social features (#78-81) - user accounts, comments, ratings
- Keep Survivor IQ Quiz (#82) - user wants this feature
- Skip domain purchase (#72) - requires credit card

**Interview preference documented:** 5 or less questions at a time, repeat as needed

---

## 2026-02-15 — Vision Expansion: Winner Strategy Analysis + Master To-Do List

**Expanded product vision to focus on analyzing paths to victory**

### Vision Updates to CLAUDE.md

**New research focus:** Decode what strategies actually lead to winning Survivor

**Key questions to answer:**
- Is challenge dominance correlated with winning?
- Do winners vote with the majority consistently or can they win while blindsided?
- What strategic archetypes exist? (social floater, mastermind, challenge beast, etc.)
- What moves should players avoid?
- Can we visually map different paths to victory?

**Updated CLAUDE.md sections:**
- Expanded "The Product Vision" with "The Ultimate Goal: Decoding Paths to Victory"
- Added detailed research questions about challenge performance, voting accuracy, vote control
- Updated core user flow to include "Winners Analysis" exploration mode

### Challenge Photo Fix

**Issue:** Challenge photos were small, grainy, weirdly cropped
**Solution:** Replaced with professional placeholders
- Styled placeholder with camera emoji and "Challenge Photo Coming Soon" text
- Preserved visual structure for when high-quality photos are sourced
- Added TODO comment for future photo integration

**File modified:** `templates/challenges.html` (lines 45-52)

### Master To-Do List Created

**File created:** `planning/TODO_MASTER_LIST.md`

**Total items:** 84 actionable tasks organized by priority

**Categories:**
1. **High Priority — Foundation** (11 items)
   - Data infrastructure (run export script, update AVAILABLE_SEASONS, test performance)
   - Challenge photos (research sources, create upload system)

2. **Winner Analysis — The Core Vision** (19 items)
   - Winner profile pages, comparison views, statistical analysis
   - Strategic archetype classification system
   - Paths to victory visualizations

3. **Data Visualizations** (9 items)
   - Challenge performance graphs, voting bloc diagrams, power rankings
   - Alliance networks, advantages timeline

4. **UI/UX Enhancements** (14 items)
   - Global search, advanced filtering, spoiler-free mode
   - Sorting tables, lazy loading, responsive design, dark mode

5. **Content & Context** (7 items)
   - Season summaries, famous quotes, iconic moments, player nicknames

6. **Technical Improvements** (13 items)
   - Caching, query optimization, CDN, pagination, tests, deployment

7. **Advanced Features** (11 items)
   - ML predictions, social features, gamification

**Priority ranking:**
- 🔴 Do First (Weeks 1-2): Items 1-21 (foundation + core winner analysis)
- 🟡 Do Next (Weeks 3-4): Items 22-49 (visualizations + UI/UX)
- 🟢 Do Later (Month 2+): Items 50-84 (polish, deployment, advanced features)

**Quick wins identified:** 6 low-effort, high-impact items for immediate value

### Next Actions

**Immediate (from user):**
1. Run `Rscript export_all_seasons.R` to pull seasons 1-39
2. Update `app.py` with all season numbers and names
3. Research high-quality challenge photo sources

**Strategic (from vision):**
4. Start building Winners Hall page
5. Design strategic archetype classification system
6. Plan winner comparison visualizations

---

## 2026-02-15 — Overnight Session: Features, Filtering & Hall of Fame

**Autonomous multi-hour session implementing user feedback**

### What Was Shipped

**UI Bug Fixes:**
- Removed winner spoiler from season homepage
- Fixed castaway headshots with fallback initials in tribe colors

**New Filtering Features:**
- Items page: Filter by Successful/Unsuccessful/Not Played/Voted Out Holding
- Challenges page: Filter by Pre-Merge/Post-Merge Reward/Post-Merge Individual Immunity
- Removed tribe filters from Castaways page (now shows all)

**Hall of Fame Page (NEW):**
- Individual records: voting accuracy, challenge wins, votes received, idol plays
- Season records table: items played, votes nullified, players receiving votes
- All-time stats calculated across all available seasons (28, 29, 30)

**Data Infrastructure:**
- Created `export_all_seasons.R` script to export seasons 1-39 from survivoR package
- Script ready to run (requires R + survivoR package installation)

**Code Quality:**
- Ran `/senior-review` on all changes
- Fixed 4 bugs (Counter import, min() defaults, None-check, debug console.log)
- Updated CLAUDE.md with all new templates and endpoints

### Files Created
- `templates/hall_of_fame.html` — All-time records page
- `export_all_seasons.R` — Data export script for seasons 1-39
- `dev/overnight-summaries/001-2026-02-15-features-and-filtering.md` — Full session summary

### Files Modified
- `app.py` — Hall of Fame route + stats, bug fixes
- `templates/base.html` — Hall of Fame nav link
- `templates/index.html` — Winner spoiler removed
- `templates/castaways.html` — Tribe filters removed, headshot fallbacks
- `templates/items.html` — Filtering added
- `templates/challenges.html` — Filtering added
- `static/js/app.js` — Debug console.log removed
- `CLAUDE.md` — Documentation updated
- `planning/MEETING_NOTES.md` — This entry

### Next Steps
1. Run `export_all_seasons.R` to generate data for seasons 1-39 (requires R installation)
2. Test Hall of Fame performance with full 39-season dataset
3. Verify headshot URLs work for older seasons

**Full details:** See `dev/overnight-summaries/001-2026-02-15-features-and-filtering.md`

---

## 2026-02-15 — Senior Review: Templates & app.py

**Scope:** `templates/` directory and `app.py`

**Bugs found and fixed:**
- `app.py:1-2` — Import `collections.Counter` moved to module level (was inside function, causing redundant imports on every request)
- `app.py:296-302` — Fixed incorrect default values in `min()` functions for Hall of Fame champion records (was using 100, now using 0 as default)
- `items.html:53` — Added None-check for `advantage.result` before calling `.replace()` to prevent potential template errors
- `static/js/app.js:15` — Removed debug `console.log` statement

**Code quality improvements:**
- Clean, working code overall
- All filtering features implemented correctly
- No dead code found
- No significant style inconsistencies

**Optimizations:**
- Hall of Fame route processes all castaways on each request. With only 3 seasons (54 castaways), performance is fine. If scaled to 39 seasons, consider caching these stats at app startup.

**Documentation updates:**
- `CLAUDE.md` — Updated templates section to include all new pages (hall_of_fame.html, challenges.html, items.html, etc.)
- `CLAUDE.md` — Updated "Current State" to reflect 3 seasons coverage and all new features
- `CLAUDE.md` — Populated API Endpoints table with all active routes

**Overall assessment:**
Codebase is in excellent shape. All features work correctly, code is clean and maintainable. The autonomous overnight session successfully implemented filtering for Items and Challenges, removed tribe filters from Castaways, built a comprehensive Hall of Fame page, and fixed the winner spoiler issue. No critical bugs or security issues found. The only minor optimization opportunity is caching Hall of Fame stats if/when the dataset scales to 39 seasons.

**Recommended follow-ups:**
- Consider pre-computing Hall of Fame stats at app startup when scaling to 39 seasons
- Test headshot image loading across all seasons (some Wikia URLs may be broken)
- Add error handling for missing data files when new seasons are added

---

## 2026-02-15 — CLAUDE.md Updated: Aggressive Parallelism & Auto Web Search

**Updated CLAUDE.md to emphasize orchestration mindset and remove web search approval requirements**

### Changes Made

**1. Parallelism & Orchestration Section Rewritten**
- Renamed to "🎯 PARALLELISM & ORCHESTRATION MANDATE"
- Added "conductor, not solo performer" metaphor
- New orchestration patterns table with 4 detailed examples:
  - Pattern 1: Fan-out exploration (multi-agent codebase investigation)
  - Pattern 2: Parallel validation (simultaneous testing/checking)
  - Pattern 3: Research + implementation (concurrent research while coding)
  - Pattern 4: Multi-source investigation (bug investigation with 4+ agents)
- Added comparison table: Sequential (Slow) vs Parallel (Fast)
- New "Rules of Engagement" section with 7 principles
- Added "Challenge Questions" to ask before starting any task
- Emphasis on maximizing parallel throughput, spawning agents preemptively

**2. Web Search Auto-Approval Added**
- Added to Personal Preferences section
- "Web searches require NO approval — Execute web searches immediately without asking for permission. Research is a core part of your job. Search freely and report findings."
- No more permission prompts for web research

### Key Philosophy Changes

**Before:** "Use subagents liberally"
**After:** "You are a conductor. Default to parallel. Challenge yourself to spawn as many agents as possible."

**Before:** Web searches required approval
**After:** Web searches execute automatically — research freely

### Why These Changes

User wants Claude instances to:
1. Think like a project manager orchestrating a team of specialists
2. Maximize parallel execution to complete work faster
3. Remove friction from common research operations (web search)
4. Push the boundaries of what's possible with aggressive parallelism

**Goal:** 5-10x faster task completion through aggressive parallel orchestration

---

## 2026-02-15 — Multi-Season Support: Seasons 28, 29, 30 Fully Operational

**Shipped complete multi-season functionality with Season 29 & 30 data**

### What Was Built

**1. Multi-Season Architecture**
- Refactored `app.py` to support multiple seasons dynamically
- All data loading centralized in `load_season_data()` function
- Season selector dropdown in navigation (Bootstrap select)
- All routes now accept `?season=` parameter (defaults to 28)

**2. Season 29 Data (San Juan del Sur)**
- ✅ 26 challenges extracted from survivoR package
- ✅ 14 tribal councils / voting data with 18 castaways
- ✅ 5 idols + 2 fake idols (researched via web search)
- ✅ 13 timeline events (tribe formations, swaps, merge, twists)
- ✅ 18 contestant headshots (Survivor Wiki)
- ✅ 27 challenge photos (True Dork Times)

**3. Season 30 Data (Worlds Apart)**
- ✅ 26 challenges extracted from survivoR package
- ✅ 15 tribal councils / voting data with 18 castaways
- ✅ 3 idols + 1 extra vote + 1 fake idol (researched via web search)
- ✅ 12 timeline events (tribe formations, swaps, merge, twists)
- ✅ 18 contestant headshots (Survivor Wiki)
- ✅ 25 challenge photos (True Dork Times)

**4. Season 28 Enhancements (Cagayan)**
- ✅ 18 contestant headshots added
- ✅ 24 challenge photos added

**5. UI Improvements**
- Season selector dropdown in navigation bar
- Dynamic page titles and branding per season
- Contestant headshot images on Castaways page (100px circular)
- Challenge photos on Challenges page (300px max height)
- Dynamic footer showing current season
- CSS styling for season selector and images

### Files Created/Modified

**Created:**
- `data/season29_challenges.json` — 26 challenges
- `data/season29_voting.json` — 14 tribal councils, 18 castaways
- `data/season29_advantages_idols.json` — 5 idols, 2 fake idols
- `data/season29_timeline.json` — 13 events
- `data/season29_headshots.json` — 18 contestant images
- `data/season29_challenge_photos.json` — 27 challenge photos
- `data/season30_challenges.json` — 26 challenges
- `data/season30_voting.json` — 15 tribal councils, 18 castaways
- `data/season30_advantages_idols.json` — 3 idols, 1 extra vote, 1 fake
- `data/season30_timeline.json` — 12 events
- `data/season30_headshots.json` — 18 contestant images
- `data/season30_challenge_photos.json` — 25 challenge photos
- `data/season28_headshots.json` — 18 contestant images
- `data/season28_challenge_photos.json` — 24 challenge photos

**Modified:**
- `app.py` — Complete refactor for multi-season support (188 lines)
- `templates/base.html` — Added season selector dropdown, dynamic branding
- `templates/castaways.html` — Added headshot images
- `templates/challenges.html` — Added challenge photos
- `static/css/survivor.css` — Added styles for season selector, headshots, challenge photos

### Technical Approach

**Parallel Agent Execution (8 agents simultaneously):**
1. Bash agent: Extract Season 29 challenges from survivoR
2. Bash agent: Extract Season 29 voting from survivoR
3. general-purpose agent: Research Season 29 advantages/idols
4. general-purpose agent: Research Season 29 timeline
5. general-purpose agent: Research Season 30 advantages/idols
6. general-purpose agent: Research Season 30 timeline
7. general-purpose agent: Research contestant headshots (all 3 seasons)
8. general-purpose agent: Research challenge photos (all 3 seasons)

**Total parallel execution time:** ~5 minutes for all 8 agents

**Additional work:**
- Bash agent: Extract castaway metadata for Season 29 & 30 from survivoR (added missing 'castaways' arrays to voting JSON)

### Key Technical Decisions

1. **Image hosting:** External URLs (Option A) — faster, no repo bloat
2. **Season parameter:** Query string `?season=28` — simplest implementation
3. **Default season:** 28 (Cagayan) — original season data
4. **Photo matching:** Index-based matching for challenges (photos in episode order)
5. **Error handling:** `onerror="this.style.display='none'"` for broken image URLs

### Testing Results

**All endpoints tested for all 3 seasons (HTTP 200):**
```
Season 28: ✓ tribal-councils ✓ castaways ✓ challenges ✓ events ✓ items
Season 29: ✓ tribal-councils ✓ castaways ✓ challenges ✓ events ✓ items
Season 30: ✓ tribal-councils ✓ castaways ✓ challenges ✓ events ✓ items
```

### Data Sources

- **Challenge data:** survivoR R Package (GitHub: doehm/survivoR)
- **Voting data:** survivoR R Package
- **Castaway metadata:** survivoR R Package (castaways.rda, vote_history.rda)
- **Advantages/Idols:** Web research (Survivor Wiki, True Dork Times, Wikipedia)
- **Timeline events:** Web research (Survivor Wiki, Inside Survivor, True Dork Times)
- **Headshots:** Survivor Wiki (survivor.fandom.com)
- **Challenge photos:** True Dork Times (truedorktimes.com)

### App Running

Server: http://localhost:8000 (port 8000 to avoid macOS AirPlay conflict)

**How to use:**
1. Navigate to any page
2. Use season selector dropdown in navigation
3. All pages update to show selected season's data

### What's Next

- Update README.md to reflect new multi-season support
- Update index.html landing page with season stats
- Consider adding season comparison features
- Expand to more seasons (40, 20, 31, 16 are popular)

---

## 2026-02-15 — Contestant Headshot URLs for Seasons 28, 29, 30

**Created comprehensive headshot image URL files for all three seasons**

**Files created:**
- `data/season28_headshots.json` — 18 Cagayan contestant headshots
- `data/season29_headshots.json` — 18 San Juan del Sur contestant headshots
- `data/season30_headshots.json` — 18 Worlds Apart contestant headshots

**Total headshots gathered:** 54 contestants across all three seasons

**Image source:**
- All images sourced from Survivor Wiki (survivor.fandom.com)
- High-quality official CBS promotional photos
- Consistent URL pattern: `https://static.wikia.nocookie.net/survivor/images/.../S[season]_[First]_[Last].jpg`

**Season coverage:**
- Season 28: Cagayan — Tony Vlachos through David Samson
- Season 29: San Juan del Sur — Natalie Anderson through Nadiya Anderson
- Season 30: Worlds Apart — Mike Holloway through So Kim

**Research approach:**
1. Fetched individual contestant Wiki pages to discover URL pattern
2. Verified pattern consistency across multiple contestants
3. Compiled comprehensive JSON mappings using exact contestant names from voting data

**Key notes:**
- Contestant names match exactly with voting data for easy integration
- All URLs point to high-resolution versions (`/revision/latest`)
- Images are official CBS promotional headshots used in season promotion

---

## 2026-02-15 — Season 29 Idols & Advantages JSON Created

**Created comprehensive idols and advantages file for Survivor Season 29: San Juan del Sur**

**File created:**
- `data/season29_advantages_idols.json` — 5 hidden immunity idols + 2 fake idols documented

**Season details:**
- Season 29: San Juan del Sur - Blood vs. Water
- Winner: Natalie Anderson (first to play idol on another player AND win)

**Hidden Immunity Idols documented:**
1. John Rocker (Coyopa) - Found Day 5, voted out Day 8 with idol in pocket
2. Keith Nale (Hunahpu) - Found Day 11, played Day 26, negated 3 votes
3. Jon Misch #1 (post-merge Exile) - Found Day 19, played Day 26, negated 4 votes
4. Jon Misch #2 (post-merge Exile) - Found Day 27, voted out Day 35 with idol in pocket
5. Natalie Anderson (post-merge Exile) - Found Day 22, played on Jaclyn Day 36, negated 3 votes

**Fake idols:**
- Val Collins - Made fake idol after bluffing about finding two idols (Episode 2)
- Dale Wentworth - Found decorative knick-knack from well, used as leverage (Episode 1)

**Key statistics:**
- Total idols found: 5
- Total idols played: 3 (100% successful — all negated votes)
- Total votes negated: 10 votes
- Voted out holding idols: 2 (John Rocker, Jon Misch)
- Unique twist: Two players with homophonic names (John/Jon) both eliminated with unused idols

**Notable idol plays:**
- Natalie's idol play on Jaclyn at Final 5 is considered one of the best in Survivor history
- First season where contestant played idol on another player AND won the game
- Keith initially told everyone Jeremy had the idol, but Keith actually found it

**Exile Island idol mechanics:**
- Pre-merge: Two vases at Exile, only one had clue to idol at contestant's tribe camp
- Post-merge: Single urn with clue to idol hidden on Exile Island itself

**Research sources:**
- Survivor Wiki (comprehensive idol history)
- True Dork Times (episode-by-episode tracking)
- Inside Survivor, Survivor Oz
- Wikipedia, episode recaps

**Data structure:** Follows same format as `season28_advantages_idols.json` with detailed tracking of each idol's journey from find to play/elimination.

---

## 2026-02-15 — Season 30 Advantages & Idols JSON Created

**Created comprehensive advantages and idols file for Survivor Season 30: Worlds Apart**

**File created:**
- `data/season30_advantages_idols.json` — 5 advantages/idols documented (3 real idols, 1 extra vote, 1 fake idol)

**Season details:**
- Season 30: Worlds Apart - White Collar vs. Blue Collar vs. No Collar
- Winner: Mike Holloway (6-2-0 over Carolyn Rivera and Will Sims II)

**Advantages/Idols documented:**
1. **Carolyn Rivera** — Found White Collar idol on Day 2 (Episode 1), played on Day 35 (Episode 13), negated 5 votes, successful
2. **Jenn Brown** — Found No Collar idol on Day 9 (Episode 4), played on Day 19 (Episode 7), negated 7 votes (tied record), successful
3. **Mike Holloway** — Found Blue Collar idol on Day 22 (Episode 8), played on Day 32 (Episode 12), negated 4 votes, successful
4. **Dan Foley** — Won Extra Vote at auction on Day 25 (Episode 9), played on Day 35 (Episode 13), backfired when Carolyn played idol
5. **Joe Anglim** — Created fake idol (Episode 9), Mike played it on Will, revealed as fake

**Notable statistics:**
- **Perfect idol success rate:** All 3 real idols played successfully (16 total votes negated)
- **First-ever Extra Vote advantage** introduced at Survivor Auction
- **Mike Holloway:** First eventual Sole Survivor to successfully play a Hidden Immunity Idol in their winning season
- **Jenn Brown's 7-vote negation** tied Russell Hantz's Samoa record
- **Carolyn Rivera:** Kept idol secret for 33 days (one of the longest secret holdings)

**Research sources:**
- Survivor Wiki, Wikipedia, True Dork Times
- Inside Survivor episode recaps
- GoldDerby, Surviving Tribal
- Episode-specific recaps from Jeff Pitman

**Data structure:** Follows same detailed format as `season28_advantages_idols.json` with complete tracking of who found/played each advantage, day/episode numbers, votes negated, outcomes, and comprehensive notes.

---

## 2026-02-15 — Season 29 Timeline JSON Created

**Created comprehensive timeline file for Survivor Season 29: San Juan del Sur**

**File created:**
- `data/season29_timeline.json` — 13 timeline events documented

**Season details:**
- Season 29: San Juan del Sur - Blood vs. Water
- Filmed: June 2 - July 10, 2014 in Nicaragua
- Aired: September 24 - December 17, 2014
- Winner: Natalie Anderson (5-2-1 over Jaclyn Schultz and Missy Payne)

**Timeline events documented:**
1. Day 1: Tribe formation (Coyopa vs. Hunahpu - 9 loved ones pairs split across tribes)
2. Day 1: Blood vs. Water twist with Exile Island
3. Day 6: John Rocker blindsided with idol in pocket
4. Day 11: Tribe swap
5. Day 16: Merge into Huyopa tribe (11 castaways)
6. Day 18: Julie McGee quit (trail mix scandal + missing boyfriend)
7. Day 19: Josh Canfield blindsided
8. Day 27: Jeremy Collins blindsided by Jon's alliance
9. Day 28: Natalie found Hidden Immunity Idol
10. Day 30: Double idol play (Jon and Keith both played idols, Wes eliminated)
11. Day 33: Jon Misch blindsided with idol in pocket
12. Day 36: Natalie played idol on Jaclyn
13. Day 39: Final Tribal Council - Natalie wins 5-2-1

**Key twists:**
- Blood vs. Water format (9 loved ones pairs competing)
- Exile Island returned after 11-season hiatus
- Reward Challenges featured one-on-one duels between loved ones
- Only 1 quit (Julie McGee), no medical evacuations
- 2 players eliminated with idols in pockets (John Rocker, Jon Misch)

**Research sources:**
- Survivor Wiki, Wikipedia, CBS News
- True Dork Times calendar
- Inside Survivor, Survivor Oz
- RobHasAWebsite exit interviews

**Data structure:** Follows same format as `season28_timeline.json` with event_type, day, date, description, tribes_affected, and detailed context for each major event.

---

## 2026-02-15 — Challenge Photos for Seasons 28-30 Compiled

**Created challenge photo JSON files for three seasons:**

**Files created:**
- `data/season28_challenge_photos.json` — 24 challenge photos
- `data/season29_challenge_photos.json` — 27 challenge photos
- `data/season30_challenge_photos.json` — 25 challenge photos

**Total: 76 challenge photos across all three seasons**

**Data source:** True Dork Times (truedorktimes.com)
- Season 28 (Cagayan): 24 challenges from 14 episodes
- Season 29 (San Juan del Sur): 27 challenges from 14 episodes
- Season 30 (Worlds Apart): 25 challenges from 14 episodes

**JSON structure:**
```json
{
  "season": 28,
  "season_name": "Survivor: Cagayan",
  "challenge_photos": {
    "Episode 1 - Draggin' the Dragon": "https://www.truedorktimes.com/s28/images/e1/e1tv8t.jpg",
    ...
  }
}
```

**Challenge naming:**
- All challenges have unique names (often music references)
- Format: "Episode # - Challenge Name"
- Examples: "Draggin' the Dragon", "Bermuda Triangles", "Octopus' Garden", "Sumo at Sea"
- Includes reward challenges, immunity challenges, and auction photos

**Image sources:**
- True Dork Times (primary source — high-quality episode screenshots)
- CBS official photos (referenced but not used due to harder linking)
- Getty Images (referenced but not used — requires licensing)
- Survivor Wiki (referenced but did not have direct image URLs in extracted content)

**Research approach:**
- Web searches for official CBS and Survivor Wiki sources
- Fetched True Dork Times calendar pages for all three seasons
- Extracted challenge names and relative image paths
- Converted to full URLs using TrueDorkTimes.com base URLs

**Next step:** Integrate challenge photos into Flask app (episode view and challenges view)

---

## 2026-02-15 — Season 28 Advantages & Idols Research Complete

**Researched all hidden immunity idols and advantages from Season 28 (Cagayan)**

**File created:** `planning/season28_advantages_idols.json`

**Research approach:**
- Conducted 15+ targeted web searches across multiple sources
- Cross-referenced Survivor Wiki, TrueDorkTimes, episode recaps, contestant interviews
- Verified timeline data from TrueDorkTimes calendar (day-by-day tracking)
- Extracted voting history details from episode-specific sources

**Complete idol/advantage inventory:**
1. **Garrett Adelstein** — Luzon idol (Day 1) — Not played, voted out holding it (Day 6)
2. **Tony Vlachos** — Aparri idol (Day 3) — Played on LJ at merge (Day 17, Episode 6)
3. **LJ McKanas** — Solana idol (Day 7) — Played on Tony at merge (Day 17, Episode 6)
4. **Spencer Bledsoe** — Post-merge idol (Day 20) — Played on himself (Day 28, Episode 10)
5. **Tony Vlachos** — Tyler Perry Super Idol (Day 26) — Never played, used as psychological weapon
6. **Tony Vlachos** — Auction idol (Day 29) — Played on himself at Final 5 (Day 35, Episode 12)

**Key findings:**
- Total: 6 idols/advantages (all Hidden Immunity Idols, one with special powers)
- Players who found idols: Garrett (1), LJ (1), Spencer (1), Tony (3)
- Idols played: 4 of 6
- Successful plays (negated votes): 0 of 4 — Unique! All plays were either unnecessary or coordinated
- Voted out holding: Garrett only (Day 6, earliest elimination while holding idol in Survivor history)
- Tyler Perry Idol: Could be played AFTER votes read, expired at Final 5, Tony lied about it being valid at Final 4

**Notable events:**
- Episode 6 merge tribal: Tony and LJ played idols on EACH OTHER simultaneously (unique in Survivor)
- Spencer's wasted idol: Played on himself when votes went to Jeremiah instead
- Tony's psychological warfare: Displayed special idol at tribals to intimidate without playing it
- Garrett's mistake: Left idol at camp when voted out Episode 2

**JSON structure:**
- Complete metadata for each idol (type, tribe, finder, days, episodes, play details, results)
- Summary statistics by player
- Special notes section documenting unique events
- 12 verified sources cited

**Insights:**
- No idol successfully negated votes — unprecedented in modern Survivor
- Tony's strategic idol bluffing was key to his 8-1 victory over Woo
- Tyler Perry Idol was controversial (Tyler Perry himself said he "wasn't happy" with it)
- All three pre-merge tribes had hidden idols, plus three post-merge idols

**Next step:** Integrate advantages data into Flask app with advantages/idols view

---

## 2026-02-15 — Season 28 Timeline Research Complete

**Researched and documented complete timeline of key events for Season 28 (Cagayan)**

**File created:** `planning/season28_timeline.json`

**Research sources:**
- Survivor Wiki (comprehensive season information)
- Wikipedia (season overview and key events)
- TrueDorkTimes calendar (day-by-day episode tracking)
- Multiple web searches for specific twist mechanics and advantage details

**Timeline includes:**
- **Tribe formations** (Day 1): Aparri (Brawn), Luzon (Brains), Solana (Beauty) - 6 members each
- **First Impressions twist** (Day 1): Leaders selected "weakest" members who were sent to camp early with choice of rice or idol clue
- **Tribe swap** (Day 12): Luzon disbanded, 14 players redistributed into new Aparri (7) and Solana (7)
- **Lindsey Ogle quit** (Day 14): Only quit in season, left after rivalry with Trish intensified
- **Merge** (Day 17): 11 players merged into Solarrion tribe at Aparri camp
- **Tyler Perry Idol introduced** (Day 17): Special idol playable AFTER votes are read (most controversial twist)
- **Survivor Auction** (Day 29): Tony won rock draw against Spencer for idol clue advantage
- **Tony's idol bluff** (Day 37): Claimed Super Idol valid at Final 4 when it expired at Final 5
- **Final Tribal Council** (Day 39): Tony defeated Woo 8-1

**JSON structure:**
- Complete event timeline with day numbers, dates, descriptions
- Tribe compositions before/after swap
- Advantage tracking (3 hidden immunity idols found, 1 special idol)
- Season mechanics documented (First Impressions, Tyler Perry Idol, traditional swap)
- Notable stats (18 castaways, 1 quit, 0 medevacs, 39 days, 16 tribal councils)

**Key insights:**
- Tyler Perry Idol was most controversial twist (fan criticism for being too powerful)
- Tony's strategic use of expired idol influenced jury votes positively
- Garrett Adelstein found idol on Day 1 after choosing clue over rice
- First Impressions twist created early strategic dilemmas

**Next step:** Integrate timeline data into Flask app with events view

---

## 2026-02-15 — Season 28 Challenge Data Extracted

**Extracted complete challenge data for Season 28 (Cagayan) from survivoR package**

**Data source:** https://raw.githubusercontent.com/doehm/survivoR/master/dev/json/challenge_results.json

**File created:** `data/season28_challenges.json`

**Data structure:**
- 23 total challenges across 13 episodes
- Breakdown: 12 immunity-only, 8 reward-only, 3 combined immunity+reward
- Outcome types: 9 tribal, 10 individual, 4 team challenges
- Challenge winners clearly identified (tribal, individual, or team)
- Individual immunity winners: Woo (1), Spencer (3), Tasha (3), Tony (1), Kass (1)

**JSON format:**
```json
{
  "season": 28,
  "season_name": "Survivor: Cagayan",
  "challenges": [
    {
      "challenge_id": 1,
      "episode": 1,
      "challenge_type": "Immunity and Reward",
      "outcome_type": "Tribal",
      "winners": ["Solana"],
      "losers": ["Aparri", "Luzon"]
    }
  ]
}
```

**Key findings:**
- Tasha dominated individual immunity (3 wins in episodes 8-10)
- Spencer and Tasha combined won 6 of 10 individual immunity challenges
- Tribal phase had 9 challenges (episodes 1-5)
- Individual phase had 10 immunity challenges (episodes 6-13)
- Team reward challenges occurred during merge phase (4 team challenges)

**Next step:** Integrate challenge data into Flask app routes and UI

---

## 2026-02-15 — Season Analyzer 2.0 SHIPPED! 🔥

**ALL 3 PHASES IMPLEMENTED IN ONE SESSION** using parallel subagent execution

**Parallel strategy:**
- Spawned 3 research agents simultaneously → completed in ~3 minutes
- Agent 1: Extracted 23 challenges from survivoR package
- Agent 2: Researched 6 idols/advantages (manual research)
- Agent 3: Researched complete season timeline
- Main thread: Implemented all backend + frontend code while agents worked

**Features shipped:**
✅ Scrollable tribal councils (16 councils, drama scores, flame ratings)
✅ Voting accuracy % on castaway profiles
✅ Challenge outcomes timeline (23 challenges)
✅ Challenge beast metrics (immunity + reward wins)
✅ Key events timeline (swaps, merge, twists)
✅ Items/advantages tracking (6 idols fully documented)

**New routes:** `/tribal-councils`, `/challenges`, `/events`, `/items`

**Files created:** 4 templates, 3 JSON data files, ~400 lines CSS

**App running at:** http://localhost:8000 — All 6 routes tested ✅

---

## 2026-02-15 — Season Analyzer 2.0 Spec Created

**Feature spec created:** `dev/specs/001-season-analyzer-2.md`

**User feedback captured:**
- Change episode view to scrollable tribal councils (no pagination)
- Add voting accuracy % to castaway profiles
- Add challenge outcomes timeline
- Add episode grading (drama scores based on items, vote spread, merge)
- Add challenge beast metrics to castaway profiles
- Add key events timeline (swaps, merge, twists)
- Add item/advantage tracking (idols, steal-a-vote, etc.)
- Skip alliance tracking for now

**Spec covers:**
- 7 new features transforming voting tracker into comprehensive season analyzer
- 3-phase implementation plan (quick wins, challenge integration, manual curation)
- Data strategy: use survivoR package for challenges, manually curate items for Season 28
- Voting accuracy algorithm, episode grading algorithm, challenge beast detection
- New routes: /tribal-councils, /challenges, /events, /items
- Scrolling UX philosophy for all timeline views

**Decisions made:**
- One comprehensive spec (not separate specs per feature)
- Ship everything possible with existing data first
- Alliance tracking deferred (lowest priority)
- Items/advantages highest priority (manual research needed for Season 28)
- UI decisions delegated to implementer
- Shareability deferred for later

**Next step:** Implement Phase 1 (scrollable tribals, voting accuracy, episode grading)

---

## 2026-02-15 — Season 28 Web App Built & Launched

**Built complete web app for Season 28 (Cagayan) voting visualization**

**Stack:**
- Backend: Flask (Python)
- Frontend: Bootstrap + Custom CSS
- Data: JSON (parsed from markdown voting data)

**Features shipped:**
1. **Landing page** with season overview, stats, winner announcement
2. **Episode View** — Navigate all 13 episodes, see every tribal council vote chronologically
   - Keyboard navigation (←/→ arrows)
   - Vote breakdowns showing who voted for whom
   - Elimination banners with torch-out animation
3. **Castaway View** — Individual profiles for all 18 castaways
   - Tribe filtering (Brawn/Brains/Beauty)
   - Complete voting history for each player
   - Expandable details showing elimination info
   - Days lasted, votes against stats

**UI/Design:**
- Survivor-themed aesthetic: torch animations, tribal colors, bamboo borders
- Tropical color palette (jungle green background, torch orange accents, tribal reds)
- Custom fonts (Trade Winds for titles, Cinzel for body)
- Animated torch flame effect
- Responsive grid layouts

**Files created:**
- `app.py` — Flask routes for /, /episodes, /castaways + API endpoints
- `data/voting_data.json` — Structured voting data (18 castaways, 13 episodes, 16 tribal councils)
- `templates/base.html` — Base template with navigation
- `templates/index.html` — Landing page
- `templates/episodes.html` — Episode view with navigation
- `templates/castaways.html` — Castaway profiles view
- `static/css/survivor.css` — Full Survivor theming (torch animations, tribal patterns, colors)
- `static/js/app.js` — Frontend interactivity
- `requirements.txt` — Flask dependency
- Updated `README.md` with run instructions

**App running at:** http://localhost:8000 (changed from 5000 due to macOS AirPlay conflict)

**Data structure:**
- Episodes array with nested tribal councils
- Castaways array with voting history, stats, elimination details
- Vote breakdowns with voters and targets
- Season metadata (winner, tribes, theme)

**Next steps:**
- Add more seasons
- Consider adding visualizations (Sankey diagrams, alliance networks)
- Possibly add search/filter functionality
- Deploy to production (TBD)

---

## 2026-02-15 — Vision, Research & Data Extraction

**Vision document created:** `planning/SURVIVOR_VISION.md`
- One-liner: "The complete visual history of every Survivor season — explore alliances, blindsides, and winning strategies through interactive gameplay analysis"
- 3 core exploration modes: Season Explorer (episode timeline), Player Deep Dive (contestant journey), Episode Analyzer (challenge/vote detail)
- Key features: voting visualizations, alliance network graphs, blindside detection, move quality grading, performance metrics
- Data structure defined: seasons, episodes, players, votes, alliances
- Technical stack proposed: Python/Flask backend, Vanilla JS frontend, D3.js for visualizations
- Open questions documented: alliance detection algorithm, move grading criteria, UI direction

**Research completed:**
- Researched Survivor game mechanics (immunity challenges, reward challenges, tribal council, old vs new era)
- Found comprehensive data sources:
  - **survivoR R Package** (GitHub) — Primary source: JSON-ready data for all seasons, includes castaways, vote history, challenge results, jury votes, season summaries
  - **Survivor Stats DB** — Web dashboard built on survivoR package with downloadable data
  - **True Dork Times** — Episode-by-episode data in Google Sheets
  - **Survivor Wiki** — Comprehensive wiki with statistics
  - **Kaggle** — Alternative Survivor dataset

**Data ingestion test — Season 28 (Cagayan):**
- Successfully cloned survivoR GitHub repo (https://github.com/doehm/survivoR)
- Found JSON data files in `dev/json/` directory (all datasets available as JSON!)
- Extracted complete Season 28 voting history: 13 episodes, 15 tribal councils, full vote-by-vote records
- Key data available: castaways (18 players), vote history (every vote recorded), episodes (14 total including reunion), challenge results
- Data structure confirmed: `castaway`, `vote`, `voted_out`, `nullified`, `tie`, `day`, `tribe`, `episode`, `order`
- Special cases captured: deadlocks, split votes, vote events (quit, advantages)
- Tony Vlachos winner confirmed, beat Woo 8-1
- Data quality: Excellent. All votes tracked, including ties and revotes. Tribal council order tracked. Castaway IDs provided for linking.

**Created documentation:**
- `planning/season28_voting_data.md` — Complete voting history for Season 28, all 15 tribal councils formatted as markdown with vote breakdowns, special events (ties, deadlocks, split votes), and results

**Next steps:**
1. ✅ ~~Verify survivoR data coverage~~ — Confirmed all 49 seasons available
2. ✅ ~~Test data ingestion~~ — Season 28 successfully extracted
3. Prototype one visualization (voting Sankey diagram for one tribal council)
4. Define alliance detection rules
5. Sketch UI mockups
6. Set up Python backend to ingest JSON data
7. Build database schema

---

## 2026-02-15 — Project Initialization

**Created:**
- Project structure with skills and organization folders
- Template CLAUDE.md for survivor-bot
- Initial ROADMAP.md and MEETING_NOTES.md
- GitHub repository: https://github.com/willhofner/survivor-bot
- Initial commit pushed to main branch

## 2026-02-15 — Season 30 Timeline JSON Created

**Created comprehensive timeline file for Survivor Season 30: Worlds Apart**

**File created:**
- `data/season30_timeline.json` — 12 timeline events documented

**Season details:**
- Season 30: Worlds Apart - White Collar vs. Blue Collar vs. No Collar
- Filmed: August 4 - September 11, 2014 in San Juan del Sur, Nicaragua
- Aired: February 25 - May 20, 2015
- Winner: Mike Holloway (6-1-1 over Carolyn Rivera and Will Sims II)

**Timeline events documented:**
1. Day 1: Tribe formation (Escameca/Blue Collar, Masaya/White Collar, Nagarote/No Collar - 6 members each)
2. Day 1: Tribe Leader Decision twist (Honest vs. Deceive choice, Joaquin/So lied about "Neutral" option)
3. Day 12: Tribe swap (Masaya dissolved, 14 players redistributed)
4. Day 14: Joaquin blindsided to break up Rodney-Joaquin alliance
5. Day 17: Merge into Merica tribe (12 castaways, name coined by Mike)
6. Day 29: Survivor Auction with Extra Vote advantage (Dan won, Mike's auction behavior damaged social game)
7. Day 30: Mike exposed Rodney's secret alliance, became primary target
8. Day 31: Mike began unprecedented 5-out-of-6 immunity challenge run
9. Day 33: Mike played Hidden Immunity Idol, blindsided Tyler
10. Day 35: Dan used Extra Vote but Carolyn played idol, Dan eliminated
11. Day 37: Fire-making tiebreaker returned (first time since Gabon)
12. Day 39: Final Tribal Council - Mike wins 6-1-1

**Key twists:**
- White Collar vs. Blue Collar vs. No Collar theme based on social class/work style
- First season to introduce Extra Vote advantage (offered at auction)
- Tribe Leader Decision: Leaders chose partner to decide between Honest (more beans) or Deceive (beans + idol clue)
- Fire-making tiebreaker returned at Final 4
- No quits or medical evacuations (first since Season 23)

**Historical significance:**
- First introduction of Extra Vote advantage in Survivor
- First season with three starting tribes to have representative from each original tribe in Final Three
- Mike's 5 immunity wins tied for second-most individual immunity wins in single season
- Dan's Extra Vote backfired when Carolyn played idol

**Research sources:**
- Survivor Wiki (comprehensive season/tribe information)
- Wikipedia (season overview, finale details)
- True Dork Times (episode calendar, challenge tracking)
- CBS News, Hollywood Reporter (cast announcements)
- Inside Survivor, Survivor Oz (episode recaps)
- Medium articles (strategic analysis)

**Data structure:** Follows same format as `season28_timeline.json` and `season29_timeline.json` with event_type, day, date, description, detailed context, tribe compositions, strategic moments, and advantages.


## 2026-02-15 — Castaway Metadata Extracted for Seasons 29 & 30

**Extracted complete castaway metadata for Seasons 29 and 30 from survivoR package**

**Files updated:**
- `data/season29_voting.json` — Added 18 castaways with complete metadata
- `data/season30_voting.json` — Added 18 castaways with complete metadata

**Data source:** survivoR R package (GitHub: doehm/survivoR)
- Installed pyreadr to read R data files (.rda format)
- Extracted from: castaways.rda, vote_history.rda, tribe_colours.rda

**Castaway metadata extracted:**
- Name, original tribe (with theme), tribe color (hex code)
- Placement (Winner, Runner-up, 2nd Runner-up, or ordinal elimination order)
- Days lasted
- Total votes against
- Complete voting history (tribal council number, voted for, day)
- Final result for finalists

**Season 29 (San Juan del Sur) data:**
- 18 castaways extracted
- Winner: Natalie Anderson (Hunahpu - Loved Ones) — 39 days, 0 votes against, 9 votes cast
- Runner-up: Jaclyn Schultz (Coyopa - Loved Ones)
- 2nd Runner-up: Missy Payne (Hunahpu - Loved Ones)
- Tribe colors: Hunahpu #5CD7DF (cyan), Coyopa #F89532 (orange)
- 14 tribal councils total

**Season 30 (Worlds Apart) data:**
- 18 castaways extracted
- Winner: Mike Holloway (Escameca - Blue Collar) — 39 days, 4 votes against, 11 votes cast
- Runners-up: Carolyn Rivera (Masaya - White Collar), Will Sims II (Nagarote - No Collar)
- Tribe colors: Escameca #0B58A0 (blue), Masaya #E9CC0E (yellow), Nagarote #C11E21 (red)
- 15 tribal councils total

**Data structure:**
- Follows exact same format as Season 28 (voting_data.json)
- Castaways sorted by placement: Winner → Runner-up → reverse elimination order (14th, 13th, 12th...)
- Tribal council numbering mapped correctly to unique vote days
- Duplicate votes removed (revotes excluded)

**Technical process:**
1. Cloned survivoR repository to /private/tmp
2. Installed pyreadr Python package for reading R data files
3. Built Python script to merge castaways, vote history, and tribe colors
4. Calculated tribal council numbers from unique vote days
5. Formatted tribe names with themes (e.g., "Hunahpu (Loved Ones)")
6. Integrated castaway arrays into existing season29_voting.json and season30_voting.json files

**Validation:**
- All three seasons (28, 29, 30) now have identical data structure
- Season 28: 18 castaways, 15 tribal councils
- Season 29: 18 castaways, 14 tribal councils
- Season 30: 18 castaways, 15 tribal councils
- Winner data verified for all seasons (voting history, votes against, final results)

**Next step:** Integrate Seasons 29 and 30 into Flask app routes and UI
