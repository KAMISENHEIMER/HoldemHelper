from detect_cards import detect_rectangles, draw_rectangles, split
from isolate_cards import isolate_cards
from template_matching import classify_cards
from poker_odds import format_cards, calculate_odds

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
    
    #detect rectangles in image
    river_rects = detect_rectangles(river_image)
    hand_rects = detect_rectangles(hand_image)

    # prints out detected rectangles - DEBUG
    # print("Rectangles detected:", len(rects))
    # for i, rect in enumerate(rects):
    #     print(f"Rectangle {i+1} corners:", rect)

    #draw detected rectangles on image - DEBUG
    # draw_rectangles(image_path, river_rects)

    #form isolated cards
    river_card_images = isolate_cards(river_image, river_rects)
    hand_card_images = isolate_cards(hand_image, hand_rects)

    #get results from each card image
    river_guesses = classify_cards(river_card_images)
    hand_guesses = classify_cards(hand_card_images)

    #ouput results
    print(f"{'RANK':<6} \t {'SUIT':<8} \t {'RANK-SCORE':<12} \t {'SUIT-SCORE'}")
    print("RIVER" + "-" * 60)
    for rank, suit, rs, ss in river_guesses:
        print(f"{rank:<6} \t {suit:<8} \t {rs:.2f} \t \t {ss:.2f}")
    print("HAND" + "-" * 60)
    for rank, suit, rs, ss in hand_guesses:
        print(f"{rank:<6} \t {suit:<8} \t {rs:.2f} \t \t {ss:.2f}")    

    formatted_river = format_cards(river_guesses)
    formatted_hand = format_cards(hand_guesses)

    odds = calculate_odds(num_players, formatted_hand, formatted_river, num_simulations)

    print(f"CHANCE OF WINNING: {odds*100:.2f}%")



    


    
