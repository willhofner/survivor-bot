from flask import Flask, render_template, jsonify, request
from collections import Counter
import json
import os
import re
import random

app = Flask(__name__)

# Jinja2 filter for JSON serialization in templates (Markup prevents HTML-escaping in <script> blocks)
from markupsafe import Markup
app.jinja_env.filters['tojson_safe'] = lambda v: Markup(json.dumps(v))

# Available seasons
AVAILABLE_SEASONS = list(range(1, 40))
SEASON_NAMES = {
    1: "Borneo",
    2: "The Australian Outback",
    3: "Africa",
    4: "Marquesas",
    5: "Thailand",
    6: "The Amazon",
    7: "Pearl Islands",
    8: "All-Stars",
    9: "Vanuatu",
    10: "Palau",
    11: "Guatemala",
    12: "Panama",
    13: "Cook Islands",
    14: "Fiji",
    15: "China",
    16: "Micronesia",
    17: "Gabon",
    18: "Tocantins",
    19: "Samoa",
    20: "Heroes vs. Villains",
    21: "Nicaragua",
    22: "Redemption Island",
    23: "South Pacific",
    24: "One World",
    25: "Philippines",
    26: "Caramoan",
    27: "Blood vs. Water",
    28: "Cagayan",
    29: "San Juan del Sur",
    30: "Worlds Apart",
    31: "Cambodia",
    32: "Kaôh Rōng",
    33: "Millennials vs. Gen X",
    34: "Game Changers",
    35: "Heroes vs. Healers vs. Hustlers",
    36: "Ghost Island",
    37: "David vs. Goliath",
    38: "Edge of Extinction",
    39: "Island of the Idols"
}

SEASON_SUMMARIES = {
    1: {"tagline": "The one that started it all", "theme": "16 strangers on a deserted island", "twist": "First-ever season — no playbook existed", "iconic_moment": "Richard Hatch's naked power play at the final immunity challenge", "filming_location": "Pulau Tiga, Borneo"},
    2: {"tagline": "The Outback awaits", "theme": "Survival in the Australian wilderness", "twist": "Skupin falls into the fire — first medical evacuation", "iconic_moment": "Colby taking Tina to Final 2 over Keith", "filming_location": "Herbert River, Queensland, Australia"},
    3: {"tagline": "Survival of the fittest in Africa", "theme": "Harsh African savanna conditions", "twist": "First tribe swap in Survivor history", "iconic_moment": "Lex's paranoia over a mystery vote", "filming_location": "Shaba National Reserve, Kenya"},
    4: {"tagline": "Outwit in the South Pacific", "theme": "Island adventure in Marquesas", "twist": "First post-merge power shift — Rotu Four overthrown", "iconic_moment": "The coconut chop challenge exposing the pecking order", "filming_location": "Nuku Hiva, Marquesas Islands"},
    5: {"tagline": "East meets West", "theme": "Thailand beach survival", "twist": "Fake merge twist", "iconic_moment": "Brian's cold, calculated gameplay earning him the 'Ice Man' title", "filming_location": "Ko Tarutao, Thailand"},
    6: {"tagline": "Battle of the sexes", "theme": "Men vs Women in the Amazon", "twist": "Gender-divided tribes with a tribe swap", "iconic_moment": "Rob Cesternino's strategic gameplay revolutionizing the game", "filming_location": "Amazon River, Brazil"},
    7: {"tagline": "Pirates of the Pacific", "theme": "Pirate-themed adventure", "twist": "The Outcasts twist — voted-out players return", "iconic_moment": "Jonny Fairplay's dead grandmother lie", "filming_location": "Pearl Islands, Panama"},
    8: {"tagline": "All-Stars collide", "theme": "Returning players battle", "twist": "First all-returnee season", "iconic_moment": "Lex's betrayal by Boston Rob at the merge", "filming_location": "Pearl Islands, Panama"},
    9: {"tagline": "Islands of Fire", "theme": "Battle of the sexes in Vanuatu", "twist": "Men vs Women tribes", "iconic_moment": "Chris Daugherty's comeback from being the last man standing", "filming_location": "Efate, Vanuatu"},
    10: {"tagline": "Paradise lost", "theme": "Island survival in Palau", "twist": "Ulong tribe decimated — Stephenie last member", "iconic_moment": "Ulong becoming the first tribe to lose every single immunity challenge", "filming_location": "Koror, Palau"},
    11: {"tagline": "Lost civilization", "theme": "Mayan ruins in Guatemala", "twist": "Two returning players (Stephenie & Bobby Jon)", "iconic_moment": "Danni's under-the-radar win after being on the minority", "filming_location": "Yaxha-Nakum-Naranjo, Guatemala"},
    12: {"tagline": "Exile Island awaits", "theme": "Panama wilderness", "twist": "Exile Island introduced — hidden immunity idol debut", "iconic_moment": "Terry Deitz's incredible immunity run", "filming_location": "Pearl Islands, Panama"},
    13: {"tagline": "Divided they fall", "theme": "Race-divided tribes spark controversy", "twist": "Tribes divided by ethnicity; super idol introduced", "iconic_moment": "Yul's strategic dominance using the super idol as leverage", "filming_location": "Aitutaki, Cook Islands"},
    14: {"tagline": "Two worlds collide", "theme": "Haves vs Have-Nots", "twist": "Unequal tribe conditions", "iconic_moment": "Earl Cole's unanimous jury vote — first in Survivor history", "filming_location": "Macuata, Fiji"},
    15: {"tagline": "Dragon slayers", "theme": "Ancient Chinese warrior theme", "twist": "Kidnapping twist between tribes", "iconic_moment": "Todd's masterful Final Tribal Council performance", "filming_location": "Zhelin Reservoir, Jiangxi, China"},
    16: {"tagline": "Fans vs Favorites", "theme": "New players vs returning favorites", "twist": "First Fans vs Favorites format; surprise final 2", "iconic_moment": "Parvati's double idol play at Final 6 — greatest move ever?", "filming_location": "Koror, Palau"},
    17: {"tagline": "Earth's last Eden", "theme": "African wilderness in Gabon", "twist": "Multiple tribe swaps and schoolyard picks", "iconic_moment": "Sugar's emotional gameplay and the chaotic tribal councils", "filming_location": "Wonga-Wongu\u00e9, Gabon"},
    18: {"tagline": "The warrior spirit", "theme": "Brazilian Highlands survival", "twist": "Exile Island with clues to hidden idol", "iconic_moment": "JT's perfect game — first unanimous winner with no votes against", "filming_location": "Tocantins, Brazil"},
    19: {"tagline": "Russell's revolution", "theme": "Island survival in Samoa", "twist": "Russell Hantz changes the game with aggressive idol hunting", "iconic_moment": "Russell finding idols without clues — pioneering modern gameplay", "filming_location": "Upolu, Samoa"},
    20: {"tagline": "Legends clash", "theme": "Heroes vs Villains — ultimate all-star battle", "twist": "All-returnee season with hero/villain themes", "iconic_moment": "Parvati's double idol play; JT giving Russell his idol", "filming_location": "Upolu, Samoa"},
    21: {"tagline": "Old vs Young", "theme": "Generational divide in Nicaragua", "twist": "Older vs Younger tribes; Medallion of Power", "iconic_moment": "Fabio's immunity run to win despite being underestimated", "filming_location": "San Juan del Sur, Nicaragua"},
    22: {"tagline": "Redemption awaits", "theme": "Second chances through Redemption Island", "twist": "Redemption Island — eliminated players can duel back", "iconic_moment": "Boston Rob's dominant, near-perfect game", "filming_location": "San Juan del Sur, Nicaragua"},
    23: {"tagline": "Divided loyalties", "theme": "Coach vs Ozzy — returning captains", "twist": "Redemption Island returns; returning player captains", "iconic_moment": "Ozzy volunteering to go to Redemption Island", "filming_location": "Upolu, Samoa"},
    24: {"tagline": "One world, one game", "theme": "Both tribes share one beach", "twist": "One World twist — tribes live together", "iconic_moment": "Kim Spradlin's dominant, flawless game", "filming_location": "Upolu, Samoa"},
    25: {"tagline": "Three tribes, three chances", "theme": "Returning player captains lead new tribes", "twist": "Three tribes with returning captains", "iconic_moment": "Denise attending every single tribal council and still winning", "filming_location": "Caramoan, Philippines"},
    26: {"tagline": "Fans vs Favorites II", "theme": "New vs returning players", "twist": "Second Fans vs Favorites season", "iconic_moment": "Cochran's flawless strategic game with zero votes against", "filming_location": "Caramoan, Philippines"},
    27: {"tagline": "Blood is thicker", "theme": "Loved ones compete together", "twist": "Blood vs Water — pairs of loved ones; Redemption Island", "iconic_moment": "Tyson playing his idol at the perfect time to save himself", "filming_location": "Galera, Philippines"},
    28: {"tagline": "Brawn vs Brains vs Beauty", "theme": "Three tribes divided by attributes", "twist": "Triple tribe format; Tyler Perry idol", "iconic_moment": "Tony's spy shack and chaotic, paranoid gameplay leading to victory", "filming_location": "Cagayan, Philippines"},
    29: {"tagline": "Blood vs Water II", "theme": "Loved ones compete on opposing tribes", "twist": "Blood vs Water with all new players", "iconic_moment": "Natalie's revenge game after her twin sister Nadiya was first out", "filming_location": "San Juan del Sur, Nicaragua"},
    30: {"tagline": "White collar vs Blue collar vs No collar", "theme": "Work ethic and lifestyle divisions", "twist": "Triple tribe format based on work philosophy", "iconic_moment": "Mike's immunity run from Final 7 to the end", "filming_location": "San Juan del Sur, Nicaragua"},
    31: {"tagline": "Second chances", "theme": "Fan-voted returning players get another shot", "twist": "All-returnee cast voted in by fans; no Redemption Island", "iconic_moment": "Jeremy's emotional idol play to save Stephen Fishbach", "filming_location": "Koh Rong, Cambodia"},
    32: {"tagline": "Brawn vs Brains vs Beauty II", "theme": "Return of the triple attribute tribes", "twist": "Multiple medical evacuations", "iconic_moment": "Tai finding and misplaying the super idol; Michele's underdog win", "filming_location": "Koh Rong, Cambodia"},
    33: {"tagline": "Generational showdown", "theme": "Millennials vs Generation X", "twist": "Generational divide; Legacy Advantage introduced", "iconic_moment": "Adam's emotional reveal about his mother at Final Tribal", "filming_location": "Mamanuca Islands, Fiji"},
    34: {"tagline": "Game changers unite", "theme": "Returning players who changed the game", "twist": "All-returnee; Legacy Advantage returns", "iconic_moment": "Sarah playing 'like a criminal' — the vote steal at Final 6", "filming_location": "Mamanuca Islands, Fiji"},
    35: {"tagline": "Heroes, Healers, and Hustlers", "theme": "Triple tribe based on life roles", "twist": "Triple tribe format; fire-making at Final 4 introduced", "iconic_moment": "Ben's historic idol streak and fire-making twist victory", "filming_location": "Mamanuca Islands, Fiji"},
    36: {"tagline": "Reverse the curse", "theme": "Haunted by past Survivor mistakes", "twist": "Ghost Island — cursed advantages from past seasons", "iconic_moment": "Domenick and Wendell's tied jury vote — first in history", "filming_location": "Mamanuca Islands, Fiji"},
    37: {"tagline": "Underdogs vs Giants", "theme": "David vs Goliath — overcoming the odds", "twist": "Underdogs vs powerhouses", "iconic_moment": "Christian Hubicki's epic immunity challenge endurance", "filming_location": "Mamanuca Islands, Fiji"},
    38: {"tagline": "The edge of survival", "theme": "Edge of Extinction gives eliminated players a chance", "twist": "Edge of Extinction — eliminated players live on a separate island", "iconic_moment": "Chris Underwood returning on Day 35 and winning it all", "filming_location": "Mamanuca Islands, Fiji"},
    39: {"tagline": "Mentors on the island", "theme": "Boston Rob and Sandra as mentors on Island of the Idols", "twist": "Island of the Idols — players visit mentors for advantages", "iconic_moment": "The season's controversy overshadowing the strategic gameplay", "filming_location": "Mamanuca Islands, Fiji"},
}

