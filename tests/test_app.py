"""Tests for Survivor Bot Flask application."""
import pytest
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import (
    app, calculate_voting_accuracy, calculate_challenge_beast_metrics,
    calculate_episode_grade, get_flame_rating, seasons_data,
    winner_profiles, AVAILABLE_SEASONS, SEASON_NAMES
)


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# --- Helper Function Tests ---

class TestVotingAccuracy:
    def test_known_data(self):
        voting_data = {
            'castaways': [{
                'name': 'TestPlayer',
                'voting_history': [
                    {'voted_for': 'Alice', 'tc': 1},
                    {'voted_for': 'Bob', 'tc': 2},
                    {'voted_for': 'Carol', 'tc': 3},
                ]
            }]
        }
        tcs = [
            {'number': 1, 'eliminated': 'Alice'},
            {'number': 2, 'eliminated': 'Bob'},
            {'number': 3, 'eliminated': 'Dave'},
        ]
        result = calculate_voting_accuracy('TestPlayer', voting_data, tribal_councils=tcs)
        assert result['correct'] == 2
        assert result['total'] == 3
        assert result['accuracy'] == 66.7

    def test_empty_voting_history(self):
        voting_data = {'castaways': [{'name': 'Empty', 'voting_history': []}]}
        result = calculate_voting_accuracy('Empty', voting_data)
        assert result['accuracy'] == 0

    def test_missing_castaway(self):
        voting_data = {'castaways': []}
        result = calculate_voting_accuracy('Nobody', voting_data)
        assert result['accuracy'] == 0

    def test_perfect_accuracy(self):
        voting_data = {
            'castaways': [{
                'name': 'Perfect',
                'voting_history': [
                    {'voted_for': 'A', 'tc': 1},
                    {'voted_for': 'B', 'tc': 2},
                ]
            }]
        }
        tcs = [{'number': 1, 'eliminated': 'A'}, {'number': 2, 'eliminated': 'B'}]
        result = calculate_voting_accuracy('Perfect', voting_data, tribal_councils=tcs)
        assert result['accuracy'] == 100.0


class TestChallengeMetrics:
    def test_basic_counting(self):
        data = {
            'challenges': [
                {'challenge_type': 'Immunity', 'outcome_type': 'Individual', 'winners': ['Alice', 'Bob']},
                {'challenge_type': 'Reward', 'outcome_type': 'Individual', 'winners': ['Alice']},
                {'challenge_type': 'Immunity and Reward', 'outcome_type': 'Individual', 'winners': ['Carol']},
            ]
        }
        result = calculate_challenge_beast_metrics('Alice', data)
        assert result['immunity_wins'] == 1
        assert result['reward_wins'] == 1
        assert result['total_wins'] == 2

    def test_excludes_team_wins(self):
        data = {
            'challenges': [
                {'challenge_type': 'Immunity', 'outcome_type': 'Tribal', 'winners': ['Alice', 'Bob', 'Carol']},
                {'challenge_type': 'Immunity', 'outcome_type': 'Individual', 'winners': ['Alice']},
                {'challenge_type': 'Reward', 'outcome_type': 'Team', 'winners': ['Alice', 'Bob']},
            ]
        }
        result = calculate_challenge_beast_metrics('Alice', data)
        assert result['immunity_wins'] == 1
        assert result['reward_wins'] == 0
        assert result['total_wins'] == 1

    def test_no_wins(self):
        data = {'challenges': [{'challenge_type': 'Immunity', 'outcome_type': 'Individual', 'winners': ['Bob']}]}
        result = calculate_challenge_beast_metrics('Alice', data)
        assert result['total_wins'] == 0

    def test_empty_challenges(self):
        data = {'challenges': []}
        result = calculate_challenge_beast_metrics('Alice', data)
        assert result['total_wins'] == 0


