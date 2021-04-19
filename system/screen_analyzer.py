import numpy as np
import cv2 as cv
from threading import Thread, Lock


class DigitFinder:
    pass


class TimeRecognition:
    pass


class Vision:
    searching_image = None

    # THREADS EPTA
    points = None
    stopped = True
    lock = None

    # properties
    needle_img = None
    needle_w = 0
    needle_h = 0
    method = None
    threshold = None

    # constructor
    def __init__(self, needle_img_path, threshold, method=cv.TM_CCOEFF_NORMED):  # method=cv.TM_CCOEFF_NORMED
        self.threshold = threshold
        self.lock = Lock()
        # load the image we're trying to match
        self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)

        # save the dimensions of the needle image
        self.needle_w = self.needle_img.shape[1]
        self.needle_h = self.needle_img.shape[0]

        # there are 6 methods to choose from:
        # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        self.method = method

    def find(self, haystack_img, debug_mode=False, coordinates_and_sizes=False, message=False):
        # run the OpenCV algorithm
        result = cv.matchTemplate(haystack_img, self.needle_img, self.method)

        # Get the all the positions from the match result that exceed our threshold
        locations = np.where(result >= self.threshold)
        locations = list(zip(*locations[::-1]))
        # print(locations)

        # You'll notice a lot of overlapping rectangles get drawn. We can eliminate those redundant
        # locations by using groupRectangles().
        # First we need to create the list of [x, y, w, h] rectangles
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            # Add every box to the list twice in order to retain single (non-overlapping) boxes
            rectangles.append(rect)
            rectangles.append(rect)
        # Apply group rectangles.
        # The groupThreshold parameter should usually be 1. If you put it at 0 then no grouping is
        # done. If you put it at 2 then an object needs at least 3 overlapping rectangles to appear
        # in the result. I've set eps to 0.5, which is:
        # "Relative difference between sides of the rectangles to merge them into a group."
        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
        # print(rectangles)

        points = []
        pos_and_sizes = []
        if len(rectangles):
            # print('Found needle.')

            line_color = (0, 255, 0)
            line_type = cv.LINE_4
            marker_color = (255, 0, 255)
            marker_type = cv.MARKER_CROSS

            # Loop over all the rectangles
            for (x, y, w, h) in rectangles:

                # Determine the center position
                center_x = x + int(w / 2)
                center_y = y + int(h / 2)
                # Save the points
                points.append((center_x, center_y))
                pos_and_sizes.append((x, y, w, h))

                if debug_mode == 'rectangles':
                    # Determine the box position
                    top_left = (x, y)
                    bottom_right = (x + w, y + h)
                    # Draw the box
                    cv.rectangle(haystack_img, top_left, bottom_right, color=line_color,
                                 lineType=line_type, thickness=2)
                elif debug_mode == 'points':
                    # Draw the center point
                    cv.drawMarker(haystack_img, (center_x, center_y),
                                  color=marker_color, markerType=marker_type,
                                  markerSize=40, thickness=2)

        if debug_mode:
            cv.imshow('Matches', haystack_img)

        if coordinates_and_sizes:
            return pos_and_sizes

        else:
            if message:
                if len(points) > 0:
                    print(haystack_img, 'найден')
                else:
                    print(haystack_img, 'не найден')
            return points

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        # t.daemon = True
        t.start()

    def stop(self):
        self.stopped = True
        print(self.needle_img, 'searching process has been stopped!')

    def run(self):
        while not self.stopped:

            try:
                points = self.find(self.searching_image)
                self.lock.acquire()
                self.points = points
                self.lock.release()

            except:
                continue
