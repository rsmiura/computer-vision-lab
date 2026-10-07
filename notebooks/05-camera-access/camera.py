import cv2
import sys

# Use camera index 0 by default; an optional command-line argument is a string
# filename or stream URL (sys.argv[0] is the script name, [1] is the first argument).
s = 0
if len(sys.argv) > 1:
    s = sys.argv[1]

# Open the camera/video source; integer indices select cameras, strings select files/URLs.
source = cv2.VideoCapture(s)

# WINDOW_NORMAL lets you resize the preview window manually.
win_name = 'Camera Preview'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

# Process window events and poll for a key each iteration; 1 requests a minimum
# 1 ms wait, and 27 is Escape's key code. Keep the preview window focused for keys.
while cv2.waitKey(1) != 27: # Escape
    # read() returns (success, image); failure can mean end of video or capture failure.
    # A typical color frame is a NumPy array of shape (H, W, 3), BGR, uint8 (0–255).
    has_frame, frame = source.read()
    if not has_frame:
        break
    # Display this frame in the named window; waitKey handles GUI events.
    cv2.imshow(win_name, frame)

# Release the capture device/file and close this preview window.
source.release()
cv2.destroyWindow(win_name)
