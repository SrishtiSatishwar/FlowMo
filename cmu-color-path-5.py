from cmu_graphics import *
from path_finder import findPaths
from data import cameraGraph, cameraPaths
import numpy as np
from PIL import Image
import cv2
import os
import json

# base map image, video frame, scale factor globals
baseDir = "/Users/srishtisatishwar/Desktop/CMU/sem-1/15-112/Term Project/"
baseDirCMUGraphics = os.path.join(baseDir, "cmu_graphics_installer")
imagePath = os.path.join(baseDir, "Route-2-base.png")
splashScreenPath = os.path.join(baseDir, "splashscreen.png")
frame = None

# Open and read the JSON file
"""Lines 12-13 GPT-assisted"""
trafficDataPath = os.path.join(baseDirCMUGraphics, "traffic_data.json")
with open(trafficDataPath, 'r') as file:
    trafficData = json.load(file)


def onAppStart(app):
    app.displaySplashScreen = True
    app.paused = True
    app.videoPopup = None
    app.popupRect = None
    app.currentVideoFrame = None  # current video frame
    app.pathData = []  # holds path info for all cameras
    app.drawAllPaths = False  # flag to control path drawing
    app.etaPaths = [] 
    app.selectedMode = None  # to track if we're in ETA selection mode
    app.hintText = ""  # "pick start cam", "pick end cam"
    app.selectedCameraStart = None
    app.selectedCameraEnd = None
    app.pointSelected = (0, 0) # cam clicked by user
    # store the selected cameras and their traffic data for the given hour
    app.startCamera = None
    app.selectedHour = "16"