# Load data for all seasons
def load_season_data(season_num):
    """Load all data files for a specific season"""
    import os
    data = {}

    # Voting data (Season 28 uses different filename)
    voting_file = 'data/voting_data.json' if season_num == 28 else f'data/season{season_num}_voting.json'
    try:
        with open(voting_file, 'r') as f:
            data['voting'] = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data['voting'] = {"season": season_num, "castaways": [], "episodes": []}

    # Challenges
    try:
        with open(f'data/season{season_num}_challenges.json', 'r') as f:
            data['challenges'] = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data['challenges'] = {"season": season_num, "challenges": []}

    # Advantages/Idols (optional - not all seasons have this file yet)
    try:
        with open(f'data/season{season_num}_advantages_idols.json', 'r') as f:
            data['advantages'] = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data['advantages'] = {"season": season_num, "advantages": []}

    # Timeline (optional)
    try:
        with open(f'data/season{season_num}_timeline.json', 'r') as f:
            data['timeline'] = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data['timeline'] = {"season": season_num, "events": []}

    # Headshots (optional)
    try:
        with open(f'data/season{season_num}_headshots.json', 'r') as f:
            data['headshots'] = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data['headshots'] = {}

    # Challenge photos (optional)
    try:
        with open(f'data/season{season_num}_challenge_photos.json', 'r') as f:
            data['challenge_photos'] = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data['challenge_photos'] = {}

    return data

# Load player nicknames
player_nicknames = {}
try:
    with open('data/player_nicknames.json', 'r') as f:
        player_nicknames = json.load(f).get('nicknames', {})
except (FileNotFoundError, json.JSONDecodeError):
    pass

# Load famous quotes
famous_quotes = []
try:
    with open('data/famous_quotes.json', 'r') as f:
        famous_quotes = json.load(f).get('quotes', [])
except (FileNotFoundError, json.JSONDecodeError):
    pass

# Load all seasons at startup
seasons_data = {}
for season in AVAILABLE_SEASONS:
    seasons_data[season] = load_season_data(season)

# Helper functions
def calculate_voting_accuracy(castaway_name, voting_data, tribal_councils=None):
    """Calculate voting accuracy for a castaway using tribal council elimination data."""
    castaway = next((c for c in voting_data['castaways'] if c['name'] == castaway_name), None)
    if not castaway or not castaway.get('voting_history'):
        return {'correct': 0, 'total': 0, 'accuracy': 0}

    total_votes = len([v for v in castaway['voting_history'] if v.get('voted_for')])
    if total_votes == 0:
        return {'correct': 0, 'total': 0, 'accuracy': 0}

    # Build elimination map from tribal councils (reconstructed or from episodes)
    elimination_map = {}
    if tribal_councils:
        for tc in tribal_councils:
            elimination_map[tc['number']] = tc.get('eliminated', '')
    elif 'episodes' in voting_data:
        for episode in voting_data['episodes']:
            for tc in episode['tribal_councils']:
                elimination_map[tc['number']] = tc['eliminated']

    if not elimination_map:
        return {'correct': 0, 'total': total_votes, 'accuracy': 0}

    correct_votes = 0
    for vote in castaway['voting_history']:
        tc_num = vote.get('tc', vote.get('tribal_council', 0))
        voted_for = vote.get('voted_for', vote.get('vote', ''))
        if voted_for and tc_num in elimination_map and voted_for == elimination_map[tc_num]:
            correct_votes += 1

    accuracy = round((correct_votes / total_votes * 100), 1) if total_votes > 0 else 0
    return {'correct': correct_votes, 'total': total_votes, 'accuracy': accuracy}

def calculate_challenge_beast_metrics(castaway_name, challenge_data):
    """Calculate challenge wins for a castaway (individual challenges only for immunity)"""
    immunity_wins = 0
    reward_wins = 0

    for challenge in challenge_data['challenges']:
        if castaway_name in challenge.get('winners', []):
            outcome = challenge.get('outcome_type', '')
            if 'Immunity' in challenge['challenge_type'] and outcome == 'Individual':
                immunity_wins += 1
            if 'Reward' in challenge['challenge_type'] and challenge['challenge_type'] != 'Immunity' and outcome == 'Individual':
                reward_wins += 1

    return {
        'immunity_wins': immunity_wins,
        'reward_wins': reward_wins,
        'total_wins': immunity_wins + reward_wins
    }

def calculate_episode_grade(tribal_council, advantages_data):
    """Calculate drama score for a tribal council"""
    score = 5.0  # Base score

    # Check if merge
    if 'Merged' in tribal_council.get('tribe', '') or 'Solarrion' in tribal_council.get('tribe', '') or 'Merica' in tribal_council.get('tribe', '') or 'Huyopa' in tribal_council.get('tribe', ''):
        score += 2.0

    # Count advantages played at this tribal (match by day or tc number)
    tc_day = tribal_council.get('day')
    advantages_played = 0
    for adv in advantages_data.get('advantages', []):
        if adv.get('day_played') == tc_day or adv.get('played_day') == tc_day:
            advantages_played += 1
    score += advantages_played * 1.0

    # Check vote spread
    votes = tribal_council.get('votes', [])
    if len(votes) >= 2:
        vote_counts = [v['count'] for v in votes]
        if abs(vote_counts[0] - vote_counts[1]) <= 2:
            score += 1.0

    # Multiple targets
    unique_targets = len(votes)
    if unique_targets > 2:
        score += (unique_targets - 2) * 0.5

    return min(score, 10.0)

def get_flame_rating(score):
    """Convert score to flame emoji rating"""
    full_flames = int(score)
    half_flame = '🔥½' if (score - full_flames) >= 0.5 else ''
    return '🔥' * full_flames + half_flame

