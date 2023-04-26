import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

print(os.getcwd())
# Load the image
img = cv2.imread('modules/facial_animation/frontal_face/face.png')

# Load the Haar Cascade Classifier for face detection
face_cascade = cv2.CascadeClassifier(
    'modules/facial_animation/frontal_face/haarcascade_frontalface_default.xml')

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect the face in the image
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

# Draw a rectangle around the detected face
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

# Create a figure object and set the limits for x and y axis
fig, ax = plt.subplots()
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)

# Create an empty list for x and y coordinates
xdata, ydata = [], []

# Create a line object using plot() function
line, = ax.plot([], [], lw=2)

# Define a function to update the line object for each frame of the animation


def update(frame):
    # Generate random x and y coordinates
    x = np.random.randint(0, 100)
    y = np.random.randint(0, 100)

    # Append the x and y coordinates to the lists
    xdata.append(x)
    ydata.append(y)

    # Update the line object with the new x and y coordinates
    line.set_data(xdata, ydata)

    # Return the line object
    return line,


# Use FuncAnimation() function to create the animation
ani = FuncAnimation(fig, update, frames=100, blit=True)

# Display the image and animation
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()
