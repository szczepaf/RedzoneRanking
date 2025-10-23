import json

class Player:
    """A class for representing one individual player.

    Attributes:

    name: the player's name used in the scoring records.
    ranking: overall +- across all practices.
    number_of_games: number of practices (games) played by the given player.
    """
    
    name: str
    ranking: int = 0
    number_of_games: int = 0

    def __init__(self, name: str, ranking: int = 0, number_of_games = 0) -> None:
        self.name = name
        self.ranking = ranking
        self.number_of_games = number_of_games

    def update_ranking(self, score_diff: int) -> None:
        """Update the player's ranking by the given score difference."""
        self.ranking += score_diff

    def __str__(self) -> str:
        """
        Return a stable string dump of all fields (as a JSON dict).
        Example:
        {"name": "Alice", "ranking": 12, "number_of_games": 3}
        """
        return json.dumps(
            {
                "name": self.name,
                "ranking": self.ranking,
                "number_of_games": self.number_of_games,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    
    @classmethod
    def from_string(cls, player_str: str) -> "Player":
        """
        Create a Player from the JSON string produced by __str__.
        """
        data = json.loads(player_str)
        return cls(name=data["name"], ranking=data.get("ranking", 0), number_of_games=data.get("number_of_games", 0))
