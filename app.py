from flask import Flask, render_template, jsonify, request
from collections import Counter
import json

app = Flask(__name__)

# Available seasons
AVAILABLE_SEASONS = [28, 29, 30]
SEASON_NAMES = {
    28: "Cagayan",
    29: "San Juan del Sur",
    30: "Worlds Apart"
}

# Load data for all seasons
def load_season_data(season_num):
    """Load all data files for a specific season"""
    data = {}

    # Voting data (Season 28 uses different filename)
    voting_file = 'data/voting_data.json' if season_num == 28 else f'data/season{season_num}_voting.json'
    with open(voting_file, 'r') as f:
        data['voting'] = json.load(f)

    # Challenges
    with open(f'data/season{season_num}_challenges.json', 'r') as f:
        data['challenges'] = json.load(f)

    # Advantages/Idols
    with open(f'data/season{season_num}_advantages_idols.json', 'r') as f:
        data['advantages'] = json.load(f)

    # Timeline
    with open(f'data/season{season_num}_timeline.json', 'r') as f:
        data['timeline'] = json.load(f)

    # Headshots
    with open(f'data/season{season_num}_headshots.json', 'r') as f:
        data['headshots'] = json.load(f)

    # Challenge photos
    with open(f'data/season{season_num}_challenge_photos.json', 'r') as f:
        data['challenge_photos'] = json.load(f)

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

    correct_votes = 0
    total_votes = len(castaway['voting_history'])

    # Build elimination map
    elimination_map = {}
    for episode in voting_data['episodes']:
        for tc in episode['tribal_councils']:
            elimination_map[tc['number']] = tc['eliminated']

    for vote in castaway['voting_history']:
        tc_num = vote['tc']
        if tc_num in elimination_map and vote['voted_for'] == elimination_map[tc_num]:
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

    # Calculate grades for all tribal councils
    all_tribal_councils = []
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

@app.route('/')
def index():
    """Landing page with season selector"""
    return render_template('index.html',
                         seasons=AVAILABLE_SEASONS,
                         season_names=SEASON_NAMES)

@app.route('/tribal-councils')
def tribal_councils():
    """Scrollable tribal councils view"""
    season = int(request.args.get('season', 28))
    if season not in AVAILABLE_SEASONS:
        season = 28

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
    season = int(request.args.get('season', 28))
    if season not in AVAILABLE_SEASONS:
        season = 28

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
    season = int(request.args.get('season', 28))
    if season not in AVAILABLE_SEASONS:
        season = 28

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
    season = int(request.args.get('season', 28))
    if season not in AVAILABLE_SEASONS:
        season = 28

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
    season = int(request.args.get('season', 28))
    if season not in AVAILABLE_SEASONS:
        season = 28

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
        return ('Season not found', 404)

    season_data = seasons_data[season]
    episode = next((e for e in season_data['voting']['episodes'] if e['number'] == episode_num), None)
    return jsonify(episode) if episode else ('Episode not found', 404)

@app.route('/api/castaway/<int:season>/<name>')
def get_castaway(season, name):
    """API endpoint for castaway data"""
    if season not in AVAILABLE_SEASONS:
        return ('Season not found', 404)

    season_data = seasons_data[season]
    castaway = next((c for c in season_data['voting']['castaways'] if c['name'].lower() == name.lower()), None)
    return jsonify(castaway) if castaway else ('Castaway not found', 404)

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

if __name__ == '__main__':
    app.run(debug=True, port=8000)
