from window_capture import WindowCapture
from screen_analyzer import Vision
import cv2 as cv
import keyboard
import time
import numpy as np
from operator import itemgetter

wincap = WindowCapture('Asterios')
vision_fishing = Vision('fishing.jpg', 0.87)

digits = [0] * 10
digits[0] = Vision('digits/0.jpg', 0.9)
digits[1] = Vision('digits/1.jpg', 0.9)
digits[2] = Vision('digits/2.jpg', 0.9)
digits[3] = Vision('digits/3.jpg', 0.9)
digits[4] = Vision('digits/4.jpg', 0.9)
digits[5] = Vision('digits/5.jpg', 0.9)
digits[6] = Vision('digits/6.jpg', 0.9)
digits[7] = Vision('digits/7.jpg', 0.9)
digits[8] = Vision('digits/8.jpg', 0.9)
digits[9] = Vision('digits/9.jpg', 0.9)

left_bracket = Vision('digits/(.jpg', 0.98)
right_bracket = Vision('digits/)_4.jpg', 0.98)
left_sq_bracket = Vision('digits/[.jpg', 0.97)
right_sq_bracket = Vision('digits/].jpg', 0.97)

weight_icon = Vision('weight.jpg', 0.9)


def digit_finder(image):
    m1 = time.time()
    digit_dict = {}

    left_bracket_pos_sq = left_sq_bracket.find(image)
    right_bracket_pos_sq = right_sq_bracket.find(image)
    left_bracket_pos = left_bracket.find(image)
    right_bracket_pos = right_bracket.find(image)

    if left_bracket_pos or right_bracket_pos:
        weight = False
    if left_bracket_pos_sq or right_bracket_pos_sq:
        left_bracket_pos = left_bracket_pos_sq
        right_bracket_pos = right_bracket_pos_sq
        weight = True

    print('l, r', left_bracket_pos, right_bracket_pos)
    # print('l, r', left_bracket_pos[-1][1], left_bracket_pos[-1][1])
    # print('l, r', left_bracket_pos[-1][0], right_bracket_pos[-1][0])
    # print('l, r', left_bracket_pos[-1][1], left_bracket_pos[-1][1])
    for id, digit in enumerate(digits):
        digit_pos = digit.find(image)  # digit_pos = [(), (), () ...] или [()]
        if digit_pos:
            digit_dict[id] = digit_pos
        else:
            digit_dict[id] = []

    temp_arr = []
    temp_dig_dict = {}
    temp_arr_weight = []
    temp_dig_dict_weight = {}
    try:
        for key, item in digit_dict.items():
            if item:
                for i in item:
                    if left_bracket_pos[-1][0] <= i[0] <= right_bracket_pos[-1][0]:
                        if left_bracket_pos[-1][1] - 5 <= i[1] <= left_bracket_pos[-1][1] + 5:
                            temp_arr.append(i)
                            if key in temp_dig_dict:
                                temp_dig_dict[key].append(i)
                            else:
                                temp_dig_dict[key] = [i]
                    if weight:
                        if left_bracket_pos[-2][0] <= i[0] <= right_bracket_pos[-2][0]:
                            if left_bracket_pos[-2][1] - 5 <= i[1] <= left_bracket_pos[-2][1] + 5:
                                temp_arr_weight.append(i)
                                if key in temp_dig_dict_weight:
                                    temp_dig_dict_weight[key].append(i)
                                else:
                                    temp_dig_dict_weight[key] = [i]
    except:
        return None

    sorted_digits_poses = sorted(temp_arr, key=itemgetter(0))
    string_digits = ''
    s = ''
    for pos in sorted_digits_poses:
        for key, item in temp_dig_dict.items():
            for i in item:
                if i == pos:
                    s = s + str(key)

    sorted_digits_weight_poses = sorted(temp_arr_weight, key=itemgetter(0))
    string_digits_weight = ''
    s_w = ''
    for pos in sorted_digits_weight_poses:
        for key, item in temp_dig_dict_weight.items():
            for i in item:
                if i == pos:
                    s_w = s_w + str(key)

    number, number2, number3 = None, None, None
    if s:
        number = int(s)
        # print(f'{number}')

    if s_w:
        number2 = int(s_w)
        # print(f'{number2}\n')

    if s and s_w:
        print()
        number3 = round(number2 / number * 100, ndigits=2)
        # print(f'{number3}%')

    m2 = time.time()
    print(f's = {s}, s_w = {s_w}, number3 = {number3}%')
    # print(f'number = {number}, number2 = {number2}, number3 = {number3}%')
    return number, number2, number3


if __name__ == '__main__':
    input('Go?')
    while True:
        # for i in range(5):
        #    print(5 - i)
        time.sleep(2)
        screenshot = wincap.capture_screen()

        # try:
        digit_finder(screenshot)
        cv.imshow('qw', screenshot)
        cv.waitKey(1)
        # except:
        #    print('Oi... не вижу циферки... простите')
