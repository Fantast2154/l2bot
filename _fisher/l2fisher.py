import math
import random
import time
from multiprocessing import Manager
from system.botnet import Client
import win32gui
import cv2


class Fisher:

    def __init__(self, fishing_window, fisher_id, number_of_fishers, q):
        # global current_state, supply_request, request_proceed, trading_is_allowed, requested_items_to_supply
        manager = Manager()
        self.exit_is_set = manager.list()
        self.exit_is_set.append(False)
        
        self.fishing_window = fishing_window
        self.fisher_id = fisher_id
        self.number_of_fishers = number_of_fishers
        self.q = q
        # self.fishing_service = fishing_service
        self.send_message(f'created')

        # communication with fisher service
        self.current_state = manager.list()
        self.current_state.append('not fishing')
        self.fishers_request = manager.list()
        self.fishers_request.append('')
        self.fishers_requested_supps = manager.list()
        self.fishers_requested_supps.append(0)
        # current_state params
        # 'not fishing'
        # 'fishing'
        # 'busy'
        # 'requests supplying'
        # 'paused'
        # 'error'

        # pause fisher
        self.paused = manager.list()
        self.paused.append(0)

       # trading
        # self.supplying_request = False # fisher wants supplying. options: True, False
        self.supplying_request = manager.list()
        self.supplying_request.append(False)
        self.supply_request_proceed = manager.list()
        self.supply_request_proceed.append(False)
        self.trading_is_allowed = manager.list()
        self.trading_is_allowed.append(False)
        self.requested_items_to_supply = manager.list()
        self.requested_items_to_supply_d = {}
        # self.requested_items_to_supply.append(10)
        # self.requested_items_to_supply.append(1)
        # self.requested_items_to_supply.append(12)

        # send/receive counters
        self.send_counter = 10000000000000
        self.receive_counter = 0
        self.attempt_counter = manager.list()
        self.attempt_counter.append(0)

        # fishing timers
        self.press_fishing_timer = manager.list()
        self.press_fishing_timer.append(time.time())
        self.total_fishing_time = 0
        self.last_rod_cast_time = 0
        self.avg_rod_cast_time = 0
        self.fishing_potion_timer = -4000
        self.alacrity_potion_timer = -4000
        self.buff_hawkeye_timer = -4000
        self.fishing_potion_rebufftime = 3600 - 40
        self.alacrity_potion_rebufftime = 1200 - 40
        self.buff_hawkeye_rebufftime = 1200 - 40
        self.position_correction_timer = time.time()
        self.absence_of_fishing_window_timer = 0

        # fishing params
        # if fisher_id == 0:
        #     self.reeling_skill_CD = 1.9
        #     self.pumping_skill_CD = 1.9
        # else:
        #     self.reeling_skill_CD = 2.3
        #     self.pumping_skill_CD = 2.3
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

        # test params
        self.time_since_last_rod_cast = time.time()
        self.time_between_rod_casts_avg = []

        # smart fishing params
        self.bar_limit_left = 0
        self.bar_limit_right = 0
        self.bar_length = 0

    def __del__(self):
        self.send_message(f"destroyed")

    def send_message(self, message):
        temp = '\t' * 11 * self.fisher_id + 'Fisher ' + f'{self.fisher_id}: {message}'
        print(temp)

    def test_action(self, count):
        self.q.new_task(count, self.fishing_window)

    def run(self):
        # function:
        # main fishing loop
        timer = time.time()
        run_hours = 6
        while not self.exit_is_set[0]:  # or keyboard was pressed and not disconnected
            if time.time() - timer > 3600*run_hours:
                self.pause_fisher()

            self.update_current_attempt()

            if not self.actions_while_fishing():
                pass
                # print('self.actions_while_fishing()')

            if not self.actions_between_fishing_rod_casts():
                self.send_message('actions_between_fishing_rod_casts FAILED')

            if self.paused[0] != 0:
                self.pause_fisher(self.paused[0])

        self.send_message(f'has finished fishing\n')
        self.current_state[0] = 'not working'

    def start_fishing(self):
        # function:
        # initial image search
        # initial rebuff
        # initial soski+baits correcting
        # choosing correct bait
        # recording game time
        # soski activation
        # trial rod case

        delay = 1
        delay_correction = delay + 9 * self.fisher_id
        self.send_message(f'will start fishing in .... {delay_correction} sec')
        self.pause_thread(delay_correction)

        if not self.fishing_window.init_search():
            self.stop_fisher()

        self.send_message(f'starts fishing')

        if not self.trial_rod_cast():
            self.send_message(f'trial rod cast FAILURE')
            self.stop_fisher()

        if not self.init_setup():
            pass

        self.fishing_window.start_accurate_search()
        self.pause_thread(1)

        # if not self.record_game_time():
        #     self.send_message(f'record_game_time FAILURE')
        #     self.stop_fisher()

        # self.send_message('rebuff')
        # self.choose_day_bait(search=True)
        # self.send_message('day baits has chosen FAILURE')
        # self.switch_soski(search=True)
        # self.send_message('soski turned ON')

        # if not self.overweight_baits_soski_correction():
        #     self.send_message('overweight_baits_soski_correction FAILURE')
        #     self.stop_fisher()

        self.current_state[0] = 'Fishing'
        self.run()

    def pause_fisher(self, delay=None):
        self.attack()
        if delay is None:
            self.send_message(f'paused permanently')
            inf_timer = 100000
            self.paused[0] = inf_timer
            while not self.exit_is_set[0]:
                if self.paused[0] == 0:
                    break
                self.pause_thread(1)
        else:
            self.send_message(f'paused for {delay} sec')
            if delay is None or delay == 0:
                pass
            else:
                self.paused[0] = delay
                for i in range(delay):
                    self.send_message(f'{delay - i} sec')
                    self.pause_thread(1)
                self.paused[0] = 0

    def stop_fisher(self):
        # global current_state
        self.send_message('self.exit_is_set[0]=True')
        self.exit_is_set[0] = True

    def trial_rod_cast(self):
        # function:
        # initial fishing window search
        # recording fishing window position
        # activation of accurate search in wincap
        self.move_to_supplier()
        self.move_to_supplier()
        self.fishing()
        self.pause_thread(1.5)
        if not self.search_object_with_click(self.fishing_window.get_object, self.fishing, 18, 'fishing_window', True):
            return False
        self.fishing_window.record_fishing_window()
        self.fishing()
        self.pause_thread(2)
        self.bar_limits()
        return True

    def actions_while_fishing(self):
        # function:
        # fishing algorithm

        # searching for fishing window
        if not self.search_object_with_click(self.fishing_window.is_fishing_window, self.fishing, 12):
            self.move_to_supplier()
            # if time.time() - self.absence_of_fishing_window_timer > 180:
            #     self.pause_fisher()
            #     return False
            # self.absence_of_fishing_window_timer = time.time()
            return False
        # self.absence_of_fishing_window_timer = 0
        self.press_fishing_timer[0] = time.time()
        # searching for clock
        counter = 1
        time_between_actions = 5
        temp_t = time.time()
        searching_time = 12.2
        fishing_fight_time = None
        while time.time() - temp_t < searching_time and not self.exit_is_set[0]:
            if not self.fishing_window.is_fishing_window():
                return False
            # if time.time() - temp_t > time_between_actions * counter:
            #     counter += 1
            #     self.attack()
            # if time.time() - temp_t > time_between_actions:
            #     counter += 1
            #     time_between_actions = 13
            #     self.attack()
            if self.fishing_window.is_clock():
                break
            time.sleep(0.5)
        fishing_fight_time = time.time()

        # fishing params
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
        extra_attack_check = False
        # self.attack()
        # fishing main loop

        while self.fishing_window.is_fishing_window() and not self.exit_is_set[0]:

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

                # SMART loop breaker depending on conditions

                # if not self.ai_fishing_breaker(x_border, fishing_fight_time):
                #     self.fishing()
                #     self.pause_thread(0.7)
                #     return True

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

                # if math.fabs(x_border - previous_position) >= 36:
                previous_position = x_border

        return True

    def actions_between_fishing_rod_casts(self):
        # function:
        # current attempts update
        # overweight and soski+baits correction if needed
        # rebuff if needed

        # if self.attempt_counter[0] == 1:
        # self.time_since_last_rod_cast = time.time()
        # return True
        # self.time_between_rod_casts_avg.append(time.time() - self.time_since_last_rod_cast)
        # self.time_since_last_rod_cast = time.time()
        # result = sum(self.time_between_rod_casts_avg) / len(self.time_between_rod_casts_avg)
        # self.send_message(f'Среднее время между забросами удочки {result}')
        # self.send_message(f'Средняя скорость ловли: {3600 // result} попыток в час')
        # self.attack()
        # self.attack()
        self.press_fishing_timer[0] = 0

        self.if_rebuff_time()

        if self.attempt_counter[0] == self.send_counter:
            self.attack()
            if not self.overweight_baits_soski_correction():
                self.send_message('overweight_baits_soski_correction FAILURE')

        self.fihser_position_correction()

        return True

    def fihser_position_correction(self):
        self.attack()
        t = 900
        if time.time() - self.position_correction_timer > t:
            self.move_to_supplier()
            self.position_correction_timer = time.time()


    def search_object_with_click(self, search_object, task_proc, searching_time, *args):
        counter = 0
        time_between_actions = 6
        repeat_times = searching_time // time_between_actions
        temp_timer = time.time()

        while not search_object(*args):

            if time.time() - temp_timer > time_between_actions * counter:
                counter += 1
                task_proc()
                self.pause_thread(0.5)

            if time.time() - temp_timer > searching_time or counter > repeat_times:
                return False
            self.pause_thread(0.1)
        return True

    def search_object_without_click(self, condition, searching_time, *args):
        temp_timer = time.time()

        while not condition(*args):

            if time.time() - temp_timer > searching_time:
                return False
            self.pause_thread(0.1)
        return True

    def hold_the_object_in_vision(self, condition, searching_time, *args):
        temp_timer = time.time()

        while condition(*args):
            if time.time() - temp_timer > searching_time:
                return True
            self.pause_thread(0.1)
        return False

    def smart_button_click(self):
        pass

    def bar_limits(self):
        [self.bar_limit_left, self.bar_limit_right] = self.fishing_window.wincap.bar_limits[self.fishing_window.hwnd]
        self.bar_limit_left -= 0.053
        self.bar_length = self.bar_limit_right - self.bar_limit_left

    def overweight_baits_soski_correction(self):

        self.send_message('overweight_baits_soski_correction')
        required_dbaits = 12
        required_nbaits = 1
        required_soski = 15

        if required_dbaits > 10 or required_nbaits > 10 or required_soski > 10:
            self.requested_items_to_supply.append(required_dbaits)  # dbaits
            self.requested_items_to_supply.append(required_nbaits)  # nbaits
            self.requested_items_to_supply.append(required_soski)  # soski

            self.requested_items_to_supply_d['dbaits'] = required_dbaits
            self.requested_items_to_supply_d['nbaits'] = required_nbaits
            self.requested_items_to_supply_d['soski'] = required_soski

            self.fishers_requested_supps[0] = self.requested_items_to_supply_d
            self.fishers_request[0] = 'requests supplying'
            # print('++++++++++++++++FISHER IS requests supplying', self.fishing_service.fishers_request)
            self.supply_request_proceed[0] = True
            self.current_state[0] = 'busy'
            self.trading_is_allowed[0] = True

            self.trading()

        return True

    def trading(self):
        self.current_state[0] = 'requests supplying'

        while not self.supply_request_proceed[0]:
            time.sleep(0.5)

        self.current_state[0] = 'busy'

        while not self.trading_is_allowed[0]:
            time.sleep(0.5)

        self.send_message('trading_is_allowed')
        self.fishing_window.stop_accurate_search()
        self.pause_thread(1)

        # waiting_time2 = 15
        # temp_timer2 = time.time()
        # while time.time() - temp_timer2 < waiting_time2 and not self.fishing_window.is_exchange_menu():
        #     self.send_trade_to_supplier()
        #     self.pause_thread(6)

        if not self.search_object_with_click(self.fishing_window.is_exchange_menu, self.send_trade_to_supplier, 15):
            return False

        if not self.search_object_without_click(self.fishing_window.is_exchange_menu, 120):
            return False

        waiting_time = 15
        temp = time.time()
        while self.fishing_window.is_exchange_menu and time.time() - temp < waiting_time:
            time.sleep(0.5)

        #self.hold_the_object_in_vision(self.fishing_window.is_exchange_menu, 15)

        self.smart_press_button('ok', self.fishing_window.is_exchange_menu, 15)

        # if self.fishing_window.is_exchange_menu:
        #     self.press_button('ok')

        self.supplying_request[0] = False
        self.supply_request_proceed[0] = False
        self.trading_is_allowed[0] = False
        self.requested_items_to_supply.pop()
        self.requested_items_to_supply.pop()
        self.requested_items_to_supply.pop()

        self.requested_items_to_supply_d['dbaits'] = 0
        self.requested_items_to_supply_d['nbaits'] = 0
        self.requested_items_to_supply_d['soski'] = 0

        self.current_state[0] = 'fishing'
        self.fishers_request[0] = ''
        #self.send_counter += 3

        self.fishing_window.start_accurate_search()

        self.pause_thread(1)

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

    def button_name(self, i):
        switcher = {
            'ok': 'ok_button',
            'confirm': 'confirm_button',
            'cancel': 'cancel_button'
        }
        return switcher.get(i, 'error')

    def ai_fishing_breaker(self, x, timer):
        if timer is not None:
            time_max = 22.8
            t = time_max - (time.time() - timer)
            if time_max > t > 0.7:
                y = (x - self.bar_limit_left) / self.bar_length

                # y_theory = (9.8467 * math.exp(0.1545 * t))/100
                # y_theory = (14.832 * math.log(t) + 54.153)/100
                y_theory = (3.653 * t + 19.635) / 100
                # self.send_message(f'y {y}, y_theory {y_theory}, y-y_theory {y - y_theory}')
                if y > y_theory:
                    self.send_message(f'Achtung! Я СДЕЛАЛ ЧТО МОГ. КАПИТУЛИРУЮ.')
                    self.send_message(f'{t} sec has been SAVED')
                    return False
        return True

    def smart_press_button(self, button_input, control_window, searching_time, *args):
        # function:
        # pushing button 'button input' every 5 seconds for 'searching time' until  window 'control_window' appears
        pause_between_clicks = 5
        temp_timer = time.time()
        button = self.button_name(button_input)
        if button != 'error':
            while control_window(*args):
                response = self.fishing_window.get_object(button, True)
                if response:
                    self.press_button(button_input)
                self.pause_thread(pause_between_clicks)

                if time.time() - temp_timer > searching_time:
                    return False
                time.sleep(0.5)
            return True
        else:
            return False

    def press_button(self, button_input):
        # function: 
        # Example: self.press_button('confirm') or 'ok' or 'cancel'
        # searching and pushing the button 'confirm'

        button = self.button_name(button_input)
        if button != 'error':
            param = button
        else:
            return False
        self.q.new_task('mouse',
                        [self.fishing_window.get_object(param, True), True, 'LEFT', False, False, False],
                        self.fishing_window)
        # coordinates, ,mouse_button, ...
        return True

    def click(self, coordinates):
        self.q.new_task('mouse',
                        [coordinates, True, 'LEFT', False, False, False],
                        self.fishing_window)

    def attack(self):
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('attack', False), True, 'LEFT', False, False, 'F4'],
                        self.fishing_window)
        # temp = self.fishing_window.is_pet_attack()
        # if temp:
        #     self.pause_thread(0.4)
        #     self.q.new_task('mouse',
        #                     [temp, True, 'LEFT', False, False, False],
        #                     self.fishing_window)
        #     self.pause_thread(0.1)

    def send_trade_to_supplier(self):
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('trade_supplier', False), True, 'LEFT', False, False, False],
                        self.fishing_window)

    def fishing(self):
        # self.q.new_task([(100, 100)], self.fishing_window.hwnd)
        # self.send_message('fishing')
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('fishing', False), True, 'LEFT', False, False, 'F1'],
                        self.fishing_window)

    def pumping(self):
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('pumping', False), True, 'LEFT', False, False, 'F2'],
                        self.fishing_window)
        # self.q.new_task('mouse', [[(100, 100)], True, 'LEFT', False, False, False], self.fishing_window)

    def reeling(self):
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('reeling', False), True, 'LEFT', False, False, 'F3'],
                        self.fishing_window)

    def rebuff(self, search=False):
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
        return True

    def update_current_attempt(self):
        self.attempt_counter[0] += 1
        temp = '\t' * 11 * self.fisher_id
        print(f'{temp}Fisher {self.fisher_id}: Attempt # {self.attempt_counter[0]}')

    def send_mail(self):
        pass

    def receive_mail(self):
        pass

    def send_trade(self):
        pass

    # def wait_for_trade(self):
    #     pass

    def change_bait(self):
        pass

    def map(self, search=False):
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('map_button', search), True, 'RIGHT', False, False, False],
                        self.fishing_window)

    def is_day_time(self):
        # if self.game_time is not None:
        return True

    def if_rebuff_time(self):
        self.attack()
        if time.time() - self.buff_hawkeye_timer > self.buff_hawkeye_rebufftime:
            self.rebuff_hawkeye()
        if time.time() - self.fishing_potion_timer > self.fishing_potion_rebufftime:
            self.rebuff_fishing_potion()
        if time.time() - self.alacrity_potion_timer > self.alacrity_potion_rebufftime:
            self.rebuff_alacrity()

    def rebuff_hawkeye(self):
        self.send_message('rebuff hawkeye')
        self.buff_hawkeye_timer = time.time()
        temp = self.fishing_window.is_hawk_buff()
        if temp:
            self.reeling_skill_CD = 1.9
            self.pumping_skill_CD = 1.9
            self.q.new_task('mouse', [temp, True, 'LEFT', False, False, False], self.fishing_window)
            self.pause_thread(2.5)
        else:
            self.buff_hawkeye_rebufftime = 10000000

    def rebuff_alacrity(self):
        self.send_message('rebuff alacrity')
        self.alacrity_potion_timer = time.time()
        temp = self.fishing_window.is_alacrity_potion_small()
        if temp:
            self.q.new_task('mouse', [temp, True, 'LEFT', False, False, False], self.fishing_window)
            self.pause_thread(0.7)
        else:
            self.alacrity_potion_rebufftime = 10000000

        # temp2 = self.fishing_window.is_alacrity_dex_warlock()
        # if temp2:
        #     self.q.new_task('mouse', [temp2, True, 'LEFT', False, False, False], self.fishing_window)
        #     self.pause_thread(6)

    def rebuff_fishing_potion(self):
        self.send_message('rebuff fishing potion')
        self.fishing_potion_timer = time.time()
        temp = self.fishing_window.is_fishing_potion_white()
        if temp:
            self.q.new_task('mouse', [temp, True, 'LEFT', False, False, False], self.fishing_window)
            self.pause_thread(0.7)
        else:
            self.fishing_potion_rebufftime = 10000000

    def move_to_supplier(self):
        temp = self.fishing_window.is_move_to_supplier()
        if temp:
            self.q.new_task('mouse', [temp, True, 'LEFT', False, False, False], self.fishing_window)
            self.pause_thread(2)

    def init_setup(self):
        self.if_rebuff_time()
        return True
