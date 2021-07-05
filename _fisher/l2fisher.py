import math
import random
import time
from multiprocessing import Manager

import win32gui
import cv2


class Fisher:

    def __init__(self, fishing_window, fisher_id, number_of_fishers, q):
        self.fishing_window = fishing_window
        self.fisher_id = fisher_id
        self.number_of_fishers = number_of_fishers
        self.current_state = 0
        self.q = q
        self.send_message(f'created')
        manager = Manager()
        self.new_task_temp = manager.list()

        # fisher params
        # 0 - not fishing
        # 1 - fishing
        # 2 - busy with actions (mail,trade and etc.)
        # 8 - paused
        # 9 - error/stucked
        self.paused = None

        # send/receive counters
        self.send_counter = 0
        self.receive_counter = 0
        self.attempt_counter = 0

        # fishing timers
        self.total_fishing_time = 0
        self.last_rod_cast_time = 0
        self.avg_rod_cast_time = 0
        self.buff_time = time.time()

        # fishing params
        # self.reeling_skill_CD = 2.32
        # self.pumping_skill_CD = 2.13
        self.reeling_skill_CD = 2.3
        self.pumping_skill_CD = 2.3
        self.pumping_CD = 1.05

        # overweight, soski, baits
        self.current_baits = None
        self.max_weight = 0
        self.used_weight = 0
        self.baits_colored = 0
        self.baits_luminous = 0
        self.soski = 0
        self.baits_colored_max = 0
        self.baits_luminous_max = 0
        self.soski_max = 0

        self.game_time = None

        # connection params
        self.bot_is_connected = True
        self.it_is_almost_server_restart_time = False

    def __del__(self):
        self.send_message(f"destroyed")

    def send_message(self, message):
        temp = '\t' * 10 * self.fisher_id + 'Fisher ' + f'{self.fisher_id}: {message}'
        print(temp)

    def test_action(self, count):
        self.q.new_task(count, self.fishing_window)

    def pause_fisher(self, delay):
        if delay is None:
            pass
        else:
            self.pause_thread(delay)

    def run(self):

        if not self.start_fishing():
            self.stop_fishing()
            self.send_message('ERROR start_fishing()')

        while True:  # or keyboard was pressed and not disconnected

            self.update_current_attempt()

            if not self.actions_while_fishing():
                pass
                # print('self.actions_while_fishing()')

            if not self.actions_between_fishing_rod_casts():
                self.send_message('actions_between_fishing_rod_casts FAILED')

        if not self.stop_fishing():
            self.send_message('ERROR stop_fishing()')
            return

    def start_fishing(self):
        self.current_state = 0
        delay = 1.5
        delay_correction = delay + 6 * self.fisher_id
        self.send_message(f'will start fishing in ........ {delay_correction} sec')
        self.pause_thread(delay_correction)

        if not self.fishing_window.init_search():
            self.stop_fishing()

        self.send_message(f'starts fishing')

        if not self.trial_rod_cast():
            self.send_message(f'trial rod cast FAILURE')
            self.stop_fishing()

        # if not self.record_game_time():
        #     self.send_message(f'record_game_time FAILURE')
        #     self.stop_fishing()

        # self.rebuff(search=True)
        # self.send_message('rebuff')
        # self.choose_day_bait(search=True)
        # self.send_message('day baits has chosen FAILURE')
        # self.switch_soski(search=True)
        # self.send_message('soski turned ON')

        # if not self.overweight_baits_soski_correction():
        #     self.send_message('overweight_baits_soski_correction FAILURE')
        #     self.stop_fishing()

        return True

    def trial_rod_cast(self):

        if not self.search_loop_with_click(self.fishing_window.get_object, self.fishing, 10, 'fishing_window', True):
            return False
        self.fishing_window.record_fishing_window()
        self.fishing_window.start_accurate_search()
        self.fishing()
        self.pause_thread(2)
        return True

    def actions_while_fishing(self):

        if not self.search_loop_with_click(self.fishing_window.is_fishing_window, self.fishing, 12):
            return False

        # if not self.search_loop_with_click(self.fishing_window.get_object, self.fishing, 10, 'fishing_window', True):
        #     return False

        # if not self.search_loop_without_click(self.fishing_window.is_clock, 12):
        #     return False

        # if not self.search_loop_without_click(self.fishing_window.get_object, 10, 'clock', True):
        #     return False

        blue_bar_pos = 0
        coords_saved = False
        x_border = None
        previous_position = None
        pump_skill_cast_time = 0
        reeling_skill_cast_time = 0
        pump_was_pressed = False
        reel_was_pressed = False
        pump_timer_was_set = False
        pumping_time = time.time()
        reeling_time = time.time()
        reel_count = 0
        reel_timer_was_set = False

        while self.fishing_window.is_fishing_window():
        # while self.fishing_window.get_object('clock', True):

            if self.is_day_time():
                temp = self.fishing_window.is_blue_bar()
            else:
                temp = self.fishing_window.is_red_bar() + self.fishing_window.is_red_bar()
            # if self.is_day_time():
            #     temp = self.fishing_window.get_object('blue_bar', True)
            # else:
            #     temp = self.fishing_window.get_object('blue_bar', True) + self.fishing_window.get_object('red_bar', True)

            if temp:
                (x_temp, y_temp) = temp[-1]
                # self.send_message(f'temp {temp[-1]}')
                x_border = x_temp
            elif self.fishing_window.is_clock():
                delta_pump_skill = time.time() - pump_skill_cast_time
                if delta_pump_skill >= self.pumping_skill_CD:
                    self.pumping()
                    pump_skill_cast_time = time.time()

            if not coords_saved and (x_border != None):
                pumping_time = time.time()
                coords_saved = True
                previous_position = x_border
                # self.send_message('COORDS SAVED!!!!')
            # self.send_message(previous_position - x_border)
            if previous_position != None and x_border != None:
                delta_pump_skill = time.time() - pump_skill_cast_time
                delta_reel_skill = time.time() - reeling_skill_cast_time

                if pump_was_pressed and 15 <= x_border - previous_position < 45 and delta_reel_skill >= self.reeling_skill_CD:
                    pump_was_pressed = False
                    reel_count = 0
                    self.reeling()
                    reeling_skill_cast_time = time.time()
                    # self.send_message('ОШИБКА PUMP. ИСПРАВЛЯЮ.')

                elif reel_was_pressed and 15 <= x_border - previous_position < 45 and delta_pump_skill >= self.pumping_skill_CD:
                    reel_was_pressed = False
                    reel_count = 0
                    self.pumping()
                    pump_skill_cast_time = time.time()
                    # self.send_message('ОШИБКА REEL. ИСПРАВЛЯЮ.')

                # if x_border != previous_position:
                if 10 > math.fabs(x_border - previous_position) > 3:  # было not < 3
                    pumping_time = time.time()

                if x_border - previous_position < 4:
                    if not pump_timer_was_set:
                        pump_timer_was_set = True
                        pumping_time = time.time()

                    delta = time.time() - pumping_time  # NEW
                    delta_pump_skill = time.time() - pump_skill_cast_time
                    if delta >= self.pumping_CD and delta_pump_skill >= self.pumping_skill_CD:  # NEW
                        pump_timer_was_set = False
                        reel_count = 0
                        self.pumping()
                        pump_skill_cast_time = time.time()
                        pump_was_pressed = True
                        reel_was_pressed = False

                elif 4 <= x_border - previous_position < 12:
                    reel_count += 1
                    delta_reel_skill = time.time() - reeling_skill_cast_time

                    # if reel_count > 0 and delta_reel_skill >= self.reeling_skill_CD:
                    if delta_reel_skill >= self.reeling_skill_CD:  # reel_count > 1
                        reel_count = 0
                        self.reeling()
                        reeling_skill_cast_time = time.time()
                        reel_was_pressed = True
                        pump_was_pressed = False
                        pump_timer_was_set = False  # NEW
                        # print(x_border - previous_position, 'REEL')

                        if not reel_timer_was_set:
                            reel_timer_was_set = True
                            reeling_time = time.time()

                        if time.time() - reeling_time >= self.reeling_skill_CD:
                            reel_timer_was_set = False

                #if math.fabs(x_border - previous_position) >= 36:
                previous_position = x_border

        return True

    def actions_between_fishing_rod_casts(self):
        return True

    def stop_fishing(self):
        self.send_message(f'has finished fishing\n')
        self.paused = True
        self.current_state = 9

    def search_loop_with_click(self, search_object, task_proc, searching_time, *args):
        counter = 0
        time_between_actions = 5
        repeat_times = searching_time // time_between_actions
        temp_timer = time.time()

        while not search_object(*args):

            if time.time() - temp_timer > time_between_actions * counter:
                counter += 1
                task_proc()

            if time.time() - temp_timer > searching_time or counter > repeat_times:
                return False

        return True

    def search_loop_without_click(self, condition, searching_time, *args):
        temp_timer = time.time()

        while not condition(*args):
            if time.time() - temp_timer > searching_time:
                return False
        return True

    def get_status(self):
        return self.current_state

    def overweight_baits_soski_correction(self):
        self.send_message('overweight_baits_soski_correction')
        return True

    def buff_is_active(self):
        if time.time() - self.buff_time < 30:
            return False
        else:
            return True

    def got_the_bait(self):
        pass

    def pause_thread(self, delay):
        # self.send_message(f'PAUSED for {delay} seconds')
        time.sleep(delay)

    def fishing(self):
        # self.q.new_task([(100, 100)], self.fishing_window.hwnd)
        # self.send_message('fishing')
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('fishing', False), True, 'LEFT', False, False, False],
                        self.fishing_window)

    def pumping(self):
        # self.send_message('pumping')
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('pumping', False), True, 'LEFT', False, False, False],
                        self.fishing_window)
        # self.q.new_task('mouse', [[(100, 100)], True, 'LEFT', False, False, False], self.fishing_window)

    def reeling(self):
        # self.send_message('reeling')
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('reeling', False), True, 'LEFT', False, False, False],
                        self.fishing_window)
        # self.q.new_task('mouse', [[(500, 500)], True, 'LEFT', False, False, False], self.fishing_window)

    def rebuff(self, search=False):
        self.send_message('rebuff')
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('buff', search), True, 'LEFT', False, False, False],
                        self.fishing_window)
        self.buff_time = time.time()
        self.pause_thread(1.5)

    def switch_soski(self, search=False):
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('soski', search), True, 'RIGHT', False, False, False],
                        self.fishing_window)

    def choose_night_bait(self, search=False):
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('luminous', search)[1], True, 'RIGHT', False, False, False],
                        self.fishing_window)
        self.current_baits = 'n_baits'
        self.pause_thread(0.7)

    def choose_day_bait(self, search=False):
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('colored', search)[0], True, 'RIGHT', False, False, False],
                        self.fishing_window)
        self.current_baits = 'd_baits'
        self.pause_thread(0.7)

    def equipment_bag(self):
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('equipment_bag', False), True, 'RIGHT', False, False, False],
                        self.fishing_window)

    def record_game_time(self):
        self.send_message('record_game_time')
        # self.game_time = None
        return True

    def update_current_attempt(self):
        self.attempt_counter += 1
        temp = '\t' * 10 * self.fisher_id
        print(f'{temp}Fisher {self.fisher_id}: Attempt # {self.attempt_counter}')

    def send_mail(self):
        pass

    def receive_mail(self):
        pass

    def send_trade(self):
        pass

    def wait_for_trade(self):
        pass

    def change_bait(self):
        pass

    def map(self, search=False):
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('map_button', search), True, 'RIGHT', False, False, False],
                        self.fishing_window)

    def is_day_time(self):
        # if self.game_time is not None:
        return True