def reconstruct_tribal_councils(voting_data, advantages_data):
    """Reconstruct tribal council data from castaway voting histories when episodes data is missing."""
    castaways = voting_data.get('castaways', [])
    if not castaways:
        return []

    # Build elimination order from placement strings
    eliminations = []
    for c in castaways:
        placement = c.get('placement', '')
        match = re.match(r'(\d+)(?:st|nd|rd|th)\s+voted\s+out', placement, re.IGNORECASE)
        if match:
            eliminations.append((int(match.group(1)), c['name']))
    eliminations.sort(key=lambda x: x[0])
    eliminated_names = [name for _, name in eliminations]

    # Collect all votes grouped by TC number
    tc_votes = {}
    for castaway in castaways:
        for vote in castaway.get('voting_history', []):
            tc_num = vote.get('tribal_council', 0)
            if tc_num == 0:
                continue
            if tc_num not in tc_votes:
                tc_votes[tc_num] = []
            target = vote.get('voted_for', '')
            if target:
                tc_votes[tc_num].append({
                    'voter': castaway['name'],
                    'target': target,
                    'day': vote.get('day', 0),
                    'tribe': castaway.get('original_tribe', 'Unknown')
                })

    if not tc_votes:
        return []

    # Build tribal councils in order
    tribal_councils = []
    sorted_tc_nums = sorted(tc_votes.keys())
    elim_idx = 0

    for tc_num in sorted_tc_nums:
        votes = tc_votes[tc_num]
        if not votes:
            continue

        day = votes[0]['day']

        # Count votes per target
        vote_counts = {}
        vote_voters = {}
        for v in votes:
            t = v['target']
            vote_counts[t] = vote_counts.get(t, 0) + 1
            vote_voters.setdefault(t, []).append(v['voter'])

        # Build vote groups sorted by count descending
        vote_groups = []
        for target, count in sorted(vote_counts.items(), key=lambda x: -x[1]):
            vote_groups.append({
                'target': target,
                'count': count,
                'voters': vote_voters[target]
            })

        # Determine who was eliminated
        # Primary: use elimination order (most reliable)
        # Fallback: person with the most votes
        eliminated = 'Unknown'
        if elim_idx < len(eliminated_names):
            # Check if the expected elimination is among the vote targets
            expected = eliminated_names[elim_idx]
            if expected in vote_counts:
                eliminated = expected
                elim_idx += 1
            elif vote_groups:
                # Idol may have been played — the majority target survived
                # Check if the majority target is NOT in our elimination list at this position
                # Use the next elimination that matches a target at this TC
                found = False
                for i in range(elim_idx, min(elim_idx + 3, len(eliminated_names))):
                    if eliminated_names[i] in vote_counts:
                        eliminated = eliminated_names[i]
                        # Reorder elimination list
                        eliminated_names.pop(i)
                        eliminated_names.insert(elim_idx, eliminated)
                        elim_idx += 1
                        found = True
                        break
                if not found:
                    eliminated = vote_groups[0]['target']
                    elim_idx += 1
        elif vote_groups:
            eliminated = vote_groups[0]['target']

        # Determine tribe from voters
        tribe_counts = {}
        for v in votes:
            t = v['tribe']
            tribe_counts[t] = tribe_counts.get(t, 0) + 1
        tribe = max(tribe_counts, key=tribe_counts.get) if tribe_counts else 'Unknown'

        # Estimate episode number
        episode_number = tc_num

        tc_data = {
            'number': tc_num,
            'day': day,
            'episode_number': episode_number,
            'tribe': tribe,
            'eliminated': eliminated,
            'votes': vote_groups,
            'notes': ''
        }

        # Calculate drama score
        tc_data['drama_score'] = round(calculate_episode_grade(tc_data, advantages_data), 1)
        tc_data['flame_rating'] = get_flame_rating(tc_data['drama_score'])

        tribal_councils.append(tc_data)

    return tribal_councils


# Enrich data for all seasons
for season_num, season_data in seasons_data.items():
    voting_data = season_data['voting']
    challenge_data = season_data['challenges']
    advantages_data = season_data['advantages']

    # Build tribal councils first (needed for voting accuracy)
    all_tribal_councils = []
    if 'episodes' in voting_data:
        for episode in voting_data['episodes']:
            for tc in episode['tribal_councils']:
                tc['episode_number'] = episode['number']
                tc['drama_score'] = calculate_episode_grade(tc, advantages_data)
                tc['flame_rating'] = get_flame_rating(tc['drama_score'])
                all_tribal_councils.append(tc)
    else:
        all_tribal_councils = reconstruct_tribal_councils(voting_data, advantages_data)
    season_data['tribal_councils'] = all_tribal_councils

    # Add computed stats to castaways (uses tribal councils for voting accuracy)
    for castaway in voting_data['castaways']:
        castaway['voting_accuracy'] = calculate_voting_accuracy(
            castaway['name'], voting_data, tribal_councils=all_tribal_councils)
        castaway['challenge_stats'] = calculate_challenge_beast_metrics(castaway['name'], challenge_data)
        castaway['headshot'] = season_data['headshots'].get(castaway['name'], '')
        castaway['nickname'] = player_nicknames.get(castaway['name'], '')

    # Add challenge photos
    challenge_photos_map = season_data['challenge_photos'].get('challenge_photos', {})
    # Convert photo map keys to list for index-based matching
    photo_urls = list(challenge_photos_map.values())

    for idx, challenge in enumerate(challenge_data['challenges']):
        # Try index-based matching first (photos are in episode order)
        if idx < len(photo_urls):
            challenge['photo'] = photo_urls[idx]
        else:
            challenge['photo'] = ''

# --- PRE-COMPUTED STATS ---

def find_all_max(items, key_func):
    """Find ALL items that share the maximum value (handles ties)"""
    if not items:
        return []
    max_val = max(key_func(item) for item in items)
    return [item for item in items if key_func(item) == max_val]

def find_all_min(items, key_func):
    """Find ALL items that share the minimum value (handles ties)"""
    if not items:
        return []
    min_val = min(key_func(item) for item in items)
    return [item for item in items if key_func(item) == min_val]

def precompute_hall_of_fame():
    """Pre-compute Hall of Fame stats at startup for performance"""
    all_castaways = []
    champions = []

    for season_num, season_data in seasons_data.items():
        voting_data = season_data['voting']
        for castaway in voting_data['castaways']:
            castaway_record = castaway.copy()
            castaway_record['season'] = season_num
            castaway_record['season_name'] = SEASON_NAMES[season_num]
            if castaway.get('placement') == 'Winner':
                champions.append(castaway_record)
            all_castaways.append(castaway_record)

    individual_records = {
        'highest_voting_accuracy_champion': find_all_max(champions, lambda c: c.get('voting_accuracy', {}).get('accuracy', 0)),
        'lowest_voting_accuracy_champion': find_all_min(champions, lambda c: c.get('voting_accuracy', {}).get('accuracy', 0)),
        'most_challenge_wins': find_all_max(all_castaways, lambda c: c.get('challenge_stats', {}).get('total_wins', 0)),
        'most_challenge_wins_champion': find_all_max(champions, lambda c: c.get('challenge_stats', {}).get('total_wins', 0)),
        'least_challenge_wins_champion': find_all_min(champions, lambda c: c.get('challenge_stats', {}).get('total_wins', 0)),
        'most_immunity_wins': find_all_max(all_castaways, lambda c: c.get('challenge_stats', {}).get('immunity_wins', 0)),
        'most_immunity_wins_champion': find_all_max(champions, lambda c: c.get('challenge_stats', {}).get('immunity_wins', 0)),
        'most_votes_received_champion': find_all_max(champions, lambda c: c.get('votes_against', 0)),
        'least_votes_received_champion': find_all_min(champions, lambda c: c.get('votes_against', 0)),
    }

    idol_records = []
    for season_num, season_data in seasons_data.items():
        for adv in season_data['advantages'].get('advantages', []):
            idol_records.append({**adv, 'season': season_num, 'season_name': SEASON_NAMES[season_num]})

    most_votes_nullified = max(idol_records, key=lambda x: x.get('votes_negated', 0)) if idol_records else None

    successful_plays_by_player = Counter()
    for idol in idol_records:
        if idol.get('result') == 'successful':
            player = idol.get('found_by') or idol.get('played_for')
            if player:
                successful_plays_by_player[player] += 1
    most_successful_idol_player = max(successful_plays_by_player.items(), key=lambda x: x[1]) if successful_plays_by_player else (None, 0)

    idols_by_season = Counter()
    items_by_season = Counter()
    for idol in idol_records:
        if idol.get('day_played'):
            idols_by_season[idol['season']] += 1
        items_by_season[idol['season']] += 1

    most_idols_played_season = max(idols_by_season.items(), key=lambda x: x[1]) if idols_by_season else (None, 0)
    most_items_season = max(items_by_season.items(), key=lambda x: x[1]) if items_by_season else (None, 0)

    season_records = {}
    for season_num, season_data in seasons_data.items():
        advantages = season_data['advantages'].get('advantages', [])
        voting_data = season_data['voting']
        votes_nullified = sum(adv.get('votes_negated', 0) for adv in advantages)
        voted_out_holding = sum(1 for adv in advantages if adv.get('voted_out_holding'))
        all_vote_targets = set()
        for episode in voting_data.get('episodes', []):
            for tc in episode.get('tribal_councils', []):
                for vote_group in tc.get('votes', []):
                    all_vote_targets.add(vote_group.get('target'))
        season_records[season_num] = {
            'season': season_num,
            'season_name': SEASON_NAMES[season_num],
            'items_played': len([a for a in advantages if a.get('day_played')]),
            'votes_nullified': votes_nullified,
            'voted_out_holding': voted_out_holding,
            'players_receiving_votes': len(all_vote_targets)
        }

    return {
        'individual_records': individual_records,
        'most_votes_nullified': most_votes_nullified,
        'most_successful_idol_player': most_successful_idol_player,
        'most_idols_played_season': most_idols_played_season,
        'most_items_season': most_items_season,
        'season_records': season_records,
        'all_castaways': all_castaways,
        'idol_records': idol_records,
    }

hall_of_fame_cache = precompute_hall_of_fame()


def get_season_param(default=28):
    """Safely parse season query parameter"""
    try:
        season = int(request.args.get('season', default))
    except (ValueError, TypeError):
        season = default
    if season not in AVAILABLE_SEASONS:
        season = default
    return season

@app.route('/')
def index():
    """Landing page with season selector"""
    import random
    total_castaways = sum(len(sd['voting']['castaways']) for sd in seasons_data.values())
    total_challenges = sum(len(sd['challenges']['challenges']) for sd in seasons_data.values())
    featured = random.choice(winner_profiles) if winner_profiles else None
    quote = random.choice(famous_quotes) if famous_quotes else None
    return render_template('index.html',
                         seasons=AVAILABLE_SEASONS,
                         season_names=SEASON_NAMES,
                         total_castaways=total_castaways,
                         total_challenges=total_challenges,
                         winner_count=len(winner_profiles),
                         featured_winner=featured,
                         quote=quote)

