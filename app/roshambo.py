from flask import Flask
from flask import request
from flask import g
from flask import jsonify

from app.game import get_game
from app.game import make_move
from app.game import create_game

app = Flask(__name__)

@app.route('/health')
def health():
    """
    Will eventually return status checks for all dependancies
    """
    health_checks = {}
    return jsonify(health_checks)

@app.route('/game', methods=['POST'])
def game_resource():
    game_id = create_game()
    game = get_game(game_id)
    return jsonify(game)

@app.route('/game/<game_id>', methods=['GET', 'PUT'])
def game_resources(game_id):
    if request.method == 'GET':
        result = get_game(game_id)
    elif request.method == 'PUT':
        username = request.form['username']
        move = request.form['move']
        result = make_move(game_id, username, move)
    else:
        result = '{}'

    return jsonify(result)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()