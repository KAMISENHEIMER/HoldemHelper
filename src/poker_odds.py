from pokerkit.analysis import calculate_hand_strength
from pokerkit import parse_range, Card, Deck, StandardHighHand 
from concurrent.futures import ProcessPoolExecutor

if __name__ == '__main__':    
    num_players = 2
    player_cards = 'AsAh'
    # river_cards = 'Kc8h8d'
    river_cards = ''

    with ProcessPoolExecutor() as executor:
        results = calculate_hand_strength(
            num_players,
            parse_range(player_cards),
            Card.parse(river_cards),
            2,                              #cards per player
            5,                              #total community cards
            Deck.STANDARD,
            (StandardHighHand,),
            sample_count=10000,
            executor=executor,
        )

    print(f"Hand Strength: {results}")