@app.route('/tribal-councils')
def tribal_councils():
    """Scrollable tribal councils view"""
    season = get_season_param()

    season_data = seasons_data[season]
    return render_template('tribal_councils.html',
                         tribal_councils=season_data['tribal_councils'],
                         season=season,
                         season_name=SEASON_NAMES[season],
                         seasons=AVAILABLE_SEASONS,
                         season_names=SEASON_NAMES)

@app.route('/castaways')
def castaways():
    """Castaway view - individual player profiles with voting accuracy and challenge stats"""
    season = get_season_param()

    season_data = seasons_data[season]
    return render_template('castaways.html',
                         castaways=season_data['voting']['castaways'],
                         season=season,
                         season_name=SEASON_NAMES[season],
                         seasons=AVAILABLE_SEASONS,
                         season_names=SEASON_NAMES)

@app.route('/challenges')
def challenges():
    """Challenge outcomes timeline"""
    season = get_season_param()

    season_data = seasons_data[season]
    return render_template('challenges.html',
                         challenges=season_data['challenges']['challenges'],
                         season=season,
                         season_name=SEASON_NAMES[season],
                         seasons=AVAILABLE_SEASONS,
                         season_names=SEASON_NAMES)

@app.route('/events')
def events():
    """Key events timeline"""
    season = get_season_param()

    season_data = seasons_data[season]
    return render_template('events.html',
                         events=season_data['timeline'].get('events', []),
                         season=season,
                         season_name=SEASON_NAMES[season],
                         seasons=AVAILABLE_SEASONS,
                         season_names=SEASON_NAMES)

@app.route('/items')
def items():
    """Item/advantage tracking"""
    season = get_season_param()

    season_data = seasons_data[season]
    return render_template('items.html',
                         advantages=season_data['advantages'].get('advantages', []),
                         summary=season_data['advantages'].get('summary', {}),
                         season=season,
                         season_name=SEASON_NAMES[season],
                         seasons=AVAILABLE_SEASONS,
                         season_names=SEASON_NAMES)

@app.route('/api/episode/<int:season>/<int:episode_num>')
def get_episode(season, episode_num):
    """API endpoint for episode data"""
    if season not in AVAILABLE_SEASONS:
        return jsonify({'error': 'Season not found'}), 404

    season_data = seasons_data[season]
    episodes = season_data['voting'].get('episodes', [])
    episode = next((e for e in episodes if e['number'] == episode_num), None)
    return jsonify(episode) if episode else (jsonify({'error': 'Episode not found'}), 404)

@app.route('/api/castaway/<int:season>/<name>')
def get_castaway(season, name):
    """API endpoint for castaway data"""
    if season not in AVAILABLE_SEASONS:
        return jsonify({'error': 'Season not found'}), 404

    season_data = seasons_data[season]
    castaway = next((c for c in season_data['voting']['castaways'] if c['name'].lower() == name.lower()), None)
    return jsonify(castaway) if castaway else (jsonify({'error': 'Castaway not found'}), 404)

@app.route('/hall-of-fame')
def hall_of_fame():
    """Hall of Fame - all-time records across all seasons (pre-computed)"""
    return render_template('hall_of_fame.html',
                         individual_records=hall_of_fame_cache['individual_records'],
                         most_votes_nullified=hall_of_fame_cache['most_votes_nullified'],
                         most_successful_idol_player=hall_of_fame_cache['most_successful_idol_player'],
                         most_idols_played_season=hall_of_fame_cache['most_idols_played_season'],
                         most_items_season=hall_of_fame_cache['most_items_season'],
                         season_records=hall_of_fame_cache['season_records'],
                         seasons=AVAILABLE_SEASONS,
                         season_names=SEASON_NAMES)

# --- WINNER PROFILES ---

def load_winner_profiles():
    """Load all winner profiles from .temp/winner_profiles/"""
    profiles = []
    profiles_dir = os.path.join(os.path.dirname(__file__), '.temp', 'winner_profiles')
    if not os.path.exists(profiles_dir):
        return profiles
    for season_num in range(1, 40):
        filepath = os.path.join(profiles_dir, f'season{season_num}.json')
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    profiles.append(json.load(f))
            except (json.JSONDecodeError, IOError):
                continue
    return sorted(profiles, key=lambda p: p.get('season', 0))

winner_profiles = load_winner_profiles()

def get_winner_aggregate_stats(profiles):
    """Calculate aggregate stats across all winners"""
    if not profiles:
        return {'avg_immunity': 0, 'avg_voting_control': 0, 'avg_social': 0, 'avg_physical': 0}
    n = len(profiles)
    return {
        'avg_immunity': sum(p.get('stats', {}).get('immunity_wins', 0) for p in profiles) / n,
        'avg_voting_control': sum(p.get('archetype', {}).get('voting_control', 0) for p in profiles) / n,
        'avg_social': sum(p.get('archetype', {}).get('social_capital', 0) for p in profiles) / n,
        'avg_physical': sum(p.get('archetype', {}).get('physical_game', 0) for p in profiles) / n,
    }

@app.route('/winners')
def winners():
    """Winners Hall - gallery of all season winners with strategic profiles"""
    avg_stats = get_winner_aggregate_stats(winner_profiles)
    return render_template('winners.html',
                         winners=winner_profiles,
                         avg_stats=avg_stats,
                         seasons=AVAILABLE_SEASONS,
                         season_names=SEASON_NAMES)

@app.route('/winner/<int:season>')
def winner_profile(season):
    """Individual winner profile page"""
    winner = next((p for p in winner_profiles if p['season'] == season), None)
    if not winner:
        return 'Winner not found', 404

    # Find prev/next winners for navigation
    idx = winner_profiles.index(winner)
    prev_winner = winner_profiles[idx - 1] if idx > 0 else None
    next_winner = winner_profiles[idx + 1] if idx < len(winner_profiles) - 1 else None

    return render_template('winner_profile.html',
                         winner=winner,
                         prev_winner=prev_winner,
                         next_winner=next_winner,
                         seasons=AVAILABLE_SEASONS,
                         season_names=SEASON_NAMES)

@app.route('/compare')
def compare_winners():
    """Compare 2-4 winners side-by-side with overlapping radar charts"""
    return render_template('compare.html',
                         winners=winner_profiles,
                         seasons=AVAILABLE_SEASONS,
                         season_names=SEASON_NAMES)

@app.route('/seasons')
def seasons_overview():
    """Season summaries and overview page"""
    season_summaries = []
    for season_num in AVAILABLE_SEASONS:
        sd = seasons_data[season_num]
        castaway_count = len(sd['voting']['castaways'])
        challenge_count = len(sd['challenges']['challenges'])
        winner = next((p for p in winner_profiles if p['season'] == season_num), None)
        winner_name = winner['name'] if winner else 'Unknown'

        summary = SEASON_SUMMARIES.get(season_num, {})
        recs = SEASON_RECOMMENDATIONS.get(season_num, [])
        rec_names = [{'season': r, 'name': SEASON_NAMES.get(r, '')} for r in recs[:3]]

        season_summaries.append({
            'season': season_num,
            'name': SEASON_NAMES[season_num],
            'castaway_count': castaway_count,
            'challenge_count': challenge_count,
            'winner': winner_name,
            'tagline': summary.get('tagline', ''),
            'theme': summary.get('theme', ''),
            'twist': summary.get('twist', ''),
            'iconic_moment': summary.get('iconic_moment', ''),
            'filming_location': summary.get('filming_location', ''),
            'similar_seasons': rec_names,
        })

    return render_template('seasons.html',
                         season_summaries=season_summaries,
                         seasons=AVAILABLE_SEASONS,
                         season_names=SEASON_NAMES)

@app.route('/analytics')
def analytics():
    """Data visualizations and era analysis"""
    # Compute era stats for winners
    eras = {
        'Classic (1-7)': [p for p in winner_profiles if 1 <= p['season'] <= 7],
        'Golden Age (8-14)': [p for p in winner_profiles if 8 <= p['season'] <= 14],
        'Strategy Era (15-20)': [p for p in winner_profiles if 15 <= p['season'] <= 20],
        'Modern (21-28)': [p for p in winner_profiles if 21 <= p['season'] <= 28],
        'New School (29-39)': [p for p in winner_profiles if 29 <= p['season'] <= 39],
    }

    era_stats = {}
    for era_name, profiles in eras.items():
        if not profiles:
            continue
        n = len(profiles)
        era_stats[era_name] = {
            'count': n,
            'avg_voting_control': round(sum(p['archetype']['voting_control'] for p in profiles) / n, 1),
            'avg_physical': round(sum(p['archetype']['physical_game'] for p in profiles) / n, 1),
            'avg_social': round(sum(p['archetype']['social_capital'] for p in profiles) / n, 1),
            'avg_aggression': round(sum(p['archetype']['strategic_aggression'] for p in profiles) / n, 1),
            'avg_immunity': round(sum(p['stats']['immunity_wins'] for p in profiles) / n, 1),
            'avg_idols': round(sum(p['stats']['idols_played'] for p in profiles) / n, 1),
            'avg_days': round(sum(p['stats']['days_lasted'] for p in profiles) / n, 1),
        }

    # Per-season winner data for line charts
    winner_timeline = []
    for p in winner_profiles:
        winner_timeline.append({
            'season': p['season'],
            'name': p['name'],
            'voting_control': p['archetype']['voting_control'],
            'physical_game': p['archetype']['physical_game'],
            'social_capital': p['archetype']['social_capital'],
            'strategic_aggression': p['archetype']['strategic_aggression'],
            'immunity_wins': p['stats']['immunity_wins'],
            'idols_played': p['stats']['idols_played'],
            'voting_accuracy': p['stats']['voting_accuracy'],
        })

    # Archetype distribution for pie/bar chart
    archetype_dist = {'Strategist': 0, 'Physical': 0, 'Social': 0, 'Balanced': 0}
    for p in winner_profiles:
        a = p['archetype']
        max_val = max(a['voting_control'], a['physical_game'], a['social_capital'], a['strategic_aggression'])
        if a['voting_control'] == max_val or a['strategic_aggression'] == max_val:
            if abs(a['voting_control'] - a['physical_game']) <= 1 and abs(a['social_capital'] - a['physical_game']) <= 1:
                archetype_dist['Balanced'] += 1
            else:
                archetype_dist['Strategist'] += 1
        elif a['physical_game'] == max_val:
            archetype_dist['Physical'] += 1
        elif a['social_capital'] == max_val:
            archetype_dist['Social'] += 1
        else:
            archetype_dist['Balanced'] += 1

    return render_template('analytics.html',
                         era_stats=era_stats,
                         winner_timeline=winner_timeline,
                         archetype_dist=archetype_dist,
                         winners=winner_profiles,
                         seasons=AVAILABLE_SEASONS,
                         season_names=SEASON_NAMES)

