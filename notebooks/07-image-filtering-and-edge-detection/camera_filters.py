import cv2
import sys
import numpy

# Named mode values make the keyboard-selected processing branch easier to read.
PREVIEW  = 0  # Preview Mode
BLUR     = 1  # Blurring Filter
FEATURES = 2  # Corner Feature Detector
CANNY    = 3  # Canny Edge Detector

# Corner settings: at most 500 points; accept scores >= 0.2 of the best score;
# keep points at least 15 pixels apart; use a 9×9 neighborhood to score corners.
# Higher qualityLevel selects stronger corners; larger minDistance spreads them out.
# Larger blockSize measures structure over a wider neighborhood.
feature_params = dict(maxCorners=500, qualityLevel=0.2, minDistance=15, blockSize=9)

# Use camera index 0 by default; sys.argv[1] is an optional string filename/URL.
# Command-line values stay strings, so "0" here is not the integer camera index 0.
s = 0
if len(sys.argv) > 1:
    s = sys.argv[1]

# Start in preview mode; alive controls when the capture loop stops.
image_filter = PREVIEW
alive = True

# WINDOW_NORMAL allows manual resizing; result will hold the image to display.
win_name = "Camera Filters"
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
result = None

# VideoCapture accepts an integer camera index or a string video filename/stream URL.
source = cv2.VideoCapture(s)

# Read and process one frame at a time until the user quits or capture ends.
while alive:
    # read() returns (success, image); False can mean end of video or capture failure.
    # Typical camera frames are (H, W, 3) BGR NumPy arrays, dtype uint8 (0–255).
    has_frame, frame = source.read()
    if not has_frame:
        break

    # Mirror left/right for a natural webcam preview: 1 flips horizontally,
    # 0 flips vertically, and a negative value flips both axes.
    frame = cv2.flip(frame, 1)

    # Select the current filter; each branch produces the next displayed image.
    if image_filter == PREVIEW:
        # Assignment shares the same array; it does not copy the pixels.
        result = frame
    elif image_filter == CANNY:
        # Mark edges using low/high gradient thresholds 80/150: strong edges seed
        # connected weaker edges. Higher thresholds generally retain fewer edges.
        # Defaults use a 3×3 Sobel aperture and L1 gradient magnitude; output is
        # (H, W) uint8, with edge pixels 255 (white) and other pixels 0 (black).
        result = cv2.Canny(frame, 80, 150)
    elif image_filter == BLUR:
        # Average each channel over a 13×13 neighborhood; larger kernels smooth
        # more detail. Output keeps the frame's shape, BGR ordering, and dtype.
        result = cv2.blur(frame, (13, 13))
    elif image_filter == FEATURES:
        # Draw on the same BGR array so detected corners overlay the color preview.
        result = frame
        # Corner detection needs a single intensity channel: BGR → (H, W) grayscale.
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # ** expands the dictionary into keyword arguments. The default detector
        # finds Shi–Tomasi corners and returns (N, 1, 2) float32 (x, y) coordinates.
        corners = cv2.goodFeaturesToTrack(frame_gray, **feature_params)
        # No detected corners returns None, which cannot be reshaped or iterated.
        if corners is not None:
            # float32 ensures floating-point coordinates (normally already float32).
            # reshape(-1, 2) makes rows of (x, y); -1 infers N from the element count.
            # Loop unpacking assigns each row's coordinates; x is column, y is row.
            for x, y in numpy.float32(corners).reshape(-1, 2):
                # circle modifies result in place; centers require integer pixels.
                # Radius 10 and thickness 1 are pixels; -1 thickness would fill it.
                # (0, 255, 0) is green in BGR; larger radii/thickness make bigger marks.
                cv2.circle(result, (int(x), int(y)), 10, (0, 255, 0), 1)

    # Show the filtered frame; imshow supports both BGR and single-channel images.
    cv2.imshow(win_name, result)

    # Pump GUI events and poll for a key with a minimum 1 ms wait (-1 if no key).
    # ord() converts a one-character string to its code; accept either letter case.
    # The OpenCV window must have focus to receive these keys; 27 is Escape.
    key = cv2.waitKey(1)
    if key == ord("Q") or key == ord("q") or key == 27:
        alive = False
    elif key == ord("C") or key == ord("c"):
        image_filter = CANNY
    elif key == ord("B") or key == ord("b"):
        image_filter = BLUR
    elif key == ord("F") or key == ord("f"):
        image_filter = FEATURES
    elif key == ord("P") or key == ord("p"):
        image_filter = PREVIEW

# Free the capture device/file and close this window when the loop ends.
source.release()
cv2.destroyWindow(win_name)