# SortMaster
---
# main.py
---
This code is a Python script that sorts and displays a collection of images from a folder. The program creates a GUI using the Tkinter library, and allows the user to sort the images by various criteria such as time of day, snow coverage, and the presence of an object in the image. The program loads all of the images from a folder specified by the user, and displays them one by one, allowing the user to assign metadata to each image (e.g. whether it contains an object, the time of day, etc.). The program saves the metadata to a CSV file and tracks the user's progress through the images. The script also uses the OpenCV library to display the images, and the PIL library to handle the images.

---
# day_night_sort.ipynb
---
The code imports several libraries including OpenCV, OS, and Numpy, as well as argparse for command-line argument parsing. The adjust_gamma function adjusts the gamma of an image using a lookup table. The code then sets the directory for the images to be processed, uses the glob function to obtain a list of image file paths in the directory, and loops through each image file. For each image, it applies the adjust_gamma function, converts the image to grayscale, calculates the average brightness of the image, and prints out the file path and whether the image is considered to be taken during the day or night based on its brightness. The threshold for classifying an image as taken during the night is an average brightness of 15.

---
# Using Sortmaster
---
The following document will detail how to access the trail cam photos, how to save progress made on classifying the objects, and how to reinitialize the program when needed. 

These steps are written by Mark Irby-Gill

---
## Accessing Trail Cam Photos 
---
1. Go to vlabs.rrcc.edu
2. Select 'Win10FsLogix' for the OS after logging in. 
3. Download the zip file from Sortmaster
4. Choose the destination of which to extract and save the file
5. Open Windows Powershell 
6. Type in the following command: 'pip3 install -r requirements.txt' -> spaces are required
7. Type in the following command: 'python main.py'
8. Open the windows 10 file manager in the VM and type in: '\\rrclkfsdatalab'
9. Select your assigned 'TrailCamsClass' folder
10. The trail cam classifier program will appear and it's interface ready for use.
---
## Saving Progress
1. Click on the 'progress.csv' file where the sortmaster program is saved
2. Open google drive on the VM and drag 'progress.csv' into it; preferrably a folder dedicated to containing any progress images you've made on previous occassions
---
## Reinitializing the Program
1. 
