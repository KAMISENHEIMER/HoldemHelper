import cv2
import numpy as np

def isolate_cards(image, rectangles):
    
    #card dimensions for output
    card_w, card_h = 250, 350
    
    #desired flattened corner positions
    transformation = np.array([
        [0, 0],                   #top-left
        [card_w - 1, 0],          #top-right
        [card_w - 1, card_h - 1], #bottom-right
        [0, card_h - 1]           #bottom-left
    ], dtype="float32")

    cardImages = []

    for i, rect in enumerate(rectangles):
        corners = np.array(rect, dtype="float32")

        #order corners
        s = corners.sum(axis=1)
        diff = np.diff(corners, axis=1)
        ordered_corners = np.zeros((4, 2), dtype="float32")
        ordered_corners[0] = corners[np.argmin(s)]      #top-left (smallest sum)
        ordered_corners[2] = corners[np.argmax(s)]      #bottom-right (largest sum)
        ordered_corners[1] = corners[np.argmin(diff)]   #top-right (smallest diff)
        ordered_corners[3] = corners[np.argmax(diff)]   #bottom-left (largest diff)

        #warp perspective to make cards flat
        M = cv2.getPerspectiveTransform(ordered_corners, transformation)
        warped = cv2.warpPerspective(image, M, (card_w, card_h))

        # cv2.imwrite(f"output/cards/card{i+1}.jpg", warped)
        cardImages.append(warped)
    
    return cardImages
