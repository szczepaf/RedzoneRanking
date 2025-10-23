from Player import Player
import json
import pandas as pd  
import csv

PLAYER_DB_FILE = "players_db.txt"


def _parse_team(team_str: str) -> list[str]:
    """
    Parse a team string of form "[Name1|Name2|Name3]".
    Returns a list of player names.
    """
    s = team_str.strip()
    
    # remove surrounding brackets if present
    if s.startswith("[") and s.endswith("]"):
        s = s[1:-1]
    # split on '|' and strip whitespace around names
    return [part.strip() for part in s.split("|") if part.strip()]

def load_players_from_db() -> dict[str, Player]:
    """Load the players from the given db file and return a dict of Player objects keyed by player name."""

    players: dict[str, Player] = {}
    with open(PLAYER_DB_FILE, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line.strip())
            current_player = Player.from_string(json.dumps(data, ensure_ascii=False))
            players[current_player.name] = current_player
    return players


def process_practice_results(row: pd.Series, players: dict[str, Player]) -> None:
    """
    Process the results of a single practice session.
    One practice session is represented by one row in the CSV file.

    The row has the following columns: Date,A-Score,B-Score,A-team,B-team,Processed
    The teams are represented as |-delimited player names in list, e.g. [Karlos|Alex|VojtysR|Eli|Cross|Čégo|Halámka|Štrůdl]

    One row is processed as follows:
      - Parse A and B team player names
      - Update each player's ranking by the corresponding diff (A-diff/B-diff)
      - Increment number_of_games by 1 for all players who appeared
      - Overwrite the DB file with the updated players
    """
    # if the row is already processed, skip it
    if row.get("Processed", False):
        return

    # Compute score diffs
    a_score = row.get("A-Score")
    b_score = row.get("B-Score")
    a_diff = a_score - b_score
    b_diff = b_score - a_score

    # Parse team rosters
    a_team = _parse_team(row.get("A-team"))
    b_team = _parse_team(row.get("B-team"))

    # Ensure all players exist in the dict (allowing new names to appear - create a new Player object for them)
    for name in a_team + b_team:
        if name not in players:
            players[name] = Player(name=name)

    # Update rankings and number_of_games
    for name in a_team:
        players[name].update_ranking(a_diff)
        players[name].number_of_games += 1

    for name in b_team:
        players[name].update_ranking(b_diff)
        players[name].number_of_games += 1

    # Save back to the same DB file we loaded from

    # Write players back as newline-delimited JSON, sorted by name for stability
    with open(PLAYER_DB_FILE, "w", encoding="utf-8") as f:
        for p in sorted(players.values(), key=lambda x: x.name.lower()):
            f.write(str(p) + "\n")


def main():
    """Main function to load players, process the CSV file, and update player rankings."""
    # Load existing players from the DB
    players = load_players_from_db()

    # Load the practice results CSV
    df = pd.read_csv("practice_results.csv")

    # Keep only unprocessed rows
    df = df[~df.get("Processed")]

    # Process each row in the CSV
    for index, row in df.iterrows():
        process_practice_results(row, players)

    # Mark all rows as processed and save back to CSV
    df["Processed"] = True
    df.to_csv("practice_results.csv", index=False)