# --- GLOBAL SEARCH API ---

@app.route('/quiz')
def quiz():
    """Survivor IQ Quiz page"""
    quiz_data = {}
    try:
        with open('data/quiz_questions.json', 'r') as f:
            quiz_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        quiz_data = {"categories": []}

    return render_template('quiz.html',
                         quiz_data=quiz_data,
                         seasons=AVAILABLE_SEASONS,
                         season_names=SEASON_NAMES)


@app.route('/returning-players')
def returning_players():
    """Returning players tracking across seasons"""
    players_data = []
    try:
        with open('data/returning_players.json', 'r') as f:
            data = json.load(f)
            players_data = data.get('returning_players', [])
    except (FileNotFoundError, json.JSONDecodeError):
        players_data = []

    return render_template('returning_players.html',
                         players=players_data,
                         seasons=AVAILABLE_SEASONS,
                         season_names=SEASON_NAMES)


@app.route('/paths-to-victory')
def paths_to_victory():
    """Interactive Paths to Victory — explore how each winner won"""
    archetypes = {}
    for p in winner_profiles:
        a = p.get('archetype', {})
        scores = {
            'Strategic Mastermind': a.get('voting_control', 0) + a.get('strategic_aggression', 0),
            'Challenge Beast': a.get('physical_game', 0) * 2,
            'Social Player': a.get('social_capital', 0) * 2,
        }
        primary = max(scores, key=scores.get)
        vals = [a.get('voting_control', 0), a.get('physical_game', 0),
                a.get('social_capital', 0), a.get('strategic_aggression', 0)]
        if max(vals) - min(vals) <= 3:
            primary = 'Balanced'
        archetypes.setdefault(primary, []).append(p)

    return render_template('paths_to_victory.html',
                         winners=winner_profiles,
                         archetypes=archetypes,
                         seasons=AVAILABLE_SEASONS,
                         season_names=SEASON_NAMES)


@app.route('/challenge-performance')
def challenge_performance():
    """Cross-season challenge performance analysis"""
    # Per-season challenge stats
    season_challenge_stats = []
    top_performers = []

    for s in AVAILABLE_SEASONS:
        sd = seasons_data[s]
        challenges = sd['challenges']['challenges']
        castaways = sd['voting']['castaways']

        immunity_challenges = [c for c in challenges if 'Immunity' in c.get('challenge_type', '')]
        reward_challenges = [c for c in challenges if 'Reward' in c.get('challenge_type', '') and c.get('challenge_type') != 'Immunity']

        # Find top challenge performer in this season
        performer_wins = {}
        for c in challenges:
            for w in c.get('winners', []):
                performer_wins[w] = performer_wins.get(w, 0) + 1
        if performer_wins:
            top_name = max(performer_wins, key=performer_wins.get)
            top_performers.append({
                'name': top_name,
                'season': s,
                'season_name': SEASON_NAMES[s],
                'wins': performer_wins[top_name],
            })

        season_challenge_stats.append({
            'season': s,
            'name': SEASON_NAMES[s],
            'total': len(challenges),
            'immunity': len(immunity_challenges),
            'reward': len(reward_challenges),
        })

    # Sort top performers by wins
    top_performers.sort(key=lambda x: -x['wins'])

    # Winner challenge wins from profiles
    winner_challenge_data = []
    for p in winner_profiles:
        winner_challenge_data.append({
            'season': p['season'],
            'name': p['name'],
            'immunity_wins': p['stats'].get('immunity_wins', 0),
            'reward_wins': p['stats'].get('reward_wins', 0),
            'total_wins': p['stats'].get('immunity_wins', 0) + p['stats'].get('reward_wins', 0),
        })

    return render_template('challenge_performance.html',
                         season_challenge_stats=season_challenge_stats,
                         top_performers=top_performers[:20],
                         winner_challenge_data=winner_challenge_data,
                         seasons=AVAILABLE_SEASONS,
                         season_names=SEASON_NAMES)


@app.route('/advantages-timeline')
def advantages_timeline():
    """Cross-season advantages timeline visualization"""
    all_advantages = []
    for season_num in AVAILABLE_SEASONS:
        season_data = seasons_data[season_num]
        for adv in season_data['advantages'].get('advantages', []):
            all_advantages.append({
                **adv,
                'season': season_num,
                'season_name': SEASON_NAMES[season_num],
            })

    # Group by type
    type_counts = Counter()
    for adv in all_advantages:
        adv_type = adv.get('type', adv.get('advantage_type', 'Unknown'))
        type_counts[adv_type] += 1

    # Per-season counts
    season_counts = {}
    for s in AVAILABLE_SEASONS:
        advs = seasons_data[s]['advantages'].get('advantages', [])
        season_counts[s] = {
            'total': len(advs),
            'played': sum(1 for a in advs if a.get('day_played') or a.get('played_day')),
            'successful': sum(1 for a in advs if a.get('result') == 'successful'),
            'votes_negated': sum(a.get('votes_negated', 0) for a in advs),
        }

    return render_template('advantages_timeline.html',
                         all_advantages=all_advantages,
                         type_counts=dict(type_counts.most_common()),
                         season_counts=season_counts,
                         seasons=AVAILABLE_SEASONS,
                         season_names=SEASON_NAMES)


@app.route('/voting-patterns')
def voting_patterns():
    """FTC vote distribution and voting pattern analysis"""
    # Collect FTC data from winner profiles
    ftc_data = []
    for p in winner_profiles:
        ftc_data.append({
            'season': p['season'],
            'season_name': p.get('season_name', SEASON_NAMES.get(p['season'], '')),
            'winner': p['name'],
            'jury_votes': p['stats'].get('jury_votes', ''),
            'voting_accuracy': p['stats'].get('voting_accuracy', 0),
            'votes_against': p['stats'].get('times_received_votes', p['stats'].get('votes_against', 0)),
        })

    # Voting accuracy distribution
    accuracy_buckets = {'90-100%': 0, '80-89%': 0, '70-79%': 0, '60-69%': 0, '<60%': 0}
    for p in winner_profiles:
        acc = p['stats'].get('voting_accuracy', 0)
        if acc >= 90:
            accuracy_buckets['90-100%'] += 1
        elif acc >= 80:
            accuracy_buckets['80-89%'] += 1
        elif acc >= 70:
            accuracy_buckets['70-79%'] += 1
        elif acc >= 60:
            accuracy_buckets['60-69%'] += 1
        else:
            accuracy_buckets['<60%'] += 1

    return render_template('voting_patterns.html',
                         ftc_data=ftc_data,
                         accuracy_buckets=accuracy_buckets,
                         winners=winner_profiles,
                         seasons=AVAILABLE_SEASONS,
                         season_names=SEASON_NAMES)


# --- GLOBAL SEARCH & API ---

@app.route('/compare-seasons')
def compare_seasons():
    """Compare two seasons side-by-side"""
    season_stats = []
    for s in AVAILABLE_SEASONS:
        sd = seasons_data[s]
        castaways = sd['voting']['castaways']
        challenges = sd['challenges']['challenges']
        advantages = sd['advantages'].get('advantages', [])
        tcs = sd['tribal_councils']
        winner = next((p for p in winner_profiles if p['season'] == s), None)

        # Calculate aggregate stats
        total_votes_cast = sum(len(c.get('voting_history', [])) for c in castaways)
        avg_drama = round(sum(tc.get('drama_score', 5) for tc in tcs) / max(len(tcs), 1), 1)
        idols_played = sum(1 for a in advantages if a.get('day_played') or a.get('played_day'))
        votes_negated = sum(a.get('votes_negated', 0) for a in advantages)

        season_stats.append({
            'season': s,
            'name': SEASON_NAMES[s],
            'castaway_count': len(castaways),
            'challenge_count': len(challenges),
            'tribal_count': len(tcs),
            'advantage_count': len(advantages),
            'idols_played': idols_played,
            'votes_negated': votes_negated,
            'avg_drama': avg_drama,
            'total_votes_cast': total_votes_cast,
            'winner': winner['name'] if winner else 'Unknown',
            'winner_archetype': winner.get('archetype', {}) if winner else {},
            'winner_stats': winner.get('stats', {}) if winner else {},
            'filming_location': SEASON_SUMMARIES.get(s, {}).get('filming_location', ''),
            'tagline': SEASON_SUMMARIES.get(s, {}).get('tagline', ''),
        })

    return render_template('compare_seasons.html',
                         season_stats=season_stats,
                         seasons=AVAILABLE_SEASONS,
                         season_names=SEASON_NAMES)