"""Drawing a CMUIMage: https://academy.cs.cmu.edu/cpcs-docs/images_and_sounds"""
def redrawAll(app):
    global frame, splashScreenPath
    if app.displaySplashScreen == True:
        originalImage = Image.open(splashScreenPath)
        scaledImage = originalImage.resize((800, 600))  # resize image to 800x600
        cmuImage = CMUImage(scaledImage)
        drawImage(cmuImage, 0, 0)
        drawRect(550, 480, 150, 50, fill="grey")
        drawLabel("Start", 625, 505, fill="white", size=20)
        return
    
    # fetch the current frame
    frameRGB = fetchImage(app)

    if frameRGB is not None:
        # convert frame to CMU Graphics Image
        cmuImage = CMUImage(Image.fromarray(frameRGB))
        drawImage(cmuImage, 0, 0)
        # if start coordinate is available, draw the line
        if hasattr(app, 'startCoordinates'): 
            lineColor = app.lineColor
            pathCoordinates = app.pathCoordinates
        
            # draw the line between the two points
            if pathCoordinates is not None :
                drawConnectingLines(pathCoordinates, lineColor)
            else : 
                print ("Clear connecting lines")

        # if a video popup is active
        if app.videoPopup and app.popupRect:
            x1, y1, width, height = app.popupRect
            if app.currentVideoFrame is not None:
                # Call helper function to render the popup
                drawVideoPopup(app, 0, 0, width, height, app.currentVideoFrame)
            else:
                print("No video frame available.")
        else:
            print("No active video popup.")

    # traffic button
    buttonWidth = 120
    buttonHeight = 40
    buttonX = 790 - buttonWidth
    buttonY = 600 - buttonHeight
    # draw traffic button
    drawRect(buttonX-50, buttonY-50, buttonWidth, buttonHeight, fill='darkgray', border="grey", borderWidth=1)
    drawLabel("Traffic", buttonX - 50 + buttonWidth / 2, buttonY - 50 + buttonHeight / 2,
               size=16, align='center', fill='black')
    
    # dial buttons
    dialX = buttonX - 50 + buttonWidth / 2
    dialY = buttonY - 70
    dialWidth = 120
    dialHeight = 40
    # draw the dial
    drawDial(app, dialCenterX=dialX, dialCenterY=dialY, 
              dialWidth=dialWidth, dialHeight=dialHeight)

    # draw ETA button
    drawRect(buttonX-50, buttonY-171, buttonWidth, buttonHeight, fill='darkgray',border="grey", borderWidth=1)
    drawLabel("ETA", buttonX - 50 + buttonWidth / 2, buttonY - 171 + buttonHeight / 2,
              size=16, align='center', fill='black')

    # draw timeline above the dial
    drawTimeline(app, dialX, dialY - 60, 24, 10)

    # draw traffic paths on click of traffic button
    if app.drawAllPaths:
        for pathInfo in app.pathData: 
            pathCoordinates = pathInfo["pathCoordinates"]
            lineColor = pathInfo["lineColor"]
            drawConnectingLines(pathCoordinates, lineColor)

    drawCamerasForEta(app)
    if hasattr(app, "etaPaths"):
        for pathInfo in app.etaPaths:
            # extract camera IDs from the path (a list of camera IDs)
            pathCameras = pathInfo[0]
            pathColor = pathInfo[1]
            pathTime = pathInfo[2]  # Total ETA for the path in minutes

            # calculating midpoint of the entire path
            totalX, totalY, totalPoints = 0, 0, 0

            # iterate over the path cameras and get pathcoordinates for each pair
            for i in range(len(pathCameras) - 1):
                # Get the current camera and the next camera in the path
                camera1 = pathCameras[i]
                camera2 = pathCameras[i + 1]
                
                # Ensure the pair is in both directions for matching
                pair1 = tuple(sorted([camera1, camera2]))  # This ensures the order doesn't matter
                pair2 = tuple(sorted([camera2, camera1]))  # Reverse pair

                # Check if the pair exists in cameraPaths (either direction)
                if pair1 in cameraPaths:
                    cameraPathcoords = cameraPaths[pair1]
                elif pair2 in cameraPaths:
                    cameraPathcoords = cameraPaths[pair2]
                else:
                    continue  # If the pair doesn't exist, skip it
                
                # Draw a line for each consecutive pair of coordinates
                for j in range(len(cameraPathcoords) - 1):
                    x1, y1 = cameraPathcoords[j]
                    x2, y2 = cameraPathcoords[j + 1]
                    drawLine(x1, y1, x2, y2, fill=pathInfo[1], lineWidth=6)

                    # Accumulate coordinates for midpoint calculation
                    totalX += (x1 + x2)
                    totalY += (y1 + y2)
                    totalPoints += 2

            # Calculate the midpoint of the path
            if totalPoints > 0:
                # Now, get the coordinates of the camera in the middle of the path (i.e., the middle camera)
                """The ideas from Line 159-164 were GPT-assisted"""
                middleCamera = pathCameras[len(pathCameras) // 2]
                if middleCamera in trafficData:
                    middleX, middleY = trafficData[middleCamera]["coordinates"]
                    # Adjust the y-coordinate to place the label above the camera
                    labelX = middleX
                    labelY = middleY - 50  # Adjust this value (50 or 100 pixels above the camera)
                    # Draw a white rectangle behind the label text
                    labelWidth = 100  # Width of the rectangle, adjust as needed
                    labelHeight = 30  # Height of the rectangle, adjust as needed
                    drawRect(labelX - labelWidth / 2, labelY - labelHeight / 2, labelWidth, labelHeight, fill="white")

                    # Display the ETA label above the middle camera
                    drawLabel(f"ETA - {pathTime:.2f} min", labelX, labelY, size=16, align="center", fill="black")


def onMousePress(app, mouseX, mouseY):
    if splashScreenButtonClicked(app, mouseX, mouseY):
        app.displaySplashScreen = False

    # point user clicked
    app.pointSelected = (mouseX, mouseY)
    # check if the click was on the < or > button of the dial
    hourChanged = handleDialClick(app, mouseX, mouseY)
    # check which camera clicked
    handleCameraClick(app, hourChanged)

    # check if ETA button clicked
    if isETAButtonClicked(mouseX, mouseY):
        return etaWorkflow(app)
    elif app.selectedMode == "ETA" :
        print(f"Mouse pressed and selected mode is ETA")
    else:
        resetETA(app)

    # check if traffic button was clicked or if all paths are drawn (toggle between painting and clearing paths)
    if isTrafficButtonClicked(mouseX, mouseY) or app.drawAllPaths is True:
        if (app.drawAllPaths is True and hourChanged is False):
            app.drawAllPaths = False
            app.pathData.clear()
        else:
            paintAllPaths(app)


def splashScreenButtonClicked(app, mouseX, mouseY):
    if (550 <= mouseX <= 700) and (480 <= mouseY <= 530):
        return True
    return False


def drawHintTextAboveEta(app):
    if app.hintText:
        # ETA button dimensions
        buttonWidth = 120
        buttonHeight = 40
        buttonX = 790 - buttonWidth - 50 
        buttonY = 600 - buttonHeight - 171

        # position the text above the ETA button
        hintX = buttonX - 50 + buttonWidth / 2
        hintX = buttonX + buttonWidth / 2
        hintY = buttonY - 10

        # hint text
        drawLabel(app.hintText, hintX, hintY, size=14, align="center", fill="black")


def drawCamerasForEta(app):
    # highlight all cameras if in ETA mode
    if app.selectedMode == "ETA":
        for cameraID, cameraData in trafficData.items():
            x, y = cameraData["coordinates"]
            if cameraID == app.selectedCameraStart:
                # highlight the source camera with blue border
                drawCircle(x, y, 20, fill=None, border="blue", borderWidth=6)
                drawLabel("Source", x, y-30, fill="black", size=15)
            if cameraID == app.selectedCameraEnd:
                # highlight the destination camera with green border
                drawCircle(x, y, 20, fill=None, border="green", borderWidth=6)
                drawLabel("Destination", x, y-30, fill="black", size=15)
            else:
                # all other cameras have a standard glow
                drawCircle(x, y, 20, fill=None, border="orange", borderWidth=3)
            # draw circ around camera
            drawCircle(x, y, 10, fill="black")
    # display hint text
    if app.hintText:
        drawHintTextAboveEta(app)



def IsTimeLineClicked(app, mouseX, mouseY, centerX, centerY):
    # timeline button
    hours = 24
    boxSizeX = 10
    boxSizeY = 40
    startX = centerX - (hours * boxSizeX) / 2
    startY = centerY
    # check if click is within timeline button
    if startY <= mouseY <= startY + boxSizeY:
        # determine which box was clicked
        for i in range(hours):
            boxX = startX + i * boxSizeX
            if boxX <= mouseX <= boxX + boxSizeX:
                app.selectedHour = str(i % 24).zfill(2)
                print (f"Selected hour from timeline is {app.selectedHour}")
                return True
    return False



def handleDialClick(app, mouseX, mouseY):
    # traffic button dimensions
    buttonWidth = 120
    buttonHeight = 40  
    # position of the traffic button
    buttonX = 790 - buttonWidth
    buttonY = 600 - buttonHeight

    # dials
    dialX = buttonX - 50 + buttonWidth / 2
    dialY = buttonY - 70
    dialCenterX = dialX
    dialCenterY = dialY
    dialWidth = 120
    dialHeight = 40

    # left and right button bounds
    leftButtonX1 = dialCenterX - dialWidth / 2 + 5
    leftButtonY1 = dialCenterY - dialHeight / 2
    leftButtonX2 = leftButtonX1 + dialHeight
    leftButtonY2 = leftButtonY1 + dialHeight
    rightButtonX1 = dialCenterX + dialWidth / 2 - dialHeight - 5
    rightButtonY1 = dialCenterY - dialHeight / 2
    rightButtonX2 = rightButtonX1 + dialHeight
    rightButtonY2 = rightButtonY1 + dialHeight

    # check if the mouse click is within the left button bounds
    if leftButtonX1 <= mouseX <= leftButtonX2 and leftButtonY1 <= mouseY <= leftButtonY2:
        # decrement the hour, wrap around at 0
        app.selectedHour = str((int(app.selectedHour) - 1) % 24).zfill(2) # learnt zfill from GPT
        return True

    # check if the mouse click is within the right button bounds
    elif rightButtonX1 <= mouseX <= rightButtonX2 and rightButtonY1 <= mouseY <= rightButtonY2:
        # increment the hour, wrap around at 23
        app.selectedHour = str((int(app.selectedHour) + 1) % 24).zfill(2)
        return True
    elif IsTimeLineClicked(app,mouseX, mouseY, dialCenterX, dialCenterY - 60):
        return True
    return False




def handleCameraClickForEta(app, x, y):
    if app.selectedMode != "ETA":
        return  # Only handle camera clicks in ETA mode

    found = None
    scaleFactor = 0.00428  # Scale factor to convert map units to miles
    # loop through cameras to find the clicked one
    for cameraID, cameraData in trafficData.items():
        camX, camY = cameraData["coordinates"]
        radius = 30  # Radius of the glowing circle
        # check if the user clicked near this camera
        if (camX - x)**2 + (camY - y)**2 <= radius**2:
            if app.selectedCameraStart is None:
                # set the source camera
                app.selectedCameraStart = cameraID
                app.hintText = "Click to select the destination camera."
                found = True
            elif app.selectedCameraEnd is None and cameraID != app.selectedCameraStart:
                # set the destination camera
                app.selectedCameraEnd = cameraID
                app.hintText = f"Route selected: {app.selectedCameraStart} -> {app.selectedCameraEnd}."
                found = True

                # find paths between start and end cameras - check path_finder for details on this function
                paths = findPaths(cameraGraph, app.selectedCameraStart, app.selectedCameraEnd)
                # compute scores and assign colors
                app.etaPaths = []
                for path in paths:
                    pathScores = [trafficData[camera]["scores"].get(app.selectedHour)for camera in path] # GPT-assisted
                    avgScore = sum(pathScores) / len(pathScores)
                    pathColor = mapScoreToColor(avgScore)  # function to map scores to colors
                    
                    # Compute total time for the path
                    totalTime = 0
                    for i in range(len(path) - 1):
                        camera1 = path[i]
                        camera2 = path[i + 1]
                        
                        # Get coordinates for the pair
                        """The idea of these sorted tuples was GPT-suggested"""
                        pair1 = tuple(sorted([camera1, camera2]))
                        pair2 = tuple(sorted([camera2, camera1]))
                        if pair1 in cameraPaths:
                            pathCoordinates = cameraPaths[pair1]
                        elif pair2 in cameraPaths:
                            pathCoordinates = cameraPaths[pair2]
                        else:
                            continue  # Skip if the pair is not found
                        
                        # Calculate time for each segment in the pair
                        segmentSpeed = mapColorToSpeed(pathColor)
                        for j in range(len(pathCoordinates) - 1):
                            coord1 = pathCoordinates[j]
                            coord2 = pathCoordinates[j + 1]
                            totalTime += computeSegmentTime(coord1, coord2, scaleFactor, segmentSpeed)

                    app.etaPaths.append((path, pathColor, totalTime))
                print (f"Found two paths {app.etaPaths}") 
                app.hintText = f"Route selected: {app.selectedCameraStart} -> {app.selectedCameraEnd}."
                found = True
            break

    if found is None :
        # clicked elsewhere, so resetting ETA workflow
        app.selectedMode = None
        app.selectedCameraStart = None
        app.selectedCameraEnd = None
        app.hintText = ""
        app.etaPaths = []
        return


def mapScoreToColor(avgScore):
    if avgScore <= 7:
        return "green"
    elif 8 <= avgScore <= 15:
        return "yellow"
    else:
        return "red"


def mapColorToSpeed(color):
    # map path color to average speed
    speedMap = {
        "red": 20,
        "yellow": 40,
        "green": 60
    }
    return speedMap.get(color, 40)


def handleCameraClick(app, hourChanged) :
    if app.selectedMode == "ETA":
        handleCameraClickForEta(app, app.pointSelected[0] , app.pointSelected[1])
        return
    # assume camera is not found on selected point and we have to close existing video if open
    closeVideo = True
    for camera, data in trafficData.items():
        cameraX, cameraY = data["coordinates"]
        # check if the clicked point is within a reasonable distance of the camera
        if abs(cameraX - app.pointSelected[0]) < 40 and abs(cameraY - app.pointSelected[1]) < 40:
            app.startCamera = camera
            print(f"Start camera selected: {camera}")
            closeVideo = False
            break
    # if start camera selected, calculate the line color based on traffic score
    if app.startCamera:
        startCoordinates = trafficData[app.startCamera]["coordinates"] # GPT-assisted for syntax
        selectedHourStr = str(app.selectedHour)
        # get traffic scores for the selected hour
        startScore = trafficData[app.startCamera]["scores"].get(selectedHourStr, 0) # GPT-assisted for syntax
        pathCoordinates = trafficData[app.startCamera].get("pathcoordinates", []) # GPT-assisted for syntax
        # calculate color based on the average score
        avgScore = startScore
        lineColor = mapScoreToColor(avgScore)

        app.lineColor = lineColor
        app.startCoordinates = startCoordinates
        app.pathCoordinates = pathCoordinates
        app.videoPopup = True 
        app.popupRect = True
        print ("app.startCamera = ", app.startCamera)
        print("app.selectedHour = ", app.selectedHour)
        fileName = app.startCamera + "-" + app.selectedHour + ".mov"
        videoPath = os.path.join(baseDir, "traffic vids/", app.selectedHour, fileName)
        (x, y) = startCoordinates
        openVideoPopup(app, videoPath, x, y)

    if closeVideo is True:
        app.videoPopup = None 
        app.popupRect = None


def computeEuclideanDistance(coord1, coord2):
    # compute euclidean distance between two coordinates
    x1, y1 = coord1
    x2, y2 = coord2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def computeSegmentTime(coord1, coord2, scaleFactor, speed):
    # compute time for a segment based on distance and speed
    distance = computeEuclideanDistance(coord1, coord2) * scaleFactor
    timeInHours = distance / speed
    timeInMinutes = timeInHours * 60
    return timeInMinutes


def closeVideoPopup(app):
    if app.videoCapture:
        app.videoCapture.release()


def openVideoPopup(app, videoPath, x, y):
    app.videoCapture = cv2.VideoCapture(videoPath)
    if app.videoCapture.isOpened():
        app.popupRect = (50, 50, 300, 200)
        app.videoPopup = True


def paintAllPaths(app):
    app.pathData = []  # list to hold the camera pairs and line colors
    for camera, data in trafficData.items():
        startScore = data["scores"].get(app.selectedHour, 0)
        # get the neighboring cameras
        connectedCameras = cameraGraph.get(camera, [])
        # path color based on the traffic score
        lineColor = mapScoreToColor(startScore)
        # iterate through each connected camera and prepare the path data
        for nextCamera in connectedCameras:
            # sorted tuple to ensure bi-directional paths are handled correctly - this idea was GPT-assisted
            cameraPair = tuple(sorted([camera, nextCamera]))
            if cameraPair in cameraPaths:
                pathCoordinates = cameraPaths[cameraPair]
                # Append the camera pair and corresponding line color to pathData
                app.pathData.append({
                    "cameraPair": cameraPair,
                    "pathCoordinates": pathCoordinates,
                    "lineColor": lineColor,
                })
    app.drawAllPaths = True



def etaWorkflow(app):
    app.selectedMode = "ETA"
    app.hintText = "Select a starting camera."
    app.lineColor = None
    app.pathCoordinates = None
    app.drawAllPaths = None
    return


def resetETA(app):
    app.selectedMode = "None"
    app.hintText = ""


def isETAButtonClicked(x, y): 
    # ETA button
    buttonWidth = 120 
    buttonHeight = 40
    buttonX = 790 - buttonWidth - 50
    buttonY = 600 - buttonHeight - 171

    # check if click is within the bounds of the button
    if buttonX <= x <= buttonX + buttonWidth and buttonY <= y <= buttonY + buttonHeight:
        return True
    return False


def isTrafficButtonClicked(x, y):
    # traffic button
    buttonWidth = 120 
    buttonHeight = 40
    buttonX = 790 - buttonWidth - 50
    buttonY = 600 - buttonHeight - 50
    
    # check if click is within the bounds of the button
    if buttonX <= x <= buttonX + buttonWidth and buttonY <= y <= buttonY + buttonHeight:
        return True
    return False



"""Most cv2 functions: https://docs.opencv.org/3.4/dd/d43/tutorial_py_video_display.html"""
def fetchImage(app):
    global frame
    # check if frame is already loaded. if yes, return the current frame
    if frame is None:
        print(f"Loading image from: {imagePath}")
        frame = cv2.imread(imagePath)  # OpenCV reads in BGR format

        if frame is None:
            print("Error: Unable to load image. Check the file path.")
            return None  # exit if the image is invalid

    # convert BGR to RGB
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    """Lines 554-564 of the fetchImage() was written with GPT assistance"""
    # resize the frame to match the CMU Graphics window size
    h, w, ch = frame.shape
    scaleFactor = min(app.width / w, app.height / h)
    newWidth = int(w * scaleFactor)
    newHeight = int(h * scaleFactor)

    targetSize = (800, 600) # app.width, app.height
    targetSize = (newWidth, newHeight)
    resizedFrame = cv2.resize(frameRGB, targetSize)
    return resizedFrame



def drawVideoPopup(app, x, y, width, height, videoFrame):
    # outer shadow for the popup
    drawRect(x - 2, y - 2, width + 4, height + 4, fill='darkgray')
    # rounded rectangle background
    drawRect(x, y, width, height, fill='black', border='white', borderWidth=2)

    titleHeight = 20
    drawRect(x, y, width, titleHeight, fill='lightgray')  # Title bar
    startCameraStreetName = camNameToStreetName(app.startCamera)
    drawLabel(f"{startCameraStreetName}", x + width / 2, y + titleHeight / 2, align='center', size=12, fill='black')

    """Lines 581-585 of drawVideoPopup() function was written with GPT assistance"""
    # Render the video frame inside the popup
    if videoFrame is not None:
        vResizedFrame = cv2.resize(videoFrame, (width, height - titleHeight))
        # convert frame to CMU Graphics Image
        cmuImageVideo = CMUImage(Image.fromarray(vResizedFrame))
        drawImage(cmuImageVideo, 0, 20)


def camNameToStreetName(camName):
    if camName == "RC1C1":
        streetName = "PLATT BRIDGE AT I-95"
    elif camName == "RC1C2":
        streetName = "PA 291 @ PLATTS BRIDGE" 
    elif camName == "RC1C3":
        streetName = "26TH ST @ PENROSE AVE" 
    elif camName == "RC2C1":
        streetName = "I-95 @ NB UPSTROKE GIRARD POINT BRIDGEE" 
    elif camName == "RC2C2":
        streetName = "I-95 @ GIRARD POINT BRIDGE" 
    elif camName == "RC2C3":
        streetName = "I-95 SB AT BROAD ST / SPORTS COMPLEX" 
    elif camName == "RC2C4":
        streetName = "S BRD ST @ PATTISON AVE" 
    elif camName == "RC2C5":
        streetName = "BROAD ST @ PATTISON AVE (NE CORNER)" 
    return streetName


"""this onStep() function was written with GPT assistance"""
def onStep(app):
   # check if a video popup is active
   if app.videoPopup and app.videoCapture:
       ret, vFrame = app.videoCapture.read()
       if ret:
           # convert the frame from BGR to RGB
           app.currentVideoFrame = cv2.cvtColor(vFrame, cv2.COLOR_BGR2RGB)
       else:
           # end of video or error handling
           print("End of video or error in video capture.")
           app.videoCapture.release()
           app.videoCapture = None
           app.videoPopup = False
           app.currentVideoFrame = None


def drawTimeline(app, centerX, centerY, hours, boxSize):
    # Calculate starting position for the timeline
    startX = centerX - (hours * boxSize) / 2
    startY = centerY
    boxSizeX = 10
    boxSizeY = 40
    
    if (app.startCamera is None or app.drawAllPaths is True) :
        selectedCamera = None
    else:
        selectedCamera = app.startCamera

    # determine the scores and colors
    if selectedCamera:
        scores = trafficData[selectedCamera]["scores"]
        colors = []
        for hour in range(hours):
            # get the score for the hour
            score = scores.get(f"{hour:02}", 0)
            color = mapScoreToColor(score)
            colors.append(color)
    else:
        colors = ["grey"] * hours

    # draw the timeline
    for i, color in enumerate(colors):
        boxX = startX + i * boxSizeX
        # highlight the selectedHour
        if i == int(app.selectedHour):
            # add glow effect
            drawRect(boxX - 3, startY - 3, boxSizeX + 6, boxSizeY + 6, fill=color, opacity=1)
            # draw a thicker border to pop out
            drawRect(boxX - 1, startY - 1, boxSizeX, boxSizeY + 2, fill=color, border="black", borderWidth=1)
        # draw the regular box
        drawRect(boxX, startY, boxSizeX - 2, boxSizeY - 2, fill=color)



def drawDial(app, dialCenterX, dialCenterY, dialWidth, dialHeight, bgColor="lightgray", btnColor="white", textColor="black"):
    # Draw dial background
    drawRect(dialCenterX - dialWidth / 2, dialCenterY - dialHeight / 2, dialWidth, dialHeight, fill=bgColor) #, border="black")

    # dial dimensions
    buttonWidth = 30
    buttonHeight = dialHeight - 4
    buttonMargin = 2
    # dial position
    leftButtonX = dialCenterX - dialWidth / 2 + buttonMargin
    leftButtonY = dialCenterY - buttonHeight / 2
    # dial position
    rightButtonX = dialCenterX + dialWidth / 2 - buttonWidth - buttonMargin
    rightButtonY = dialCenterY - buttonHeight / 2

    # draw left dial
    drawRect(leftButtonX, leftButtonY, buttonWidth, buttonHeight, fill=btnColor) #, border="black")
    drawLabel("<", leftButtonX + buttonWidth / 2, leftButtonY + buttonHeight / 2, size=16, align='center', fill=textColor)
    # draw right dial
    drawRect(rightButtonX, rightButtonY, buttonWidth, buttonHeight, fill=btnColor) #, border="black")
    drawLabel(">", rightButtonX + buttonWidth / 2, rightButtonY + buttonHeight / 2, size=16, align='center', fill=textColor)
    # draw selected hour in the center of the dial
    drawLabel(f"{app.selectedHour} hrs", dialCenterX, dialCenterY, size=14, align='center', fill=textColor)



def drawConnectingLines(pathCoordinates, lineColor):
    # ensure there are at least two points to connect
    if len(pathCoordinates) > 1:
        for i in range(len(pathCoordinates) - 1):
            x1, y1 = pathCoordinates[i]
            x2, y2 = pathCoordinates[i + 1]
            drawLine(x1, y1, x2, y2, fill=lineColor, lineWidth=6)



runApp(width=800, height=600)
