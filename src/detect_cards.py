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

#helper for splitting river and hand areas
def split(image_path):
    img = cv2.imread(image_path)
    height, width, _ = img.shape

    river = img[0:height//2, 0:width]
    hand = img[height//2:height, 0:width]

    return river, hand

#main function for detecting possible cards in the image
def detect_rectangles(image):

    #resize image for consistency
    target_width = 600
    scale = target_width / image.shape[1] #keep scale for later use
    dim = (target_width, int(image.shape[0] * scale))
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    #grayscale and blur image for less noise
    grayscale = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(grayscale, (5, 5), 0)
    
    #bilateral filter to reduce noise while keeping sharp edges (card edges)
    blur = cv2.bilateralFilter(grayscale, 9, 75, 75)    

    #canny edge detection
    edges = cv2.Canny(blur, 50, 150)
    cv2.imwrite("output/edges.jpg", edges) #output edges for debugging

    #dilate to help reconnect edges
    kernel = np.ones((3,3), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)

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
            #found corners, scale them back up
            corners = [(pt[0][0] / scale, pt[0][1] / scale) for pt in approx]
            rectangles.append(corners)

    return rectangles
