from detect_cards import detect_rectangles, draw_rectangles, split
from isolate_cards import isolate_cards
from template_matching import classify_cards
from poker_odds import format_cards, calculate_odds

if __name__ == "__main__":
    import sys

    #example images
    # image_path = "test_images/5cardsbasic.png"
    # image_path = "test_images/5cardswithclutter.png"
    # image_path = "test_images/3cardswithclutter.png" #failure case, chip on card
    # image_path = "test_images/5cardswithhands.png" #failure case, stylized background
    # image_path = "test_images/boonecards4.png"
    # image_path = "test_images/onlinepoker.PNG"
    image_path = "test_images/riverandhand.PNG"

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

    num_players = 2
    num_simulations = 10000

    odds = calculate_odds(num_players, formatted_hand, formatted_river, num_simulations)

    print(f"CHANCE OF WINNING: {odds*100:.2f}%")



    


    
