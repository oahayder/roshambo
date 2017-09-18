# roshambo

Proof of concept

# Quickstart
```python
Clone repo. 
Optionally create you're own virtual env
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app/roshambo.py
export ROSHAMBO_DB=<path to db> Ex. $HOME/roshambo.db
flask run --host=0.0.0.0
```

# Run tests
```
python tests/test_game.py
```
