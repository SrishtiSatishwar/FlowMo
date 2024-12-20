import cv2
import numpy as np
import os
from cmu_graphics import *
from data import trafficData
import json


class MotionDetector:
    """Most cv2 functions: https://docs.opencv.org/3.4/dd/d43/tutorial_py_video_display.html"""
    def __init__(self, videoPath):
        self.cap = cv2.VideoCapture(videoPath) # creates a cv2.VideoCapture object to read frames from the video
        self.frameNumber = 0 # current frame

    def findConnectedComponents(self, binaryImage):
        h, w = binaryImage.shape
        """Reference for general use of numpy arrays: https://www.geeksforgeeks.org/numpy-array-in-python/"""
        visited = np.zeros_like(binaryImage, dtype=bool)  # Track visited pixels
        components = []  # List to store connected components

        # Moves for 4-connectivity: (row_delta, col_delta)
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        def searchAndMarkVisited(x, y):
            stack = [(x, y)]
            currentComponent = []
            while stack:
                cx, cy = stack.pop()
                # Skip already visited pixels or black pixels
                if visited[cx, cy] or binaryImage[cx, cy] == 0:
                    continue
                # Mark pixel as visited and add to current component
                visited[cx, cy] = True
                currentComponent.append((cy, cx))  # Store as (x, y)
                # Add unvisited neighbors
                for dx, dy in neighbors:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < h and 0 <= ny < w and not visited[nx, ny] and binaryImage[nx, ny] == 255:
                        stack.append((nx, ny))
            return currentComponent
        
        whitePixels = []
        mask = (binaryImage == 255)  # GPT-assisted
        for i in range(h):
            for j in range(w):
                if mask[i, j]:
                    whitePixels.append((i, j))

        for x, y in whitePixels:
            if not visited[x, y]:  # Start a new component only if not visited
                component = searchAndMarkVisited(x, y)
                if component:
                    components.append(component)
        return components
    

    def calculateAverageContours(self, connectedComponents):
            # Count valid contours
            contourCount = 0
            contourCountList = []

            # Iterate through each connected component
            for component in connectedComponents:
                if len(component) > 50:  # Ignore small contours
                    contourCount += 1
                    points = np.array(component)
                    hull = cv2.convexHull(points)  # Create a contour-like structure

            contourCountList.append(contourCount)
            if contourCountList:
                avgContours = sum(contourCountList) / len(contourCountList)
            else:
                avgContours = 0
            return avgContours

    def detect_movement(self):
            # set video reader to current frame
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.frameNumber)
            print(f"Current Frame : {self.frameNumber}")
            ret, frame = self.cap.read() # ret = success, frame = image data

            if not ret:
                print("End of video or error reading frame.")
                return None, None

            """Line 88-107: https://www.geeksforgeeks.org/python-grayscaling-of-images-using-opencv/ (used this link as a source, made my own necessary changes for frame differencing)"""
            # Convert current frame to grayscale
            grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Calculate the previous frame index, 10 frames behind the current frame
            previousFrameIndex = max(0, self.frameNumber - 10)
            print(f"Previous Frame : {previousFrameIndex}")
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, previousFrameIndex)

            # Capture the previous frame
            retPrev, previousFrame = self.cap.read()
            if not retPrev:
                print("Error reading previous frame.")
                return None, None

            previousGray = cv2.cvtColor(previousFrame, cv2.COLOR_BGR2GRAY)

            # Calculate the frame difference between current and delayed frame
            diffFrame = cv2.absdiff(previousGray, grayFrame)

            # Apply threshold to highlight moving parts
            _, fgMask = cv2.threshold(diffFrame, 30, 255, cv2.THRESH_BINARY)

            # Find connected components
            connectedComponents = self.findConnectedComponents(fgMask)

            # Count valid contours
            contourCount = 0
            contourCountList = []

            # Draw contours on the original frame
            outputFrame = frame.copy()
            for component in connectedComponents:
                if len(component) > 50:  # Ignore small components
                    contourCount += 1
                    points = np.array(component)
                    """Line 122, 130: https://docs.opencv.org/4.x/d7/d1d/tutorial_hull.html"""
                    hull = cv2.convexHull(points)  # Create a contour-like structure
                    cv2.drawContours(outputFrame, [hull], -1, (0, 255, 0), 2)
            contourCountList.append(contourCount)
            print ("CONTOUR COUNT = ", contourCount)
            avgContours = sum(contourCountList) / len(contourCountList)
            print ("SCORE = ", avgContours)
            return outputFrame, avgContours
    
    
    def run(self):
        lastAvgContours = None  # Initialize to store the last score
        while self.cap.isOpened():
            outputFrame, avgContours = self.detect_movement()
            if outputFrame is None:
                break

            """Line 140: https://www.geeksforgeeks.org/python-grayscaling-of-images-using-opencv/"""
            #cv2.imshow("Motion Contours", outputFrame) 
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            self.frameNumber += 10
            lastAvgContours = avgContours  # Store the latest score

        """General CV2 understanding: https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html"""
        self.cap.release()
        cv2.destroyAllWindows()
        return lastAvgContours  # Return the final score after processing all frames



"""Path joining: https://www.geeksforgeeks.org/python-os-path-join-method/"""
# Path to the main "traffic vids" directory
mainFolderPath = "/Users/srishtisatishwar/Desktop/CMU/sem-1/15-112/Term Project/traffic vids/"
scores_dict = dict()
# Iterate through folders named 00 to 23
for folder_name in [f"{i:02}" for i in range(24)]:
    folder_path = os.path.join(mainFolderPath, folder_name)
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        print(f"Folder {folder_name} does not exist. Skipping.")
        continue
    # Get all .mov files in the current folder
    video_files = [f for f in os.listdir(folder_path) if f.endswith('.mov')] # GPT-assisted
    for video_file in video_files:
        videoPath = os.path.join(folder_path, video_file)
        detector = MotionDetector(videoPath)
        avgContours = detector.run()  # This now returns the final score for the video
        camera_name = os.path.basename(video_file) # video file name = camera name
        # Initialize a nested dictionary for the camera if it doesn't exist
        if camera_name not in scores_dict:
            scores_dict[camera_name] = {}
        # Store the score for the specific folder
        scores_dict[camera_name] = avgContours



for camera in scores_dict:
    cam_name = camera[: 5]  # Extracts "RC1C1"
    print ("cam_name = ", cam_name)
    time = camera[6: 8]  # Extracts "00", "01", etc.
    score = scores_dict[camera]  # Gets the score value from scores_dict
    # Update the trafficData dictionary
    #if cam_name in trafficData and "scores" in trafficData[cam_name]:
    trafficData[cam_name]["scores"][time] = score # GPT assistance for syntax


# path to save the JSON file
outputFilePath = "/Users/srishtisatishwar/Desktop/CMU/sem-1/15-112/Term Project/cmu_graphics_installer/traffic_data.json"
# write trafficData to a JSON file
"""JSON dump assisted by GPT"""
with open(outputFilePath, 'w') as json_file:
    json.dump(trafficData, json_file, indent=4)
print(f"Traffic data has been written to {outputFilePath}")


