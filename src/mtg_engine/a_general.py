# --- DSL Framework ---
def add_properties(cls, **annotations):
    """
    Dynamically adds typed properties to a class and updates its __init__
    so it can accept them as kwargs, preserving previous properties.
    """
    if not hasattr(cls, '__annotations__'):
        cls.__annotations__ = {}
    cls.__annotations__.update(annotations)

    if not hasattr(cls, '_dsl_properties'):
        cls._dsl_properties = []
        
    # Only add new properties to avoid duplicates if called multiple times on the same class
    for key in annotations:
        if key not in cls._dsl_properties:
            cls._dsl_properties.append(key)

    def new_init(self, **kwargs):
        for prop in self.__class__._dsl_properties:
            setattr(self, prop, kwargs.get(prop))
            
    cls.__init__ = new_init
    return cls

# ==========================================
# MTG Comprehensive Rules
# ==========================================
# 100. General
# 100.1. These Magic rules apply to any Magic game with two or more players, including two-player
# games and multiplayer games.
class Game:
    pass

class Player:
    pass


add_properties(Game, players=list[Player])


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
    pass

class Card:
    pass

class TokenAndCounterTracker:
    pass

class LifeTotalTracker:
    pass


add_properties(Deck, cards=list[Card])

add_properties(Player, 
    deck=Deck,
    token_and_counter_tracker=TokenAndCounterTracker,
    life_total_tracker=LifeTotalTracker
)


# 100.2a In constructed play (a way of playing in which each player creates their own deck ahead of time), each deck has a minimum deck size of 60 cards. 
# A constructed deck may contain any number of basic land cards and no more than four of any card with a particular English name other than basic land cards. 
# For the purposes of deck construction, cards with interchangeable names have the same English name (see rule 201.3).
add_properties(Card, 
    english_name=str, 
    is_basic_land=bool
)


def is_valid_constructed_deck(deck: Deck) -> bool:
    from collections import Counter

    has_minimum_cards = len(deck.cards) >= 60
    
    # Count how many times each English name appears
    counts = Counter(card.english_name for card in deck.cards if not card.is_basic_land)
    
    # Check if any non-basic land name appears more than 4 times
    has_no_more_than_four_copies = all(count <= 4 for count in counts.values())
    
    return has_minimum_cards and has_no_more_than_four_copies


# 100.2b In limited play (a way of playing in which each player gets the same quantity of unopened Magic product such as booster packs and 
# creates their own deck using only this product and basic land cards), each deck has a minimum deck size of 40 cards. A limited deck may 
# contain as many duplicates of a card as are included with the product.
def is_valid_limited_deck(deck: Deck) -> bool:
    return len(deck.cards) >= 40

# 100.2c Commander decks are subject to additional deckbuilding restrictions and requirements. See rule 903, “Commander,” for details.
def is_valid_commander_deck(deck: Deck) -> bool:
    raise NotImplementedError("Commander deck rules are not implemented yet.")

# 100.2d Some formats and casual play variants allow players to use a supplementary deck of nontraditional Magic cards (see rule 108.2a). 
# These supplementary decks have their own deck construction rules. See rule 717, “Attraction Cards;” rule 901, “Planechase;” and rule 904, “Archenemy.”
class AttractionCardDeck:
    pass

class PlanechaseDeck:
    pass

class ArchenemyDeck:
    pass


# 100.3. Some cards require coins or traditional dice. Some casual variants require additional items, such as specially designated cards, nontraditional Magic cards, and specialized dice.
class Coin:
    pass

class Die:
    pass

class SpeciallyDesignatedCard:
    pass

class NontraditionalMagicCard:
    pass

class SpecializedDie:
    pass

# 100.4. Each player may also have a sideboard, which is a group of additional cards the player may use to modify their deck between games of a match.
# Sideboard rules and restrictions for some formats are modified by the Magic: The Gathering Tournament Rules (found at WPN.Wizards.com/en/rules-documents).
class Sideboard:
    pass

add_properties(Player, sideboard=Sideboard)

class Match:
    pass

add_properties(Match, games=list[Game])

# 100.4a In constructed play, a sideboard may contain no more than fifteen cards. The four-card limit (see rule 100.2a) applies to the combined deck and sideboard.
def is_valid_constructed_sideboard(sideboard: Sideboard, deck: Deck) -> bool:
    from collections import Counter

    if len(sideboard.cards) > 15:
        return False
    
    combined_cards = deck.cards + sideboard.cards
    
    # Count how many times each English name appears
    counts = Counter(card.english_name for card in combined_cards if not card.is_basic_land)
    
    # Check if any non-basic land name appears more than 4 times
    has_no_more_than_four_copies = all(count <= 4 for count in counts.values())
    
    return has_no_more_than_four_copies

# 100.4b In limited play involving individual players, all cards in a player’s card pool not included in their deck are in that player’s sideboard.
class CardPool:
    pass

add_properties(CardPool, cards=list[Card])
add_properties(Player, card_pool=CardPool)


