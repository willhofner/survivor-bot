# Survivor Bot - Master To-Do List

**Generated:** 2026-02-15
**Vision:** Decode the paths to victory — analyze winner strategies across all 40+ seasons

---

## 🔴 HIGH PRIORITY — Foundation

### Data Infrastructure
1. ✅ **Run `export_all_seasons.R`** to pull seasons 1-39 data (script already created)
2. **Update `AVAILABLE_SEASONS`** in app.py to `list(range(1, 40))`
3. **Update `SEASON_NAMES`** dict in app.py with all season names/subtitles
4. **Test Hall of Fame performance** with full 39-season dataset
5. **Verify headshot URLs** work for older seasons (or fallback to initials)
6. **Add data validation layer** — check for missing/malformed data on load
7. **Performance optimization** — Pre-compute Hall of Fame stats if >500ms load time

### Challenge Photos (Current Issue)
8. ✅ **Add placeholder for challenge photos** (grainy photos removed)
9. **Research high-quality challenge photo sources** — CBS, Survivor Wiki, fan archives
10. **Document photo specifications** (resolution, aspect ratio, naming convention)
11. **Create photo upload/management system** (or manual JSON updates)

---

## 🏆 WINNER ANALYSIS — The Core Vision

### Winner Profile Pages
12. **Create "Winners Hall" page** — Gallery of all winners across all seasons
13. **Individual winner profile pages** — Deep dive into each winner's game
14. **Winner comparison view** — Side-by-side stats for 2+ winners
15. **Winning game summary cards** — Key stats at a glance (votes against, idols, challenge wins)

### Statistical Analysis
16. **Calculate challenge win rates** for all winners (pre-merge vs post-merge breakdown)
17. **Track voting accuracy** for winners — % of votes with majority
18. **Measure "blindside resilience"** — times voted incorrectly but still won
19. **Idol/advantage usage patterns** — Do winners play more items? Successfully?
20. **Final tribal council vote margins** — Did they dominate or squeak by?
21. **Days survived correlation** — Do winners make it through without immunity more?

### Strategic Archetype Classification
22. **Define strategic archetypes** — Challenge beast, social floater, strategic mastermind, under-the-radar, etc.
23. **Tag each winner** with primary/secondary archetype
24. **Archetype success rate analysis** — Which strategies win most often?
25. **Archetype evolution over time** — How has the meta changed across eras?

### Paths to Victory Visualization
26. **Create visual "strategy maps"** — Flow diagrams showing different winning paths
27. **Highlight critical moments** — Key immunity wins, crucial votes, blindsides survived
28. **"Winning move" detector** — Identify turning-point decisions in winning games
29. **"Fatal flaw" detector** — Common mistakes that eliminate strong players
30. **Interactive timeline** — Scrub through a winner's game day-by-day

---

## 📊 DATA VISUALIZATIONS

### Charts & Graphs
31. **Challenge performance graphs** — Win rate by challenge type, over time
32. **Voting bloc network diagrams** — Who voted together most often
33. **Power ranking timeline** — Episode-by-episode ranking based on votes received, challenge wins
34. **Alliance formation/dissolution flowcharts** — Track voting patterns to infer alliances
35. **Advantages timeline** — When items were found, played, successful across all seasons

### Comparative Analysis
36. **Season-to-season comparison tool** — Compare two seasons side-by-side
37. **Era analysis** — Early seasons vs middle vs modern (meta evolution)
38. **Tribe swap impact graphs** — Before/after performance metrics
39. **Final tribal council vote distribution** — Jury vote patterns across seasons

---

## 🎨 UI/UX ENHANCEMENTS

### Navigation & Discovery
40. **Global player search** — Search by name across all seasons
41. **Advanced filtering** — Filter by placement, challenge wins, votes received, etc.
42. **"Random player" button** — Discover interesting games
43. **Season recommendations** — "If you liked Season X, try Season Y"
44. **Spoiler-free mode** — Hide winners/placements until user opts in

