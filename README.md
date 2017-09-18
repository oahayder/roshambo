# roshambo

Proof of concept

# Quickstart

pip install -r requirements.txt
export FLASK_APP=app/roshambo.py
export ROSHAMBO_DB=<path to db> Ex. $HOME/roshambo.db
flask run --host=0.0.0.0

# Run tests

python tests/test_game.py