def is_valid_limited_sideboard(sideboard: Sideboard, card_pool: CardPool, deck: Deck) -> bool:
    if not len(deck.cards) + len(sideboard.cards) == len(card_pool.cards):
        return False

    for card in card_pool.cards:
        if card not in deck.cards and card not in sideboard.cards:
            return False
    return True

# 100.4c In limited play involving the Two-Headed Giant multiplayer variant, all cards in a team’s card pool but not in either
# player’s deck are in that team’s sideboard
class TwoHeadedGiantTeam:
    pass

add_properties(TwoHeadedGiantTeam, 
    players=list[Player], 
    card_pool=CardPool, 
    sideboard=Sideboard
)

def is_valid_two_headed_giant_sideboard(two_headed_giant_team: TwoHeadedGiantTeam) -> bool:
    # 1. Check total count to ensure no cards were duplicated or lost
    total_cards_in_play = sum(len(p.deck.cards) for p in two_headed_giant_team.players)
    total_cards_in_play += len(two_headed_giant_team.sideboard.cards)
    
    if total_cards_in_play != len(two_headed_giant_team.card_pool.cards):
        return False

    # 2. Ensure every card in the pool is actually present somewhere
    for card in two_headed_giant_team.card_pool.cards:
        in_a_deck = any(card in p.deck.cards for p in two_headed_giant_team.players)
        if not in_a_deck and card not in two_headed_giant_team.sideboard.cards:
            return False
            
    return True

# 100.4d In limited play involving other multiplayer team variants, each card in a team’s card pool but not in any player’s deck
# is assigned to the sideboard of one of those players. Each player has their own sideboard; cards may not be transferred between players.
class Team:
    pass

add_properties(Team, 
    players=list[Player], 
    card_pool=CardPool
)

def is_valid_multiplayer_team_sideboard(team: Team) -> bool:
    # Check total pool integrity: Pool = Sum(all decks) + Sum(all sideboards)
    total_cards_in_decks = sum(len(p.deck.cards) for p in team.players)
    total_cards_in_sideboards = sum(len(p.sideboard.cards) for p in team.players)
    
    if total_cards_in_decks + total_cards_in_sideboards != len(team.card_pool.cards):
        return False

    # Ensure every card in the pool is in exactly one player's deck OR exactly one player's sideboard
    for card in team.card_pool.cards:
        found_count = 0
        for player in team.players:
            if card in player.deck.cards:
                found_count += 1
            if card in player.sideboard.cards:
                found_count += 1
        
        if found_count != 1:
            return False
            
    return True

# 100.5. If a deck must contain at least a certain number of cards, that number is referred to as a minimum deck size. There is no maximum deck size for non-Commander decks.
def is_deck_size_valid(deck: Deck, minimum_deck_size: int, is_commander: bool = False) -> bool:
    """
    Validates a deck against a provided minimum_deck_size. 
    The minimum size is dictated by the format/ruleset, not the deck object itself.
    """
    if is_commander:
        raise NotImplementedError("Commander maximum deck size rules are not implemented yet.")
    
    return len(deck.cards) >= minimum_deck_size


# 100.6. Most Magic tournaments (organized play activities where players compete against other players to win prizes) have additional rules covered in the Magic: The Gathering Tournament Rules (found at WPN.Wizards.com/en/rules-documents). These rules may limit the use of some cards, including barring all cards from some older sets.
class Tournament:
    """
    Informational: Tournaments are governed by the MTR (WPN.Wizards.com/en/rules-documents).
    """
    pass

add_properties(Tournament, banned_cards=list[Card]) # Representing the mechanical limitation of cards


# 100.6a Tournaments usually consist of a series of matches. A two-player match usually involves playing until one player has won two games. A multiplayer match usually consists of only one game.
add_properties(Tournament, matches=list[Match])

# We need a way to track game winners to calculate match completion
add_properties(Game, winner=Player)

def is_two_player_match_complete(match: Match) -> bool:
    from collections import Counter
    
    # Count how many games each player has won in this match
    win_counts = Counter(game.winner for game in match.games if game.winner is not None)
    
    # Match is complete if any player has won at least 2 games
    return any(wins >= 2 for wins in win_counts.values())

def is_multiplayer_match_complete(match: Match) -> bool:
    # A multiplayer match usually consists of only one game
    return len(match.games) >= 1


# 100.6b Players can use the Magic Store & Event Locator at Locator.Wizards.com to find tournaments in their area.
# (Informational text: No mechanical programmatic implementation required.)


# 100.7. Certain cards are intended for casual play and may have features and text that aren’t covered by these rules. These include Mystery Booster playtest cards, promotional cards and cards in “Un-sets” that were printed with a silver border, and cards in the Unfinity™ expansion that have an acorn symbol at the bottom of the card.
add_properties(Card, 
    is_playtest_card=bool,
    is_promotional_casual=bool,
    is_silver_bordered=bool,
    has_acorn_symbol=bool
)

def is_casual_only_card(card: Card) -> bool:
    return (
        card.is_playtest_card or 
        card.is_promotional_casual or 
        card.is_silver_bordered or 
        card.has_acorn_symbol
    )
# %%
