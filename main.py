import numpy as np
import cv2

frame_list = []
frame_name_counter = 0
olives_counter = {"black": 0, "green": 0}

capture = cv2.VideoCapture('input_video.mp4')
capture.set(cv2.CAP_PROP_FPS, int(capture.get(cv2.CAP_PROP_FPS)))

while capture.isOpened():
    frame_is_read, current_frame = capture.read()
    if frame_is_read:
        if frame_name_counter == 0 or frame_name_counter == 70:
            frame_name = f"frame{str(frame_name_counter)}.jpg"
            cv2.imwrite(frame_name, current_frame)
            frame_list.append(frame_name)
            if frame_name_counter == 70:
                break
        frame_name_counter += 1
    else:
        break

#  crop first frame
cut_image = cv2.imread(frame_list[0])
crop_image = cut_image[1:500, 1:400]
cv2.imwrite(frame_list[0], crop_image)

for frame in frame_list:
    for color in olives_counter:
        image = cv2.imread(frame)
        image = cv2.GaussianBlur(image, (5, 5), 0)

        if color == 'black':
            lower = np.array([30, 10, 0])  # BGR
            upper = np.array([70, 70, 60])
            shapeMask = cv2.inRange(image, lower, upper)

            ret, thresh = cv2.threshold(shapeMask, 125, 255, 1)
            contours, h = cv2.findContours(thresh, 1, 2)

        elif color == 'green':
            lower = np.array([50, 130, 50])  # BGR
            upper = np.array([100, 160, 150])
            shapeMask = cv2.inRange(image, lower, upper)

            ret, thresh = cv2.threshold(shapeMask, 125, 255, 1)
            contours, h = cv2.findContours(thresh, 1, 2)

        for contour in contours:
            cv2.imwrite(f'{color}_olives_contour_{frame[:-4]}.jpg',
                        cv2.drawContours(image, [contour], 0, (0, 0, 255), 1))

        olives_counter[color] += len(contours)

for key in olives_counter.keys():
    print(f'{olives_counter[key]} {key} olives.')
