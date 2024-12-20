FloMo \\
This project is a system that analyzes video footage from multiple cameras along different roads (leading from a source to a destination), calculates traffic levels using a contour-based scoring method, and visualizes traffic conditions on a map. This allows users to make informed decisions about the best route to take at a given time, given the source and destination. The user will xpick the desired “time of interest” on the dial, pick the source and destination and be presented with a map of color-coded paths from the source to the destination, and the ETA.

--------------------------------------------------------------------
Pre-requisites
--------------------------------------------------------------------
Libraries or modules that need to be installed:
1.     CMU graphics. Note: this should be under the folder where you’ll install this TP project. More on that will come later in the ReadMe.
2.     OpenCV
3.     Numpy
4.     Pillow
[Dependencies:
cmu_graphics==1.1.37
numpy==1.24.3
opencv_python==4.10.0.84
Pillow==11.0.0]
 
--------------------------------------------------------------------
Files/folders reference:
--------------------------------------------------------------------
-       Folder - “traffic vids”: This is a folder of the videos I have screen recorded from PennDot. There are around 192 videos separated into folders named by the hour. There are 8 videos from 8 different streets for every hour. Here is a google drive link to all the videos: https://drive.google.com/drive/folders/1nJvvAcnCAL8rKl6ULqhYIs29DSFiXRoX?usp=drive_link
-       traffic-scoring.py: This is a python file of my code. The main part of it is my custom motion detection algorithm to detect traffic from the PennDot videos (above folder). It scores the traffic in each of the 192 videos and dumps the data into a json file.
-       traffic data.json: This is the json file that contains all the data of the traffic scores for the 8 cameras over 24 hours, as scores by my code in traffic-scoring.py.
-       path_finder.py: This is a separate file for my depth-first search function. I recursively find all paths from a user-chosen source to destination. This helps me find the ETA and mark the traffic on the two different routes the user can take from the source to the destination.
-       data.py: This is a file containing necessary data for my programs to run. It contains the cameraGraph which is a graph data structure storing all the cameras on the map, with their neighboring cameras. This is what I recursively iterate on to find all possible paths from the source to the destination while calculating ETA. It also contains cameraPaths - a dict where the key is a tuple of two cameras, and the value is the coordinates on the path between the two cameras. This assists in drawing the paths with their corresponding traffic color.
-       Image: splashscreen.png: This is an image of the splash screen I designed to display when my project is first launched.
-       Image: “Route-2-base.png”: This is an image of the base map (taken from PennDot). On this background map, my product carries out all its other functionalities.
-       cmu-color-path-5.py: This is the file that brings all of the above together. It contains UI design, invokes functions from path_finder, uses data from the data files to draw paths, and contains all the functions that are the essence of this project.
 

--------------------------------------------------------------------
Download and create Instructions:
--------------------------------------------------------------------
In this section, I will expand on where the above files/folders should be located on one's local disk so that the program can run. 
For the sake of this section, we will refer to the user’s base directory as “baseDir”.
 
1. Create Base Folder
   1. Make a folder called “Srishti TP”.
   2. Your baseDir is the path to this folder on your computer. Example <basedir> for me is, “/Users/srishtisatishwar/Desktop/CMU/sem-1/15-112/Term Project/“
   3. Remember to use "\" if working on Windows.
2. Download images and videos
   1. Download and move the splashscreen.png and Route-2-base.png and the folder “traffic vids” under the baseDir folder.
   2. For “traffic vids” directory use the download option.
3. Ensure cmu_graphics_installer  folder exists inside baseDir (Installed as part of CMU graphics package installation)
4. Download python and JSON files to <baseDir>/cmu_graphics_installer
   1. Download traffic-scoring.py, traffic data.json, path_finder.py, data.py, cmu-color-path-5.py and move them into baseDir/cmu_graphics_installer.
5. Update baseDir in cmu-color-path-5.py
   1. Open cmu-color-path-5.py and on Line 11, change the line to reflect your own baseDir. (it should look like: baseDir = “<entire path to your baseDir>”).
Folder Structure
The paths to all 8 files/folders should look like this:
* Traffic vids folder: “baseDir/traffic vids”
* splashscreen.png: “baseDir/splashscreen.png”
* Route-2-base.png: “baseDir/Route-2-base.png”
* traffic-scoring.py: “baseDir/cmu_graphics_installer/traffic-scoring.py”
* path_finder.py: “baseDir/cmu_graphics_installer/path_finder.py”
* cmu-color-path-5.py: “baseDir/cmu_graphics_installer/cmu-color-path-5.py”
* data.py: “baseDir/cmu_graphics_installer/data.py”
* traffic_data.json: “baseDir/cmu_graphics_installer/traffic data.json”
   * Disclaimer about traffic data.json: this is the json dump from when I ran traffic-scoring.py on my own computer. It takes around 10-15 mins to go through all 200 videos, contour them, detect the degree of change in motion and score the traffic (which is the data it dumps into a json). You are good to go with this file for TP demo. In case you want to re-generate this file, the instructions can be found later in the ReadMe.

--------------------------------------------------------------------
--------------------------------------------------------------------
Running Instructions:
--------------------------------------------------------------------
--------------------------------------------------------------------
 
Step – 1 (Optional Step). This step is optional. The traffic_data.json that is generated in this step is already shipped as part of the deliverable.
 
python3 traffic-scoring.py
 
In case you choose to run this, it will take 10-15 mins to run through all the videos and will dump a json file of the data it collected from the videos, at the very end.
 
Step – 2 Run the main program
 
python3 cmu-color-path-5.py
 
Run this from your terminal and it will pop up a new cmu graphics window with a User Interface that the user can use.
-       Click to the Start button to navigate to the map.
-       Follow the demo to explore the different functionalities of the product.
