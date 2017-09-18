import os
import json
from app import roshambo
import unittest
import tempfile


from app.helpers import init_db

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, roshambo.app.config['DATABASE'] = tempfile.mkstemp()
        roshambo.app.testing = True
        self.app = roshambo.app.test_client()
        with roshambo.app.app_context():
            init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(roshambo.app.config['DATABASE'])

    def test_health(self):
        """
        Get status of dependancies
        :return:
        """
        rv = self.app.get('/health')
        result = json.loads(rv.data)
        assert result == {}

    def test_create_game(self):
        """
        Create a game and get a valid game_id
        :return:
        """
        rv = self.app.post('/game')
        game = json.loads(rv.data)
        assert game['active'] == True
        assert game['winner'] == None
        assert game['player_a_username'] == None
        assert game['player_a_move'] == None
        assert game['player_b_username'] == None
        assert game['player_b_move'] == None


    def test_make_move(self):
        """
        Should be able to make an initial move and update the game
        :return:
        """
        rv = self.app.post('/game')
        game = json.loads(rv.data)

        self.app.put('/game/{}'.format(game['id']), data=dict(
        username='player 1',
        move='rock'))

        rv = self.app.get('/game/{}'.format(game['id']))
        game = json.loads(rv.data)

        assert game['active'] == True
        assert game['winner'] == None
        assert game['player_a_username'] == 'player 1'
        assert game['player_a_move'] == 'rock'
        assert game['player_b_username'] == None
        assert game['player_b_move'] == None


    def test_tie_game(self):
        """
        Identical moves result in a tie. Game ends with no winner
        :return:
        """
        rv = self.app.post('/game')
        game = json.loads(rv.data)

        self.app.put('/game/{}'.format(game['id']), data=dict(
        username='player 1',
        move='rock'))
        self.app.put('/game/{}'.format(game['id']), data=dict(
        username='player 2',
        move='rock'))

        rv = self.app.get('/game/{}'.format(game['id']))
        game = json.loads(rv.data)

        assert game['active'] == False
        assert game['winner'] == 't'
        assert game['player_a_username'] == 'player 1'
        assert game['player_a_move'] == 'rock'
        assert game['player_b_username'] == 'player 2'
        assert game['player_b_move'] == 'rock'


    def test_winner(self):
        """
        Winning move results in a defined winneer, game over
        :return:
        """

        # RbS
        rv = self.app.post('/game')
        game = json.loads(rv.data)

        self.app.put('/game/{}'.format(game['id']), data=dict(
        username='player 1',
        move='rock'))
        self.app.put('/game/{}'.format(game['id']), data=dict(
        username='player 2',
        move='scissors'))

        rv = self.app.get('/game/{}'.format(game['id']))
        game = json.loads(rv.data)

        assert game['active'] == False
        assert game['winner'] == 'a'
        assert game['player_a_username'] == 'player 1'
        assert game['player_a_move'] == 'rock'
        assert game['player_b_username'] == 'player 2'
        assert game['player_b_move'] == 'scissors'

        #SbP
        rv = self.app.post('/game')
        game = json.loads(rv.data)

        self.app.put('/game/{}'.format(game['id']), data=dict(
        username='player 1',
        move='paper'))
        self.app.put('/game/{}'.format(game['id']), data=dict(
        username='player 2',
        move='scissors'))

        rv = self.app.get('/game/{}'.format(game['id']))
        game = json.loads(rv.data)

        assert game['active'] == False
        assert game['winner'] == 'b'
        assert game['player_a_username'] == 'player 1'
        assert game['player_a_move'] == 'paper'
        assert game['player_b_username'] == 'player 2'
        assert game['player_b_move'] == 'scissors'

        #RbS
        rv = self.app.post('/game')
        game = json.loads(rv.data)

        self.app.put('/game/{}'.format(game['id']), data=dict(
        username='player 1',
        move='scissors'))
        self.app.put('/game/{}'.format(game['id']), data=dict(
        username='player 2',
        move='rock'))

        rv = self.app.get('/game/{}'.format(game['id']))
        game = json.loads(rv.data)

        assert game['active'] == False
        assert game['winner'] == 'b'
        assert game['player_a_username'] == 'player 1'
        assert game['player_a_move'] == 'scissors'
        assert game['player_b_username'] == 'player 2'
        assert game['player_b_move'] == 'rock'

        #RbS
        rv = self.app.post('/game')
        game = json.loads(rv.data)

        self.app.put('/game/{}'.format(game['id']), data=dict(
        username='player 1',
        move='rock'))
        self.app.put('/game/{}'.format(game['id']), data=dict(
        username='player 2',
        move='scissors'))

        rv = self.app.get('/game/{}'.format(game['id']))
        game = json.loads(rv.data)

        assert game['active'] == False
        assert game['winner'] == 'a'
        assert game['player_a_username'] == 'player 1'
        assert game['player_a_move'] == 'rock'
        assert game['player_b_username'] == 'player 2'
        assert game['player_b_move'] == 'scissors'


if __name__ == '__main__':
    unittest.main()