class TestEpisodeGrade:
    def test_base_score(self):
        tc = {'tribe': 'Brawn', 'votes': [], 'day': 3}
        adv_data = {'advantages': []}
        score = calculate_episode_grade(tc, adv_data)
        assert score == 5.0

    def test_merge_bonus(self):
        tc = {'tribe': 'Merged Tribe', 'votes': [], 'day': 20}
        adv_data = {'advantages': []}
        score = calculate_episode_grade(tc, adv_data)
        assert score == 7.0

    def test_close_vote_bonus(self):
        tc = {'tribe': 'Brawn', 'votes': [{'count': 4}, {'count': 3}], 'day': 5}
        adv_data = {'advantages': []}
        score = calculate_episode_grade(tc, adv_data)
        assert score == 6.0  # base 5 + close vote 1


class TestFlameRating:
    def test_low_score(self):
        result = get_flame_rating(3.0)
        assert result.count('\u25A0') == 3  # filled squares

    def test_half_flame(self):
        result = get_flame_rating(5.5)
        assert '\u25B2' in result  # triangle for half

    def test_max_score(self):
        result = get_flame_rating(10.0)
        assert result.count('\u25A0') == 10  # 10 filled squares


# --- Route Tests ---

class TestRoutes:
    def test_index(self, client):
        assert client.get('/').status_code == 200

    def test_quiz(self, client):
        assert client.get('/quiz').status_code == 200

    def test_returning_players(self, client):
        assert client.get('/returning-players').status_code == 200

    def test_advantages_timeline_removed(self, client):
        assert client.get('/advantages-timeline').status_code == 404

    def test_challenge_performance(self, client):
        assert client.get('/challenge-performance').status_code == 200

    def test_voting_patterns(self, client):
        assert client.get('/voting-patterns').status_code == 200

    def test_paths_to_victory(self, client):
        assert client.get('/paths-to-victory').status_code == 200

    def test_winners(self, client):
        assert client.get('/winners').status_code == 200

    def test_compare(self, client):
        assert client.get('/compare').status_code == 200

    def test_seasons(self, client):
        assert client.get('/seasons').status_code == 200

    def test_analytics_removed(self, client):
        assert client.get('/analytics').status_code == 404

    def test_hall_of_fame(self, client):
        assert client.get('/hall-of-fame').status_code == 200

    def test_tribal_councils_default(self, client):
        assert client.get('/tribal-councils').status_code == 200

    def test_tribal_councils_season(self, client):
        assert client.get('/tribal-councils?season=28').status_code == 200

    def test_castaways(self, client):
        assert client.get('/castaways?season=28').status_code == 200

    def test_challenges(self, client):
        assert client.get('/challenges?season=1').status_code == 200

    def test_events(self, client):
        assert client.get('/events?season=28').status_code == 200

    def test_items(self, client):
        assert client.get('/items?season=28').status_code == 200

    def test_invalid_season_defaults(self, client):
        resp = client.get('/castaways?season=999')
        assert resp.status_code == 200

    def test_non_numeric_season_defaults(self, client):
        resp = client.get('/castaways?season=abc')
        assert resp.status_code == 200

    def test_winner_profile(self, client):
        assert client.get('/winner/28').status_code == 200

    def test_winner_profile_404(self, client):
        assert client.get('/winner/999').status_code == 404

    def test_search_api(self, client):
        resp = client.get('/api/search?q=tony')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert isinstance(data, list)
        assert len(data) > 0

    def test_search_too_short(self, client):
        resp = client.get('/api/search?q=a')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert len(data) == 0

    def test_random_player_api(self, client):
        resp = client.get('/api/random-player')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert 'name' in data
        assert 'season' in data

    def test_castaway_api(self, client):
        resp = client.get('/api/castaway/28/Tony Vlachos')
        assert resp.status_code == 200

    def test_castaway_api_404(self, client):
        resp = client.get('/api/castaway/28/Nobody')
        assert resp.status_code == 404

    def test_compare_seasons(self, client):
        assert client.get('/compare-seasons').status_code == 200

    def test_season_recommendations_api(self, client):
        resp = client.get('/api/season-recommendations/28')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert isinstance(data, list)
        assert len(data) > 0

    def test_season_recommendations_invalid(self, client):
        resp = client.get('/api/season-recommendations/999')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert len(data) == 0

    # --- New Feature Routes ---

    def test_alliances_default(self, client):
        assert client.get('/alliances').status_code == 200

    def test_alliances_season(self, client):
        assert client.get('/alliances?season=20').status_code == 200

    def test_power_rankings_removed(self, client):
        assert client.get('/power-rankings').status_code == 404

    def test_power_rankings_season_removed(self, client):
        assert client.get('/power-rankings?season=7').status_code == 404

    def test_random_quote_api(self, client):
        resp = client.get('/api/random-quote')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert 'quote' in data
        assert 'speaker' in data

    def test_custom_404(self, client):
        resp = client.get('/this-page-does-not-exist')
        assert resp.status_code == 404
        assert b'TRIBE HAS SPOKEN' in resp.data

    def test_alliances_has_network_data(self, client):
        resp = client.get('/alliances?season=28')
        assert resp.status_code == 200
        assert b'Alliance Network' in resp.data
        assert b'Top Voting Pairs' in resp.data

    def test_idol_strategy_has_advantages_tab(self, client):
        resp = client.get('/idol-strategy')
        assert resp.status_code == 200
        assert b'Advantages Evolution' in resp.data

    def test_castaways_have_nicknames(self, client):
        resp = client.get('/castaways?season=28')
        assert resp.status_code == 200
        # Tony should have "The King of the Jungle" nickname
        assert b'The King of the Jungle' in resp.data

    def test_index_has_feature_cards(self, client):
        resp = client.get('/')
        assert resp.status_code == 200
        assert b'Alliance Networks' in resp.data
        assert b'Winners Hall' in resp.data
        assert b'Idol Strategy' in resp.data

    def test_idol_strategy_page(self, client):
        resp = client.get('/idol-strategy')
        assert resp.status_code == 200
        assert b'Idol Strategy Guide' in resp.data
        assert b'idolsPerSeasonChart' in resp.data

    def test_idol_strategy_has_best_plays(self, client):
        resp = client.get('/idol-strategy')
        assert resp.status_code == 200
        assert b'Parvati Shallow' in resp.data
        assert b'Kelley Wentworth' in resp.data

    def test_idol_strategy_has_conclusions(self, client):
        resp = client.get('/idol-strategy')
        assert resp.status_code == 200
        assert b'The 7 Rules of Idol Play' in resp.data

    def test_idol_strategy_has_type_catalog(self, client):
        resp = client.get('/idol-strategy')
        assert resp.status_code == 200
        assert b'Standard Hidden Immunity Idol' in resp.data
        assert b'God Idol (Post-Vote Read)' in resp.data

    def test_idol_strategy_god_idol_not_in_strategies(self, client):
        """God Idol strategies should not bleed into standard idol analysis"""
        resp = client.get('/idol-strategy')
        html = resp.data.decode()
        # The strategies tab should not reference Tyler Perry or Super Idol
        strategies_section = html.split('TAB 3: STRATEGIES')[1].split('TAB 4:')[0]
        assert 'Tyler Perry' not in strategies_section
        assert 'Super Idol' not in strategies_section

    def test_nav_shows_idol_strategy(self, client):
        resp = client.get('/idol-strategy')
        assert b'Idol Strategy' in resp.data
        assert b'/idol-strategy' in resp.data


# --- Data Integrity Tests ---

class TestDataIntegrity:
    def test_all_39_seasons_loaded(self):
        for s in range(1, 40):
            assert s in seasons_data, f"Season {s} not loaded"

    def test_every_season_has_castaways(self):
        for s in range(1, 40):
            castaways = seasons_data[s]['voting'].get('castaways', [])
            assert isinstance(castaways, list), f"Season {s} castaways is not a list"

    def test_every_season_has_challenges(self):
        for s in range(1, 40):
            challenges = seasons_data[s]['challenges'].get('challenges', [])
            assert isinstance(challenges, list), f"Season {s} challenges is not a list"

    def test_winner_profiles_loaded(self):
        assert len(winner_profiles) > 0, "No winner profiles loaded"

    def test_all_season_names(self):
        for s in range(1, 40):
            assert s in SEASON_NAMES, f"Season {s} missing from SEASON_NAMES"

    def test_available_seasons(self):
        assert len(AVAILABLE_SEASONS) == 39
        assert 1 in AVAILABLE_SEASONS
        assert 39 in AVAILABLE_SEASONS
