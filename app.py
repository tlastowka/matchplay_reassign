from flask import Flask, render_template, request, url_for, flash, redirect
import os
from mpnext import MpNext
from random import choice

# ...
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
app.config['NEXT_MATCHPLAY_API_KEY'] = os.environ.get('NEXT_MATCHPLAY_API_KEY')


def _build_arena_map(tournament_id):

    """
    organizes a bunch of data from mp in a way thats easier to use
    TODO:  clean this up
    """
    api = MpNext(app.config['NEXT_MATCHPLAY_API_KEY'])
    tournament = api.get_tournament(
        tournament_id,
        includeArenas=True,
        includePlayers=True
    )['data']

    active_games = api.get_tournament_games(tournament_id, status='started')['data']
    tournament_id = tournament['tournamentId']
    wanted_arena = ['arenaId', 'name']

    arenas = tournament['arenas']
    players = tournament['players']
    arena_map = {}
    for a in arenas:
        _a = {w: a[w] for w in wanted_arena}
        _a['active_game'] = False
        _a['tournamentId'] = tournament_id
        arena_map[a['arenaId']] = _a

    for g in active_games:
        arena_id = g.get('arenaId')
        player_ids = g.get('playerIds')
        game_players = [
            p for p in players
            if p['playerId'] in player_ids
        ]
        arena_map[arena_id]['active_game'] = True
        arena_map[arena_id]['game'] = g
        arena_map[arena_id]['players'] = game_players

    return arena_map


@app.route('/')
def index():
    """Does nothing"""
    return render_template('index.html')


@app.route('/active/<tournament_id>')
def active(tournament_id):

    """Displays active games in tournament"""
    arena_map = _build_arena_map(tournament_id)

    return render_template('active.html', arena_map=arena_map)


@app.route('/reassign/<tournament_id>/<arena_id>')
def reassign(tournament_id, arena_id):

    """suggests a replacement game"""
    arena_map = _build_arena_map(tournament_id)

    if int(arena_id) not in arena_map:

        raise Exception(f"""arena_id {arena_id} doesn't appear in this tournament!""")
    available_games = [v for v in arena_map.values() if not v['active_game']]
    deactivated_game = arena_map[int(arena_id)]
    replacement_game = choice(available_games)

    return render_template('reassign.html', deactivated_game=deactivated_game, replacement_game=replacement_game)
