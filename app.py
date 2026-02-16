from flask import Flask, render_template, jsonify, request
from collections import Counter
import json
import os

app = Flask(__name__)

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

# Load all seasons at startup
seasons_data = {}
for season in AVAILABLE_SEASONS:
    seasons_data[season] = load_season_data(season)

# Helper functions
def calculate_voting_accuracy(castaway_name, voting_data):
    """Calculate voting accuracy for a castaway"""
    castaway = next((c for c in voting_data['castaways'] if c['name'] == castaway_name), None)
    if not castaway or not castaway.get('voting_history'):
        return {'correct': 0, 'total': 0, 'accuracy': 0}

    # Check if we have detailed episode data (old format)
    if 'episodes' not in voting_data:
        # New format doesn't have detailed vote breakdowns yet
        # Return placeholder until we build full tribal council data
        total_votes = len(castaway['voting_history'])
        return {'correct': 0, 'total': total_votes, 'accuracy': 0}

    correct_votes = 0
    total_votes = len(castaway['voting_history'])

    # Build elimination map
    elimination_map = {}
    for episode in voting_data['episodes']:
        for tc in episode['tribal_councils']:
            elimination_map[tc['number']] = tc['eliminated']

    for vote in castaway['voting_history']:
        tc_num = vote.get('tc', vote.get('tribal_council', 0))
        voted_for = vote.get('voted_for', vote.get('vote', ''))
        if tc_num in elimination_map and voted_for == elimination_map[tc_num]:
            correct_votes += 1

    accuracy = round((correct_votes / total_votes * 100), 1) if total_votes > 0 else 0
    return {'correct': correct_votes, 'total': total_votes, 'accuracy': accuracy}

def calculate_challenge_beast_metrics(castaway_name, challenge_data):
    """Calculate challenge wins for a castaway"""
    immunity_wins = 0
    reward_wins = 0

    for challenge in challenge_data['challenges']:
        if castaway_name in challenge.get('winners', []):
            if 'Immunity' in challenge['challenge_type']:
                immunity_wins += 1
            if 'Reward' in challenge['challenge_type'] and challenge['challenge_type'] != 'Immunity':
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

# Enrich data for all seasons
for season_num, season_data in seasons_data.items():
    voting_data = season_data['voting']
    challenge_data = season_data['challenges']
    advantages_data = season_data['advantages']

    # Add headshot URLs to castaways
    for castaway in voting_data['castaways']:
        castaway['voting_accuracy'] = calculate_voting_accuracy(castaway['name'], voting_data)
        castaway['challenge_stats'] = calculate_challenge_beast_metrics(castaway['name'], challenge_data)
        castaway['headshot'] = season_data['headshots'].get(castaway['name'], '')

    # Calculate grades for all tribal councils (if episodes data exists)
    all_tribal_councils = []
    if 'episodes' in voting_data:
        for episode in voting_data['episodes']:
            for tc in episode['tribal_councils']:
                tc['episode_number'] = episode['number']
                tc['drama_score'] = calculate_episode_grade(tc, advantages_data)
                tc['flame_rating'] = get_flame_rating(tc['drama_score'])
                all_tribal_councils.append(tc)

    # Store enriched tribal councils
    season_data['tribal_councils'] = all_tribal_councils

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
    return render_template('index.html',
                         seasons=AVAILABLE_SEASONS,
                         season_names=SEASON_NAMES,
                         total_castaways=total_castaways,
                         total_challenges=total_challenges,
                         winner_count=len(winner_profiles),
                         featured_winner=featured)

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
    """Hall of Fame - all-time records across all seasons"""

    # Calculate individual records
    all_castaways = []
    champions = []

    for season_num, season_data in seasons_data.items():
        voting_data = season_data['voting']
        challenge_data = season_data['challenges']
        advantages_data = season_data['advantages']

        for castaway in voting_data['castaways']:
            # Add season context
            castaway_record = castaway.copy()
            castaway_record['season'] = season_num
            castaway_record['season_name'] = SEASON_NAMES[season_num]

            # Track champions separately
            if castaway.get('placement') == 'Winner':
                champions.append(castaway_record)

            all_castaways.append(castaway_record)

    # Calculate individual records
    individual_records = {
        'highest_voting_accuracy_champion': max(champions, key=lambda c: c.get('voting_accuracy', {}).get('accuracy', 0)) if champions else None,
        'lowest_voting_accuracy_champion': min(champions, key=lambda c: c.get('voting_accuracy', {}).get('accuracy', 0)) if champions else None,
        'most_challenge_wins': max(all_castaways, key=lambda c: c.get('challenge_stats', {}).get('total_wins', 0)),
        'most_challenge_wins_champion': max(champions, key=lambda c: c.get('challenge_stats', {}).get('total_wins', 0)) if champions else None,
        'least_challenge_wins_champion': min(champions, key=lambda c: c.get('challenge_stats', {}).get('total_wins', 0)) if champions else None,
        'most_votes_received_champion': max(champions, key=lambda c: c.get('votes_against', 0)) if champions else None,
        'least_votes_received_champion': min(champions, key=lambda c: c.get('votes_against', 0)) if champions else None,
    }

    # Calculate idol/advantage records
    idol_records = []
    for season_num, season_data in seasons_data.items():
        advantages = season_data['advantages'].get('advantages', [])
        for adv in advantages:
            idol_records.append({
                **adv,
                'season': season_num,
                'season_name': SEASON_NAMES[season_num]
            })

    # Most votes nullified by a single idol
    most_votes_nullified = max(idol_records, key=lambda x: x.get('votes_negated', 0)) if idol_records else None

    # Most successful idol plays by a player
    successful_plays_by_player = Counter()
    for idol in idol_records:
        if idol.get('result') == 'successful':
            player = idol.get('found_by') or idol.get('played_for')
            if player:
                successful_plays_by_player[player] += 1

    most_successful_idol_player = max(successful_plays_by_player.items(), key=lambda x: x[1]) if successful_plays_by_player else (None, 0)

    # Most idols played in a season
    idols_by_season = Counter()
    items_by_season = Counter()
    for idol in idol_records:
        if idol.get('day_played'):
            idols_by_season[idol['season']] += 1
        items_by_season[idol['season']] += 1

    most_idols_played_season = max(idols_by_season.items(), key=lambda x: x[1]) if idols_by_season else (None, 0)
    most_items_season = max(items_by_season.items(), key=lambda x: x[1]) if items_by_season else (None, 0)

    # Season records
    season_records = {}
    for season_num, season_data in seasons_data.items():
        advantages = season_data['advantages'].get('advantages', [])
        voting_data = season_data['voting']

        votes_nullified = sum(adv.get('votes_negated', 0) for adv in advantages)
        voted_out_holding = sum(1 for adv in advantages if adv.get('voted_out_holding'))

        # Count unique players who received votes
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

    return render_template('hall_of_fame.html',
                         individual_records=individual_records,
                         most_votes_nullified=most_votes_nullified,
                         most_successful_idol_player=most_successful_idol_player,
                         most_idols_played_season=most_idols_played_season,
                         most_items_season=most_items_season,
                         season_records=season_records,
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

if __name__ == '__main__':
    app.run(debug=True, port=8000)
