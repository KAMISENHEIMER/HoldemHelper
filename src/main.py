from detect_cards import detect_rectangles, draw_rectangles
from isolate_cards import isolate_cards
from template_matching import classify_cards

if __name__ == "__main__":
    import sys

    #example images
    # image_path = "test_images/5cardsbasic.png"
    image_path = "test_images/5cardswithclutter.png"
    # image_path = "test_images/3cardswithclutter.png" #failure case, chip on card
    # image_path = "test_images/5cardswithhands.png" #failure case, stylized background
    # image_path = "test_images/boonecards2.png"
    
    #detect rectangles in image
    rects = detect_rectangles(image_path)

    # prints out detected rectangles - DEBUG
    # print("Rectangles detected:", len(rects))
    # for i, rect in enumerate(rects):
    #     print(f"Rectangle {i+1} corners:", rect)

    #draw detected rectangles on image - DEBUG
    # draw_rectangles(image_path, rects)

    #form isolated cards
    cardImages = isolate_cards(image_path, rects)

    #get results from each card image
    results = classify_cards(cardImages)

    #ouput results
    print(f"{'RANK':<6} \t {'SUIT':<8} \t {'RANK-SCORE':<12} \t {'SUIT-SCORE'}")
    print("-" * 60)
    for rank, suit, rs, ss in results:
        print(f"{rank:<6} \t {suit:<8} \t {rs:.2f} \t \t {ss:.2f}")


    
