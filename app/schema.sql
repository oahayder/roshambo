CREATE TABLE IF NOT EXISTS games (
    id integer PRIMARY KEY,
    player_a_username text,
    player_b_username text,
    player_a_move text,
    player_b_move text,
    winner integer,
    active boolean
)
