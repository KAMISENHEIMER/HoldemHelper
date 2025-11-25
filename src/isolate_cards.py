import cv2
import numpy as np

#ensure corners are always in the same order
# (top-left, top-right, bottom-right, bottom-left)
def order_corners(pts):
    rect = np.zeros((4, 2), dtype="float32")

    #top-left has smallest sum (x+y), bottom-right has largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    #top-right has smallest diff (y-x), bottom-left has largest diff
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def isolate_cards(image_path, rectangles):
    img = cv2.imread(image_path)
    
    #card size for output
    card_w, card_h = 250, 350

    for i, rect in enumerate(rectangles):

        pts = np.array(rect, dtype="float32")
        rect_ordered = order_corners(pts)

        # 2. Define where the points should go (flat 2D coordinates)
        dst = np.array([
            [0, 0],            # Top-Left
            [card_w - 1, 0],   # Top-Right
            [card_w - 1, card_h - 1], # Bottom-Right
            [0, card_h - 1]    # Bottom-Left
        ], dtype="float32")

        # 3. Calculate the Perspective Transform Matrix
        M = cv2.getPerspectiveTransform(rect_ordered, dst)

        # 4. Warp the image (flatten it)
        warped = cv2.warpPerspective(img, M, (card_w, card_h))

        # 5. Save
        save_path = f"output/cards/card{i+1}.jpg"
        cv2.imwrite(save_path, warped)


import cv2
import numpy as np

def isolate_cards(image_path, rectangles):
    img = cv2.imread(image_path)
    
    #card dimensions for output
    card_w, card_h = 250, 350
    
    #desired flattened corner positions
    transformation = np.array([
        [0, 0],                   #top-left
        [card_w - 1, 0],          #top-right
        [card_w - 1, card_h - 1], #bottom-right
        [0, card_h - 1]           #bottom-left
    ], dtype="float32")

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
        warped = cv2.warpPerspective(img, M, (card_w, card_h))

        cv2.imwrite(f"output/cards/card{i+1}.jpg", warped)
        #eventually we'll pass the card to the next function, instead of saving it