# Season recommendations — similar seasons based on shared traits
SEASON_RECOMMENDATIONS = {
    1: [3, 2, 9],     # Early social games
    2: [1, 3, 10],    # Classic survival
    3: [1, 2, 11],    # African adventure, early era
    4: [13, 31, 33],  # Power shifts, strategic evolution
    5: [24, 22, 21],  # Dominant winners
    6: [15, 28, 37],  # Strategic gameplay
    7: [16, 20, 28],  # Iconic characters, big moves
    8: [20, 31, 34],  # All-Stars returnee seasons
    9: [18, 25, 11],  # Underdog stories
    10: [35, 30, 22], # Dominant tribe, immunity runs
    11: [25, 18, 9],  # Under-the-radar winners
    12: [13, 7, 28],  # Idol gameplay beginnings
    13: [31, 7, 4],   # Underdog tribe comeback
    14: [15, 24, 33], # Strategic dominance
    15: [28, 6, 37],  # Strategic masterclasses
    16: [20, 7, 31],  # All-time great gameplay
    17: [21, 30, 39], # Chaotic, unpredictable
    18: [3, 25, 37],  # Likable winners, social games
    19: [28, 20, 35], # Aggressive idol play
    20: [16, 8, 31],  # All-Stars, legendary moves
    21: [17, 30, 39], # Underestimated winners
    22: [5, 24, 23],  # Dominant winners
    23: [22, 27, 8],  # Returning player dynamics
    24: [5, 22, 26],  # Dominant winner control
    25: [9, 18, 37],  # Underdog comebacks
    26: [8, 31, 34],  # Returnee seasons, strategic
    27: [29, 20, 23], # Blood vs Water family dynamics
    28: [15, 37, 20], # Elite strategic play
    29: [27, 37, 33], # Blood vs Water, revenge arcs
    30: [10, 35, 19], # Immunity runs
    31: [20, 16, 28], # All-Stars strategic depth
    32: [25, 18, 37], # Underdog winners
    33: [37, 29, 31], # Modern strategic gameplay
    34: [8, 20, 31],  # Game Changers, returnees
    35: [30, 19, 36], # Idol-heavy, twists
    36: [35, 34, 33], # Ghost Island, advantage era
    37: [28, 15, 33], # Elite strategic play, David vs Goliath
    38: [22, 23, 34], # Controversial twists
    39: [17, 38, 35], # Controversial seasons
}


