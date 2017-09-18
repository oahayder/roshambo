from app.data_access import write_to_db
from app.data_access import query_db

def create_game():
    """
    Initialize a game with no moves

    :return int: game id
    """
    id = write_to_db('INSERT INTO games (active) VALUES (1)')

    return id

def make_move(game_id, username, move):
    """
    Given a username and a move, make a move on a game. If this is
    the second move, evalute the game outcome.

    :param username:
    :param move:
    :return:
    """
    game = get_game(game_id)
    if not game or not game['active'] or game['winner']:
        return None

    if game['player_a_move'] is None:
        query = "UPDATE games SET player_a_username='{}', player_a_move='{}' WHERE id={}".format(username, move, game_id)
        write_to_db(query)
    elif game['player_b_move'] is None:
        query = "UPDATE games SET player_b_username='{}', player_b_move='{}' WHERE id={}".format(username, move, game_id)
        write_to_db(query)

        calculate_winner(game_id)
    else:
        return None

    return get_game(game_id)


def move_translator(move):
    """
    This is a dumb function. Would setup an enum but am too lazy
    :param move:
    :return:
    """
    if move == 'rock':
        return 1
    if move == 'paper':
        return 2
    if move == 'scissors':
        return 3

    return 0

def get_game(game_id):
    """
    Get a game resource

    :param game_id:
    :return:
    """
    game = query_db('select * from games where id=?',
                    [game_id], one=True)

    return game

def calculate_winner(game_id):
    """
    Given a game id, decide if there is a winner or not and update the game

    :param game_id:
    :return char: letter representing player or 't' for tie
    """

    game = get_game(game_id)
    if not game['active'] or game['winner']:
        return None

    if not (game['player_a_move'] and game['player_b_move']):
        return None

    # 'rock' = 1
    # 'paper' = 2
    # 'scissors' = 3

    result = move_translator(game['player_a_move']) - move_translator(game['player_b_move'])

    if result == 0:
        query = "UPDATE games SET winner='t', active=0 WHERE id={}".format(game_id)
        write_to_db(query)
        return 't'

    elif result == -2 or result == 1:
        # Player A wins
        query = "UPDATE games SET winner='a', active=0 WHERE id={}".format(game_id)
        write_to_db(query)
        return 'a'

    else:
        # Player B wins
        query = "UPDATE games SET winner='b', active=0 WHERE id={}".format(game_id)
        write_to_db(query)
        return 'b'
