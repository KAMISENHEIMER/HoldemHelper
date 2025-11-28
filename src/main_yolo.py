from detect_cards import detect_rectangles, draw_rectangles, split
from isolate_cards import isolate_cards
from template_matching import classify_cards
from poker_odds import format_cards, calculate_odds
from detect_cards_yolo import detect_cards, format_cards_from_yolo, draw_detections

if __name__ == "__main__":
    import sys
    import argparse
    import os

    #example images
    # image_path = "test_images/5cardsbasic.png"
    # image_path = "test_images/5cardswithclutter.png"
    # image_path = "test_images/3cardswithclutter.png" #failure case, chip on card
    # image_path = "test_images/5cardswithhands.png" #failure case, stylized background
    # image_path = "test_images/boonecards4.png"
    # image_path = "test_images/onlinepoker.PNG"
    # image_path = "test_images/riverandhand.PNG"

    #command line input
    parser = argparse.ArgumentParser()
    parser.add_argument("image_path", help="Path to image file")
    parser.add_argument("num_players", type=int, help="Number of players")
    parser.add_argument("--sims", type=int, default=10000, help="Number of simulations")
    
    args = parser.parse_args()
    image_path = args.image_path
    num_players = args.num_players
    num_simulations = args.sims

    #error checking
    if not os.path.exists(image_path):
        sys.exit(f"Error: Image file '{args.image_path}' not found.")
    if num_players < 2:
        sys.exit("Error: Number of players must be at least 2")
    if num_simulations < 1:
        sys.exit("Error: Number of simulations must be at least 1")

    river_image, hand_image = split(image_path)
    
    #yolo magic here
    river_guesses = detect_cards(river_image)
    hand_guesses = detect_cards(hand_image)

    formatted_river = format_cards_from_yolo(river_guesses)
    formatted_hand = format_cards_from_yolo(hand_guesses)

    #ouput results
    print("RIVER" + "-" * 60)
    print(formatted_river)
    print("HAND" + "-" * 60)
    print(formatted_hand)

    odds = calculate_odds(num_players, formatted_hand, formatted_river, num_simulations)

    print(f"CHANCE OF WINNING: {odds*100:.2f}%")



    


    
