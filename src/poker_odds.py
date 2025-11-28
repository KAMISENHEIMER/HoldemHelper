from pokerkit.analysis import calculate_hand_strength
from pokerkit import parse_range, Card, Deck, StandardHighHand 
from concurrent.futures import ProcessPoolExecutor

RANK_MAP = {
    "two": "2", 
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "ten": "T", 
    "jack": "J", 
    "queen": "Q", 
    "king": "K", 
    "ace": "A"
}

#quickly convert image detection output into pokerkit input
def format_cards(cards):
    return "".join([RANK_MAP.get(rank) + suit[0] for rank, suit, rs, ss in cards])

def calculate_odds(num_players, player_cards, river_cards, num_simulations=10000):
    # num_players = 2
    # player_cards = 'AsAh'
    # river_cards = 'Kc8h8d'
    # river_cards = ''

    with ProcessPoolExecutor() as executor:
        results = calculate_hand_strength(
            num_players,
            parse_range(player_cards),
            Card.parse(river_cards),
            2,                              #cards per player
            5,                              #total community cards
            Deck.STANDARD,
            (StandardHighHand,),
            sample_count=num_simulations,
            executor=executor,
        )

    # print(f"Hand Strength: {results}")
    return results