@app.route('/alliances')
def alliances():
    """Alliance tracking and voting bloc network diagrams"""
    season = get_season_param()
    sd = seasons_data[season]
    castaways = sd['voting']['castaways']
    tcs = sd['tribal_councils']

    # Build vote map: tc_number -> {voter_name: target}
    tc_vote_map = {}
    for castaway in castaways:
        for vote in castaway.get('voting_history', []):
            tc_num = vote.get('tribal_council', vote.get('tc', 0))
            if tc_num == 0:
                continue
            target = vote.get('voted_for', vote.get('vote', ''))
            if target:
                tc_vote_map.setdefault(tc_num, {})[castaway['name']] = target

    # Count co-votes (same target at same tribal council)
    co_votes = {}
    shared_tcs = {}
    for tc_num, voters in tc_vote_map.items():
        voter_list = list(voters.items())
        for i in range(len(voter_list)):
            for j in range(i + 1, len(voter_list)):
                name_a, target_a = voter_list[i]
                name_b, target_b = voter_list[j]
                pair = tuple(sorted([name_a, name_b]))
                shared_tcs[pair] = shared_tcs.get(pair, 0) + 1
                if target_a == target_b:
                    co_votes[pair] = co_votes.get(pair, 0) + 1

    # Build node data
    tribe_set = set()
    nodes = []
    for c in castaways:
        tribe = c.get('original_tribe', 'Unknown')
        tribe_set.add(tribe)
        nodes.append({
            'name': c['name'],
            'tribe': tribe,
            'placement': c.get('placement', ''),
            'is_winner': c.get('placement') == 'Winner',
        })

    # Build edges
    edges = []
    for pair, count in co_votes.items():
        total = shared_tcs.get(pair, 1)
        rate = round(count / total * 100, 1) if total > 0 else 0
        if count >= 2:
            edges.append({
                'source': pair[0],
                'target': pair[1],
                'co_votes': count,
                'total_shared': total,
                'rate': rate,
            })
    edges.sort(key=lambda x: -x['co_votes'])

    # Top voting pairs
    top_pairs = edges[:25]

    # Detect voting blocs: groups of 3+ players who all co-voted frequently
    strong_threshold = max(3, len(tcs) // 4) if tcs else 3
    blocs = []
    strong_pairs = {pair: count for pair, count in co_votes.items() if count >= strong_threshold}
    # Build adjacency from strong pairs
    adj = {}
    for (a, b), count in strong_pairs.items():
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    # Find cliques (groups where everyone is connected)
    visited_blocs = set()
    for player in adj:
        neighbors = adj[player]
        for n in neighbors:
            common = neighbors & adj.get(n, set())
            bloc = frozenset({player, n} | common)
            if len(bloc) >= 3 and bloc not in visited_blocs:
                # Verify it's a real clique (all pairs connected)
                bloc_list = list(bloc)
                is_clique = True
                for ii in range(len(bloc_list)):
                    for jj in range(ii + 1, len(bloc_list)):
                        if bloc_list[jj] not in adj.get(bloc_list[ii], set()):
                            is_clique = False
                            break
                    if not is_clique:
                        break
                if is_clique:
                    visited_blocs.add(bloc)
                    avg_strength = sum(co_votes.get(tuple(sorted([bloc_list[ii], bloc_list[jj]])), 0)
                                       for ii in range(len(bloc_list))
                                       for jj in range(ii + 1, len(bloc_list))) / max(1, len(bloc_list) * (len(bloc_list) - 1) // 2)
                    blocs.append({
                        'members': sorted(bloc_list),
                        'size': len(bloc_list),
                        'avg_strength': round(avg_strength, 1),
                    })
    blocs.sort(key=lambda x: (-x['size'], -x['avg_strength']))

    # Tribe colors
    tribes = sorted(tribe_set)

    return render_template('alliances.html',
        nodes=nodes,
        edges=edges[:60],
        top_pairs=top_pairs,
        blocs=blocs[:10],
        tribes=tribes,
        season=season,
        season_name=SEASON_NAMES[season],
        seasons=AVAILABLE_SEASONS,
        season_names=SEASON_NAMES)


@app.route('/power-rankings')
def power_rankings():
    """Episode-by-episode power ranking timeline"""
    season = get_season_param()
    sd = seasons_data[season]
    castaways = sd['voting']['castaways']
    tcs = sd['tribal_councils']
    challenges = sd['challenges']['challenges']

    # Build per-player timeline: at each tribal council, compute a "power score"
    # Power score factors: votes received (penalty), challenge wins (bonus), voting accuracy (bonus)

    # Build map of tc_num -> eliminated person
    eliminated_at = {}
    for tc in tcs:
        eliminated_at[tc['number']] = tc.get('eliminated', '')

    # Build map of tc_num -> who voted for whom
    tc_votes_received = {}  # tc_num -> {target: count}
    tc_vote_map = {}
    for c in castaways:
        for vote in c.get('voting_history', []):
            tc_num = vote.get('tribal_council', vote.get('tc', 0))
            if tc_num == 0:
                continue
            target = vote.get('voted_for', '')
            if target:
                tc_votes_received.setdefault(tc_num, {})
                tc_votes_received[tc_num][target] = tc_votes_received[tc_num].get(target, 0) + 1
                tc_vote_map.setdefault(tc_num, {})[c['name']] = target

    # Challenge wins per player up to each point
    challenge_wins_by_tc = {}  # player -> cumulative wins at each tc
    challenge_list = sorted(challenges, key=lambda c: c.get('episode', c.get('day', 0)))
    tc_days = {tc['number']: tc.get('day', 0) for tc in tcs}

    sorted_tc_nums = sorted(tc_votes_received.keys())
    if not sorted_tc_nums:
        sorted_tc_nums = sorted(tc['number'] for tc in tcs) if tcs else []

    # Track cumulative challenge wins per player
    cumulative_wins = {}
    challenge_idx = 0

    # Build power scores for each player at each TC
    player_timelines = {}
    eliminated_players = set()

    for tc_num in sorted_tc_nums:
        tc_day = tc_days.get(tc_num, 0)

        # Count challenge wins up to this day
        while challenge_idx < len(challenge_list):
            ch = challenge_list[challenge_idx]
            ch_day = ch.get('day', ch.get('episode', 0)) or 0
            if ch_day > tc_day and tc_day > 0:
                break
            for winner in ch.get('winners', []):
                cumulative_wins[winner] = cumulative_wins.get(winner, 0) + 1
            challenge_idx += 1

        votes_at_tc = tc_votes_received.get(tc_num, {})
        votes_cast = tc_vote_map.get(tc_num, {})
        eliminated = eliminated_at.get(tc_num, '')

        for c in castaways:
            name = c['name']
            if name in eliminated_players:
                continue

            # Power score components
            votes_received = votes_at_tc.get(name, 0)
            ch_wins = cumulative_wins.get(name, 0)
            voted_correctly = 1 if (name in votes_cast and votes_cast[name] == eliminated) else 0

            # Power score: higher = more powerful
            score = 50  # base
            score -= votes_received * 8  # penalty for receiving votes
            score += ch_wins * 5  # bonus for challenge wins
            score += voted_correctly * 3  # bonus for correct vote
            score = max(5, min(100, score))

            player_timelines.setdefault(name, []).append({
                'tc': tc_num,
                'score': score,
                'votes_received': votes_received,
                'voted_correctly': voted_correctly,
            })

        if eliminated:
            eliminated_players.add(eliminated)

    # Sort players by final power score (or placement)
    placement_order = {}
    for c in castaways:
        p = c.get('placement', '')
        if p == 'Winner':
            placement_order[c['name']] = 0
        elif 'Runner' in p:
            placement_order[c['name']] = 1
        else:
            match = re.match(r'(\d+)', p)
            placement_order[c['name']] = int(match.group(1)) if match else 99

    sorted_players = sorted(player_timelines.keys(), key=lambda n: placement_order.get(n, 99))

    # Build chart-ready data
    timeline_data = []
    for name in sorted_players:
        tribe = next((c.get('original_tribe', 'Unknown') for c in castaways if c['name'] == name), 'Unknown')
        placement = next((c.get('placement', '') for c in castaways if c['name'] == name), '')
        timeline_data.append({
            'name': name,
            'tribe': tribe,
            'placement': placement,
            'is_winner': placement == 'Winner',
            'data': player_timelines[name],
        })

    return render_template('power_rankings.html',
        timeline_data=timeline_data,
        tc_labels=['TC' + str(tc) for tc in sorted_tc_nums],
        season=season,
        season_name=SEASON_NAMES[season],
        seasons=AVAILABLE_SEASONS,
        season_names=SEASON_NAMES)


@app.route('/api/season-recommendations/<int:season>')
def season_recommendations(season):
    """Get season recommendations based on similar seasons"""
    if season not in SEASON_RECOMMENDATIONS:
        return jsonify([])
    recs = []
    for rec_season in SEASON_RECOMMENDATIONS[season]:
        summary = SEASON_SUMMARIES.get(rec_season, {})
        recs.append({
            'season': rec_season,
            'name': SEASON_NAMES.get(rec_season, ''),
            'tagline': summary.get('tagline', ''),
            'theme': summary.get('theme', ''),
        })
    return jsonify(recs)


@app.route('/api/search')
def global_search():
    """Search across all castaways in all seasons"""
    query = request.args.get('q', '').lower().strip()
    if not query or len(query) < 2:
        return jsonify([])

    results = []
    for season_num, season_data in seasons_data.items():
        for castaway in season_data['voting']['castaways']:
            if query in castaway['name'].lower():
                results.append({
                    'name': castaway['name'],
                    'season': season_num,
                    'season_name': SEASON_NAMES[season_num],
                    'placement': castaway.get('placement', 'Unknown'),
                    'url': f'/castaways?season={season_num}'
                })
    return jsonify(results[:20])


@app.route('/api/random-quote')
def random_quote():
    """Return a random famous Survivor quote"""
    if not famous_quotes:
        return jsonify({'error': 'No quotes available'}), 404
    quote = random.choice(famous_quotes)
    return jsonify(quote)


@app.route('/api/random-player')
def random_player():
    """Return a random castaway from any season"""
    season_num = random.choice(AVAILABLE_SEASONS)
    castaways = seasons_data[season_num]['voting']['castaways']
    if not castaways:
        return jsonify({'error': 'No castaways found'}), 404
    castaway = random.choice(castaways)
    return jsonify({
        'name': castaway['name'],
        'season': season_num,
        'season_name': SEASON_NAMES[season_num],
        'placement': castaway.get('placement', 'Unknown'),
        'url': f'/castaways?season={season_num}'
    })


@app.route('/idol-strategy')
def idol_strategy():
    """Idol Strategy analysis — comprehensive cross-season idol usage analysis"""
    all_idols = []
    for s in AVAILABLE_SEASONS:
        sd = seasons_data[s]
        for adv in sd['advantages'].get('advantages', []):
            idol = adv.copy()
            idol['season'] = s
            idol['season_name'] = SEASON_NAMES[s]
            all_idols.append(idol)

    # Filter to idol-type items only (exclude Extra Vote, Vote Steal, etc.)
    idol_types = {'Hidden Immunity Idol', 'Hidden Immunity Idol with Special Powers (Tyler Perry Idol)',
                  'Super Idol', 'Super Idol (transferred)', 'Hidden Immunity Idol (God Idol)',
                  'Hidden Immunity Idol (split idol - two halves)',
                  'Hidden Immunity Idol (held by Stephen)',
                  'Hidden Immunity Idol (J.T.\'s idol, given to Russell)',
                  'Hidden Immunity Idol (Island of the Idols - temporary)',
                  'Legacy Advantage', 'Legacy Advantage (transferred)',
                  'Fake Hidden Immunity Idol'}
    idols_only = [i for i in all_idols if i.get('type', '') in idol_types
                  or 'Immunity Idol' in i.get('type', '')
                  or 'Super Idol' in i.get('type', '')
                  or 'Legacy Advantage' in i.get('type', '')]
    non_idol_advantages = [i for i in all_idols if i not in idols_only]

    # Separate real idols from fakes
    fake_idols = [i for i in idols_only if 'Fake' in i.get('type', '')]
    real_idols = [i for i in idols_only if 'Fake' not in i.get('type', '')]

    # Classify God/Super Idols early — these have fundamentally different strategy
    # (played AFTER votes read) so they get their own type and are excluded from strategy analysis
    def is_god_idol(idol):
        t = idol.get('type', '')
        return ('God Idol' in t or 'Tyler Perry' in t or 'Special Powers' in t or 'Super Idol' in t)

    standard_idols = [i for i in real_idols if not is_god_idol(i)]

    # === CORE STATS (all idols) ===
    played = [i for i in real_idols if i.get('day_played')]
    not_played = [i for i in real_idols if not i.get('day_played')]
    successful = [i for i in played if i.get('result') == 'successful']
    unsuccessful = [i for i in played if i.get('result') == 'unsuccessful']
    voted_out_holding = [i for i in real_idols if i.get('voted_out_holding')]

    total_votes_negated = sum(i.get('votes_negated', 0) for i in real_idols)

    # === STRATEGY STATS (standard idols only — excludes God/Super Idols) ===
    std_played = [i for i in standard_idols if i.get('day_played')]

    # Self vs. other plays (standard idols only)
    self_plays = [i for i in std_played if i.get('played_on') == i.get('found_by')]
    ally_plays = [i for i in std_played if i.get('played_on') and i.get('played_on') != i.get('found_by')]
    self_successful = [i for i in self_plays if i.get('result') == 'successful']
    ally_successful = [i for i in ally_plays if i.get('result') == 'successful']

    # Holding duration (standard idols only)
    durations = []
    for i in std_played:
        df = i.get('day_found') or 0
        dp = i.get('day_played') or 0
        if df > 0 and dp > 0:
            durations.append({'days': dp - df, 'player': i.get('found_by', ''), 'season': i['season'],
                              'season_name': i['season_name'], 'result': i.get('result', '')})
    durations.sort(key=lambda x: -x['days'])

    # Duration buckets for chart
    duration_buckets = {'Same day': 0, '1-3 days': 0, '4-7 days': 0, '8-14 days': 0, '15-21 days': 0, '22+ days': 0}
    for d in durations:
        days = d['days']
        if days == 0:
            duration_buckets['Same day'] += 1
        elif days <= 3:
            duration_buckets['1-3 days'] += 1
        elif days <= 7:
            duration_buckets['4-7 days'] += 1
        elif days <= 14:
            duration_buckets['8-14 days'] += 1
        elif days <= 21:
            duration_buckets['15-21 days'] += 1
        else:
            duration_buckets['22+ days'] += 1

    # Top idol finders
    finders = {}
    for i in real_idols:
        name = i.get('found_by', '')
        if name:
            if name not in finders:
                finders[name] = {'name': name, 'found': 0, 'played': 0, 'successful': 0,
                                 'votes_negated': 0, 'seasons': set()}
            finders[name]['found'] += 1
            finders[name]['seasons'].add(i['season'])
            if i.get('day_played'):
                finders[name]['played'] += 1
                if i.get('result') == 'successful':
                    finders[name]['successful'] += 1
            finders[name]['votes_negated'] += i.get('votes_negated', 0)
    # Convert sets to lists for template
    for f in finders.values():
        f['seasons'] = sorted(f['seasons'])
        f['season_count'] = len(f['seasons'])
    top_finders = sorted(finders.values(), key=lambda x: -x['found'])[:15]

    # Most votes negated single play
    top_negations = sorted(
        [i for i in played if i.get('votes_negated', 0) > 0],
        key=lambda x: -x.get('votes_negated', 0)
    )[:10]

    # Per-season idol stats for chart
    season_idol_stats = []
    for s in AVAILABLE_SEASONS:
        sd = seasons_data[s]
        advs = sd['advantages'].get('advantages', [])
        season_real = [a for a in advs if 'Immunity Idol' in a.get('type', '')
                       or 'Super Idol' in a.get('type', '')
                       or 'Legacy Advantage' in a.get('type', '')]
        season_real = [a for a in season_real if 'Fake' not in a.get('type', '')]
        season_played = [a for a in season_real if a.get('day_played')]
        season_successful = [a for a in season_played if a.get('result') == 'successful']
        season_idol_stats.append({
            'season': s,
            'name': SEASON_NAMES[s],
            'found': len(season_real),
            'played': len(season_played),
            'successful': len(season_successful),
            'votes_negated': sum(a.get('votes_negated', 0) for a in season_real),
            'voted_out_holding': sum(1 for a in season_real if a.get('voted_out_holding')),
        })

    # Idol types catalog
    type_catalog = {}
    for i in real_idols:
        t = i.get('type', 'Unknown')
        # Normalize type names — God Idol is its own category
        if is_god_idol(i):
            norm = 'God Idol (Post-Vote Read)'
        elif 'split idol' in t.lower():
            norm = 'Split Idol (Two Halves)'
        elif 'Legacy Advantage' in t:
            norm = 'Legacy Advantage'
        elif 'temporary' in t.lower() or 'Island of the Idols' in t:
            norm = 'Temporary Idol'
        elif t == 'Hidden Immunity Idol':
            norm = 'Standard Hidden Immunity Idol'
        else:
            norm = 'Standard Hidden Immunity Idol'
        if norm not in type_catalog:
            type_catalog[norm] = {'name': norm, 'count': 0, 'seasons': set(), 'played': 0, 'successful': 0}
        type_catalog[norm]['count'] += 1
        type_catalog[norm]['seasons'].add(i['season'])
        if i.get('day_played'):
            type_catalog[norm]['played'] += 1
            if i.get('result') == 'successful':
                type_catalog[norm]['successful'] += 1
    for tc in type_catalog.values():
        tc['seasons'] = sorted(tc['seasons'])

    # Notable plays data (best and worst)
    best_plays = [
        {'rank': 1, 'player': 'Parvati Shallow', 'season': 20, 'season_name': 'Heroes vs. Villains',
         'description': 'Double idol play — played idols on Jerri (5 votes negated) and Sandra, eliminating J.T. in the greatest strategic move in Survivor history.',
         'votes_negated': 5, 'target': 'Jerri Manthey & Sandra', 'category': 'Played on Ally'},
        {'rank': 2, 'player': 'Kelley Wentworth', 'season': 31, 'season_name': 'Cambodia',
         'description': 'Negated all-time record 9 votes, blindsiding Andrew Savage. Grabbed idol during an immunity challenge — nobody knew she had it.',
         'votes_negated': 9, 'target': 'Self', 'category': 'Secret Play'},
        {'rank': 3, 'player': 'Russell Hantz', 'season': 19, 'season_name': 'Samoa',
         'description': 'Negated 7 votes when Foa Foa was outnumbered 8-4. Found idol without clues — revolutionary. Cracked the Galu majority.',
         'votes_negated': 7, 'target': 'Self', 'category': 'Underdog Save'},
        {'rank': 4, 'player': 'Davie Rickenbacker', 'season': 37, 'season_name': 'David vs. Goliath',
         'description': 'Saved Christian Hubicki at the merge by negating 7 votes. Blindsided John Hennigan. Part of an epic triple-advantage sequence.',
         'votes_negated': 7, 'target': 'Christian Hubicki', 'category': 'Played on Ally'},
        {'rank': 5, 'player': 'Ben Driebergen', 'season': 35, 'season_name': 'Heroes vs. Healers vs. Hustlers',
         'description': 'Three consecutive idol plays (6+4+3 = 13 votes negated). Only player to survive 3 straight tribals as primary target via idol alone.',
         'votes_negated': 13, 'target': 'Self (x3)', 'category': 'Consecutive Saves'},
        {'rank': 6, 'player': 'Natalie Anderson', 'season': 29, 'season_name': 'San Juan del Sur',
         'description': '"Jaclyn, did you vote for who I told you to vote for?" Played on ally at F5, blindsided Baylor. First to play on ally AND win.',
         'votes_negated': 3, 'target': 'Jaclyn Schultz', 'category': 'Played on Ally'},
        {'rank': 7, 'player': 'Jenn Brown', 'season': 30, 'season_name': 'Worlds Apart',
         'description': 'Perfect read at the merge — negated 7 votes. No Collar alliance was outnumbered but survived. Cleanest self-save idol play ever.',
         'votes_negated': 7, 'target': 'Self', 'category': 'Perfect Read'},
        {'rank': 8, 'player': 'Carolyn Rivera', 'season': 30, 'season_name': 'Worlds Apart',
         'description': 'Kept idol secret for 33 days — one of the longest holds. Negated 5 votes including Dan\'s Extra Vote. Patient mastery.',
         'votes_negated': 5, 'target': 'Self', 'category': 'Long Hold'},
        {'rank': 9, 'player': 'Jeremy Collins', 'season': 31, 'season_name': 'Cambodia',
         'description': 'Played idol on ally Stephen Fishbach to maintain meat shield strategy. Later played second idol on himself at F6.',
         'votes_negated': 4, 'target': 'Stephen Fishbach', 'category': 'Played on Ally'},
        {'rank': 10, 'player': 'David Wright', 'season': 33, 'season_name': 'Millennials vs. Gen X',
         'description': 'Saved Jessica Lewis at a pre-merge tribal, negating 5 votes and blindsiding Lucy Huang. Playing for an ally this early was extremely bold and cemented his alliance for the rest of the game.',
         'votes_negated': 5, 'target': 'Jessica Lewis', 'category': 'Played on Ally'},
    ]

    worst_plays = [
        {'rank': 1, 'player': 'James Clement', 'season': 15, 'season_name': 'China',
         'description': 'Blindsided holding TWO idols. First player to hold two simultaneously. Overconfident in the majority alliance.',
         'type': 'Voted Out Holding'},
        {'rank': 2, 'player': 'J.T. Thomas', 'season': 20, 'season_name': 'Heroes vs. Villains',
         'description': 'Gave his idol to Russell Hantz believing the Villains had an all-female alliance. The idol was used against him. "Worst move in Survivor history."',
         'type': 'Gave to Enemy'},
        {'rank': 3, 'player': 'Ozzy Lusth', 'season': 16, 'season_name': 'Micronesia',
         'description': 'Blindsided 5-4 by the Black Widow Brigade with idol in pocket. Made a fake (the famous "stick") but never played the real one.',
         'type': 'Voted Out Holding'},
        {'rank': 4, 'player': 'Garrett Adelstein', 'season': 28, 'season_name': 'Cagayan',
         'description': 'Found idol Day 1, voted out Day 6 — LEFT THE IDOL AT CAMP. Earliest elimination while possessing an idol.',
         'type': 'Left at Camp'},
        {'rank': 5, 'player': 'J.T. Thomas', 'season': 34, 'season_name': 'Game Changers',
         'description': 'Found an idol at Nuku camp but left it behind when going to tribal. Blindsided by Sandra. Two seasons, two catastrophic idol failures.',
         'type': 'Left at Camp'},
        {'rank': 6, 'player': 'Tony & LJ', 'season': 28, 'season_name': 'Cagayan',
         'description': 'Played idols on EACH OTHER at the merge tribal — neither received any votes. Two idols wasted simultaneously for zero votes negated.',
         'type': 'Double Waste'},
        {'rank': 7, 'player': 'Jason Siska', 'season': 16, 'season_name': 'Micronesia',
         'description': 'Already fooled by Ozzy\'s fake idol stick, then found the REAL re-hidden idol and STILL didn\'t play it. Blindsided by Black Widow Brigade.',
         'type': 'Voted Out Holding'},
        {'rank': 8, 'player': 'Lauren O\'Connell', 'season': 38, 'season_name': 'Edge of Extinction',
         'description': 'Held idol 30 days, then was manipulated into playing it on Chris Underwood (back 1 day from Edge). Voted out next tribal. Chris won the season.',
         'type': 'Manipulated'},
    ]

    # Strategy dimension data
    strategy_self_rate = round(len(self_successful) / max(len(self_plays), 1) * 100, 1)
    strategy_ally_rate = round(len(ally_successful) / max(len(ally_plays), 1) * 100, 1)
    avg_duration = round(sum(d['days'] for d in durations) / max(len(durations), 1), 1) if durations else 0

    return render_template('idol_strategy.html',
                         # Core stats
                         total_real_idols=len(real_idols),
                         total_played=len(played),
                         total_successful=len(successful),
                         total_unsuccessful=len(unsuccessful),
                         total_not_played=len(not_played),
                         total_voted_out_holding=len(voted_out_holding),
                         total_votes_negated=total_votes_negated,
                         success_rate=round(len(successful) / max(len(played), 1) * 100, 1),
                         # Self vs ally
                         self_plays_count=len(self_plays),
                         ally_plays_count=len(ally_plays),
                         self_success_rate=strategy_self_rate,
                         ally_success_rate=strategy_ally_rate,
                         self_successful_count=len(self_successful),
                         ally_successful_count=len(ally_successful),
                         # Duration
                         avg_duration=avg_duration,
                         duration_buckets=duration_buckets,
                         longest_holds=durations[:8],
                         # Top finders
                         top_finders=top_finders,
                         # Top negations
                         top_negations=top_negations,
                         # Per-season stats
                         season_idol_stats=season_idol_stats,
                         # Type catalog
                         type_catalog=sorted(type_catalog.values(), key=lambda x: -x['count']),
                         # Notable plays
                         best_plays=best_plays,
                         worst_plays=worst_plays,
                         # Fake idols
                         fake_idols=fake_idols,
                         # Non-idol advantages count
                         non_idol_count=len(non_idol_advantages),
                         # All idols for detailed exploration
                         all_idols=real_idols,
                         # Standard template vars
                         seasons=AVAILABLE_SEASONS,
                         season_names=SEASON_NAMES)


@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 page"""
    return render_template('404.html',
                         seasons=AVAILABLE_SEASONS,
                         season_names=SEASON_NAMES), 404


@app.errorhandler(500)
def internal_error(e):
    """Custom 500 page"""
    return render_template('500.html',
                         seasons=AVAILABLE_SEASONS,
                         season_names=SEASON_NAMES), 500


if __name__ == '__main__':
    app.run(debug=True, port=8000)
