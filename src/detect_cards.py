import cv2
import numpy as np

#helper for debugging, draws detected rectangles on image, eventually can use this for live feedback
def draw_rectangles(image_path, rectangles):
    img = cv2.imread(image_path)

    for rect in rectangles:
        pts = np.array(rect, dtype=np.int32).reshape((-1, 1, 2))
        cv2.polylines(img, [pts], isClosed=True, color=(0, 0, 255), thickness=4)
        # cv2.fillPoly(img, [pts], color=(0, 0, 255,)) #fill entirely

    cv2.imwrite("output/contours.jpg", img)


#main function for detecting possible cards in the image
def detect_rectangles(image_path):

    #load image 
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Failed to load image")

    #grayscale and blur image for less noise
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grayscale, (5, 5), 0)

    #canny edge detection
    edges = cv2.Canny(blur, 50, 150)
    cv2.imwrite("output/edges.jpg", edges) #output edges for debugging

    #find contours from edges
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    rectangles = []

    min_area=5000 #to filter out small countours (likely noise)
    for contour in contours:
        #skip small contours
        area = cv2.contourArea(contour)
        if area < min_area:
            continue

        #approximate contour to polygon
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

        #return polygons with 4 corners (rectangles)
        if len(approx) == 4:
            corners = [(pt[0][0], pt[0][1]) for pt in approx]
            rectangles.append(corners)

    return rectangles


if __name__ == "__main__":
    import sys

    #example images
    # image_path = "test_images/5cardsbasic.png"
    image_path = "test_images/5cardswithclutter.png"
    # image_path = "test_images/3cardswithclutter.png" #failure case, chip on card
    # image_path = "test_images/5cardswithhands.png" #failure case, stylized background
    # image_path = "test_images/boonecards4.png"
    
    #detect rectangles in image
    rects = detect_rectangles(image_path)

    #prints out detected rectangles
    # print("Rectangles detected:", len(rects))
    # for i, rect in enumerate(rects):
    #     print(f"Rectangle {i+1} corners:", rect)

    #draw detected rectangles on image
    draw_rectangles(image_path, rects)