### Page Improvements
45. **Add sorting to all tables** — Click column headers to sort
46. **Lazy loading** for large datasets (40 seasons of data)
47. **Loading states** for data-heavy pages
48. **"Back to top" buttons** on long pages (already on some, add to all)
49. **Breadcrumb navigation** — Always know where you are in the app

### Visual Polish
50. **Season theme colors** — Each season gets unique color palette (tribe colors, logo colors)
51. **Animated transitions** — Smooth page transitions, hover effects
52. **Responsive design audit** — Mobile, tablet, desktop optimization
53. **Dark mode support** — For late-night Survivor binge analysis

---

## 📝 CONTENT & CONTEXT

### Season Context
54. **Season summaries** — Brief description of each season's theme/twist
55. **Famous quotes** — Memorable lines from each season
56. **Iconic moments** — Tag legendary blindsides, challenge performances, tribal councils
57. **Season twists explained** — Exile Island, Redemption Island, Edge of Extinction, etc.

### Player Context
58. **Player nicknames** — "Boston Rob", "Parvati", etc.
59. **Returning player tracking** — Link multiple appearances by same player
60. **Player archetypes** — Tag players beyond just winners (villains, underdogs, etc.)

---

## 🛠️ TECHNICAL IMPROVEMENTS

### Performance
61. **Implement caching layer** — Redis or in-memory cache for computed stats
62. **Optimize database queries** — Index frequently queried fields
63. **CDN for static assets** — Faster image/CSS/JS loading
64. **Pagination** for large lists (40 seasons of tribal councils = a lot of cards)

### Code Quality
65. **Add unit tests** — Test stat calculations, data transformations
66. **Error handling** — Graceful fallbacks for missing data
67. **API documentation** — Document all endpoints for future frontend rewrite
68. **Code comments** — Document complex stat calculations

### Deployment
69. **Choose hosting platform** — Heroku, Railway, Vercel, etc.
70. **Set up CI/CD pipeline** — Auto-deploy on git push
71. **Production database** — Move from JSON files to PostgreSQL or SQLite
72. **Domain name** — survivorbot.com? survivoranalytics.com?
73. **SSL certificate** — HTTPS for production

---

## 🎯 ADVANCED FEATURES (Future Vision)

### Machine Learning / Advanced Stats
74. **Predict winner likelihood** — Based on episode N stats, who's most likely to win?
75. **"Invisible edit" detector** — Players with low screen time (often lose)
76. **Voting pattern clustering** — Group players by voting behavior
77. **Challenge difficulty estimation** — Based on win rates, which challenges are hardest?

### Social Features
78. **User accounts** — Save favorite players, seasons
79. **Custom lists** — "Best blindsides", "Most robbed players", etc.
80. **Comments/discussions** — Per-episode, per-player discussion threads
81. **Ratings** — Let users rate episodes, players, moves

### Gamification
82. **"Survivor IQ" quiz** — Test your knowledge
83. **Fantasy Survivor** — Draft players, score points based on performance
84. **Prediction game** — Guess who gets voted out next (for live seasons)

---

## 📌 PRIORITY RANKING

**🔴 Do First (Weeks 1-2):**
- Items 1-7: Get all 39 seasons loaded and working
- Items 12-21: Build core winner analysis features
- Items 8-11: Solve challenge photo problem

**🟡 Do Next (Weeks 3-4):**
- Items 22-30: Strategic archetype system and visualizations
- Items 31-39: Core data visualizations
- Items 40-49: UI/UX improvements

**🟢 Do Later (Month 2+):**
- Items 50-60: Content, polish, context
- Items 61-73: Technical improvements, deployment
- Items 74-84: Advanced features, social, gamification

---

## 🎬 QUICK WINS (Low Effort, High Impact)

These can be knocked out quickly for immediate value:

- ✅ Challenge photo placeholders (DONE)
- Global player search (basic text filter)
- Sorting on tables (HTML table sort)
- "Back to top" buttons everywhere
- Season summaries (copy from Wikipedia)
- Spoiler-free mode (CSS hide class)

---

**Total Items: 84**

**Next Actions:**
1. Run `Rscript export_all_seasons.R`
2. Update app.py with all seasons
3. Start building Winners Hall page
