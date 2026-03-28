# %%
# 100. General
# 100.1. These Magic rules apply to any Magic game with two or more players, including two-player
# games and multiplayer games.
class Game:
    ...

class Player:
    ...


def game_has_players(self, *args, __init=Game.__init__, **kwargs):
    __init(self, *args, **kwargs)
    self.players: list[Player] = kwargs.get("players")

Game.__init__ = game_has_players


def rules_apply(game: Game) -> bool:
    return len(game.players) >= 2

# 100.1a A two-player game is a game that begins with only two players.
def is_two_player(game: Game) -> bool:
    return len(game.players) == 2

# 100.1b A multiplayer game is a game that begins with more than two players. See section 8,
# “Multiplayer Rules.”
def is_multiplayer(game: Game) -> bool:
    return len(game.players) > 2

# 100.2. To play, each player needs their own deck of traditional Magic cards, small items to represent any tokens and counters, and some way to clearly track life totals.
class Deck:
    ...

class TokenAndCounterTracker:
    ...

class LifeTotalTracker:
    ...

def player_has_deck(self, *args, __init=Player.__init__, **kwargs):
    __init(self, *args, **kwargs)
    self.deck: Deck = kwargs.get("deck")
    self.token_and_counter_tracker: TokenAndCounterTracker = kwargs.get("token_and_counter_tracker")
    self.life_total_tracker: LifeTotalTracker = kwargs.get("life_total_tracker")

Player.__init__ = player_has_deck


# 100.2a In constructed play (a way of playing in which each player creates their own deck ahead of time), each deck has a minimum deck size of 60 cards. A constructed deck may contain any number of basic land cards and no more than four of any card with a particular English name other than basic land cards. For the purposes of deck construction, cards with interchangeable names have the same English name (see rule 201.3).

# 100.2b In limited play (a way of playing in which each player gets the same quantity of unopened Magic product such as booster packs and creates their own deck using only this product and basic land cards), each deck has a minimum deck size of 40 cards. A limited deck may contain as many duplicates of a card as are included with the product.

# 100.2c Commander decks are subject to additional deckbuilding restrictions and requirements. See rule 903, “Commander,” for details.

# 100.2d Some formats and casual play variants allow players to use a supplementary deck of nontraditional Magic cards (see rule 108.2a). These supplementary decks have their own deck construction rules. See rule 717, “Attraction Cards;” rule 901, “Planechase;” and rule 904, “Archenemy.”

# 100.3. Some cards require coins or traditional dice. Some casual variants require additional items, such as specially designated cards, nontraditional Magic cards, and specialized dice.

# 100.4. Each player may also have a sideboard, which is a group of additional cards the player may use to modify their deck between games of a match. Sideboard rules and restrictions for some formats are modified by the Magic: The Gathering Tournament Rules (found at WPN.Wizards.com/en/rules-documents).

# 100.4a In constructed play, a sideboard may contain no more than fifteen cards. The four-card limit (see rule 100.2a) applies to the combined deck and sideboard.

# 100.4b In limited play involving individual players, all cards in a player’s card pool not included in their deck are in that player’s sideboard.

# 100.4c In limited play involving the Two-Headed Giant multiplayer variant, all cards in a team’s card pool but not in either player’s deck are in that team’s sideboard
# %%
