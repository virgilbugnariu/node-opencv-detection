import cv2
import numpy as np

windowTitle = 'Playground V2'
imageFilename = 'image.png'
image = None
iterations = 1
morphed = None
def main():
    global iterations
    global image

    cv2.namedWindow(windowTitle)
    image = cv2.imread(imageFilename)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    render()

def findContours():
    global image
    
    rows, cols = image.shape

    image = cv2.dilate(image, np.ones((5,5),np.uint8), iterations=2)
    
    contours, hierarchy = cv2.findContours(
        image, 
        cv2.RETR_TREE, 
        cv2.CHAIN_APPROX_SIMPLE
    )

    cv2.drawContours(
        image, 
        [max(contours, key = cv2.contourArea)], 
        -1, 
        (255, 255, 255),
        thickness = cv2.FILLED
    )

def morph():
    global image
    global morphed

    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (20,20)
    )

    morphed = cv2.morphologyEx(
        image,
        cv2.MORPH_ELLIPSE,
        kernel,
        iterations = 3
    )

def blobDetection():
    global morphed

    params = cv2.SimpleBlobDetector_Params()

    params.filterByColor = False
    params.filterByCircularity = True
    params.filterByConvexity = False
    params.filterByInertia = False
    
    params.minCircularity = 0.001

    params.filterByArea = True
    params.minArea = 0.001
    params.maxArea = 99999
    params.minDistBetweenBlobs = 0.1

    
    detector = cv2.SimpleBlobDetector_create(params)
    
    keypoints = detector.detect(morphed)
    
    markedBlobs = cv2.drawKeypoints(morphed, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    for keypoint in keypoints:
        print(keypoint.pt)
        print(keypoint.size)
    cv2.imshow('Blobs', markedBlobs)

def render():
    findContours()
    morph()
    blobDetection()

    cv2.imshow(windowTitle, morphed)


if __name__ == '__main__':
    main()
    while True:
        key = cv2.waitKey()
        if key == 27:
            break
        else:
            render()
            continue