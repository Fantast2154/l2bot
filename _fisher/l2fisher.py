import math
import random
import time
from multiprocessing import Manager
import keyboard
from system.botnet import Client
import win32gui
import cv2


class Fisher:

    def __init__(self, fishing_window, fisher_id, number_of_fishers, q):
        self.fisher_id = fisher_id
        self.send_message(f'created')
        # global current_state, supply_request, request_proceed, trading_is_allowed, requested_items_to_supply
        manager = Manager()
        self.exit_is_set = manager.list()
        self.exit_is_set.append(False)
        self.nickname = manager.list()
        self.nickname.append(None)
        self.fishing_window = fishing_window

        self.number_of_fishers = number_of_fishers
        self.q = q
        # self.fishing_service = fishing_service

        # communication with fisher service
        self.current_state = manager.list()
        self.current_state.append('not fishing')
        self.fishers_request = manager.list()
        self.fishers_request.append('')
        self.fishers_requested_supps = manager.list()
        self.fishers_requested_supps.append(0)
        self.supply_now = manager.list()
        self.supply_now.append(False)
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
        self.overweight_request_proceed = manager.list()
        self.overweight_request_proceed.append(False)
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
        self.send_counter = 700
        # if self.fisher_id == 0:
        #     self.send_counter = 4
        # if self.fisher_id == 1:
        #     self.send_counter = 6
        self.next_supplying_counter = self.send_counter
        self.receive_counter = 0
        self.attempt_counter = manager.list()
        self.attempt_counter.append(0)

        # fishing timers
        self.press_fishing_timer = manager.list()
        self.press_fishing_timer.append(time.time())
        self.total_fishing_time = 0
        self.last_rod_cast_time = 0
        self.avg_rod_cast_time = 0
        self.fishing_potion_timer = 999999999999
        self.alacrity_potion_timer = 999999999999
        self.buff_hawkeye_timer = 999999999999
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
        self.reeling_skill_CD = 1.9
        self.pumping_skill_CD = 1.9
        self.pumping_CD = 1.05

        # overweight, soski, baits
        self.current_baits = None
        self.max_weight = 0
        self.used_weight = 0
        self.baits_max = 1300
        self.soski_max = 5000
        self.soski_pet_max = 1000
        self.soski = 0
        self.baits = 0
        self.soski_pet = 0

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
        del self.attempt_counter
        self.send_message(f'=destroyed=')

    def send_message(self, message):
        temp = '\t' * 11 * (self.fisher_id + 1) + 'Fisher ' + f'{self.fisher_id}: {message}'
        print(temp)

    def test_action(self, count):
        self.q.new_task(count, self.fishing_window)

    def run(self):
        # function:
        # main fishing loop

        while not self.exit_is_set[0]:  # or keyboard was pressed and not disconnected

            self.update_current_attempt()

            if not self.actions_while_fishing():
                pass
                # print('self.actions_while_fishing()')

            if self.paused[0] != 0:
                self.pause_fisher(self.paused[0])

            if not self.actions_between_fishing_rod_casts():
                self.send_message('actions_between_fishing_rod_casts FAILED')

        self.send_message(f'has finished fishing\n')
        self.current_state[0] = 'not fishing'

    def start_fishing(self):
        # function:
        # initial image search
        # initial rebuff
        # initial soski+baits correcting
        # choosing correct bait
        # recording game time
        # soski activation
        # trial rod case
        self.current_state[0] = 'not fishing'
        delay = 7
        delay_correction = delay + 17 * self.fisher_id
        self.pause_thread(delay_correction)
        self.send_message(f'fisher will start in ...{delay_correction}')

        self.init_setup()

        self.activate_soski()
        self.activate_soski_pet()

        if not self.trial_rod_cast():
            self.send_message(f'trial rod cast FAILURE')
            self.stop_fisher()

        self.if_rebuff_time()

        # if self.number_of_fishers > 1:
        #     delay = 17 * (self.number_of_fishers - self.fisher_id - 1) + self.fisher_id * 2
        #     self.send_message(f'will start fishing in .... {delay} sec')
        #     self.pause_thread(delay)

        self.pause_thread(2)

        self.fishing_window.start_accurate_search()
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
        self.send_message(f'starts fishing')
        self.current_state[0] = 'fishing'
        self.run()

    def pause_fisher(self, delay=None):
        self.attack()
        if delay is None:
            self.send_message(f'paused permanently')
            self.current_state[0] = 'paused'
            inf_timer = 100000
            self.paused[0] = inf_timer
            while not self.exit_is_set[0]:
                if self.paused[0] == 0:
                    break
                self.pause_thread(1)
            self.send_message('unpaused')
            self.pause_thread(2 * self.fisher_id)
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
        self.exit_is_set[0] = True

    def trial_rod_cast(self):
        # function:
        # initial fishing window search
        # recording fishing window position
        # activation of accurate search in wincap

        if not self.search_object_with_click(self.fishing_window.get_object,
                                             self.fishing_window.get_object('fishing', False), 18, 4, 'fishing_window',
                                             True):
            return False
        self.pause_thread(0.1)
        if self.fishing_window.record_fishing_window():
            self.fishing()
        else:
            self.stop_fisher()

        # self.bar_limits()
        self.pause_thread(0.2)

        return True

    def actions_while_fishing(self):
        self.current_state[0] = 'fishing'
        # function:
        # fishing algorithm

        # searching for fishing window
        if not self.search_object_with_click(self.fishing_window.is_fishing_window,
                                             self.fishing_window.get_object('fishing', False), 12, 4):
            self.move_to_supplier()
            self.pause_thread(3)
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

        clock_time_without_bars = 0
        clock_is_checked = False
        threshold_time_without_any_bar = 2

        pump_skill_cast_time = 0
        reeling_skill_cast_time = 0
        pump_was_pressed = False
        reel_was_pressed = False
        pump_timer_was_set = False
        pumping_time = time.time()
        reeling_time = time.time()
        delta_pumping_skill = time.time()
        reel_count = 0
        reel_timer_was_set = False
        extra_attack_check = False
        # self.attack()
        # fishing main loop

        max_fishing_time = time.time()
        while self.fishing_window.is_fishing_window() and not self.exit_is_set[0]:
            if time.time() - max_fishing_time > 40:  # emergency antibug exit
                self.fishing()
            self.pause_thread(0.1)

            if self.is_day_time():
                temp = self.fishing_window.is_blue_bar()
            else:
                temp = self.fishing_window.is_red_bar() + self.fishing_window.is_red_bar()
            # if self.is_day_time():
            #     temp = self.fishing_window.get_object('blue_bar', True)
            # else:
            #     temp = self.fishing_window.get_object('blue_bar', True) + self.fishing_window.get_object('red_bar', True)

            # SMART loop breaker depending on conditions

            # if not self.ai_fishing_breaker(x_border, fishing_fight_time):
            #     self.fishing()
            #     self.pause_thread(0.7)
            #     return True

            if self.fishing_window.is_clock():

                if temp:
                    (x_temp, y_temp) = temp[-1]
                    # self.send_message(f'temp {temp[-1]}')
                    x_border = x_temp
                    clock_time_without_bars = time.time()
                else:

                    if time.time() - clock_time_without_bars > threshold_time_without_any_bar:
                        if time.time() - delta_pumping_skill >= self.pumping_skill_CD:
                            delta_pumping_skill = time.time()
                            self.pumping()

                # delta_pump_skill = time.time() - pump_skill_cast_time
                # if delta_pump_skill >= self.pumping_skill_CD:
                #     self.pumping()
                #     pump_skill_cast_time = time.time()

                if not coords_saved and x_border is not None:
                    pumping_time = time.time()
                    coords_saved = True
                    previous_position = x_border
                    # self.send_message('COORDS SAVED!!!!')
                # self.send_message(previous_position - x_border)
                if previous_position is not None and x_border is not None:
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

                    elif 4 <= x_border - previous_position < 15:
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

        if self.attempt_counter[0] == self.next_supplying_counter or self.supply_now[0]:
            print('supply now')
            self.supply_now[0] = False
            self.attack()
            self.trading()
        self.fihser_position_correction()

        return True

    def fihser_position_correction(self):
        t = 900
        if time.time() - self.position_correction_timer > t:
            self.attack()
            self.move_to_supplier()
            self.position_correction_timer = time.time()

    def search_object_with_click(self, search_object, click_coordinates, searching_time, time_between_actions, *args):
        counter = 0
        repeat_times = searching_time // time_between_actions
        temp_timer = time.time()

        while not search_object(*args):

            if time.time() - temp_timer > time_between_actions * counter:
                counter += 1
                self.click(click_coordinates)
                self.pause_thread(0.2)

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
            self.pause_thread(0.3)
        return False

    def smart_button_click(self):
        pass

    def bar_limits(self):
        [self.bar_limit_left, self.bar_limit_right] = self.fishing_window.wincap.bar_limits[self.fishing_window.hwnd]
        self.bar_limit_left -= 0.053
        self.bar_length = self.bar_limit_right - self.bar_limit_left

    def overweight_baits_soski_correction(self):
        self.send_message('overweight_baits_soski_correction')
        self.fishing_window.stop_accurate_search()
        self.pause_thread(1)
        self.baits_max = 1300
        self.soski_max = 5000
        self.soski_pet_max = 1000
        self.soski = 0
        self.baits = 0
        self.soski_pet = 0

        soski = self.recognize_number(self.fishing_window.get_object('soski'))
        time.sleep(5)
        baits = self.recognize_number(self.fishing_window.get_object('baits'))
        time.sleep(5)
        soski_pet = self.recognize_number(self.fishing_window.get_object('soski_pet'))

        self.pause_thread(1)
        if self.baits_max - baits > 0:
            required_dbaits = self.baits_max - baits
        else:
            required_dbaits = 0
        required_nbaits = 0
        if self.soski_max - soski > 0:
            required_soski = self.soski_max - soski
        else:
            required_soski = 0
        required_alacrity = 0
        if self.soski_pet_max - soski_pet > 0:
            required_soski_pet = self.soski_pet_max - soski_pet
        else:
            required_soski_pet = 0
        required_potion = 0

        if required_dbaits >= 1 or required_nbaits >= 1 or required_soski >= 1 or required_alacrity >= 1 or required_soski_pet >= 1 or required_potion >= 1:
            self.requested_items_to_supply.append(required_dbaits)  # dbaits
            self.requested_items_to_supply.append(required_nbaits)  # nbaits
            self.requested_items_to_supply.append(required_soski)  # soski

            self.requested_items_to_supply_d['dbaits'] = required_dbaits
            self.requested_items_to_supply_d['nbaits'] = required_nbaits
            self.requested_items_to_supply_d['soski'] = required_soski

            self.requested_items_to_supply_d['alacrity'] = required_alacrity
            self.requested_items_to_supply_d['soski_pet'] = required_soski_pet
            self.requested_items_to_supply_d['potion'] = required_potion
            # print('required_dbaits', required_dbaits)
            # print('required_nbaits', required_nbaits)
            # print('required_soski', required_soski)
            # print('required_alacrity', required_alacrity)
            # print('required_soski_pet', required_soski_pet)
            # print('required_potion', required_potion)
            self.fishers_requested_supps[0] = self.requested_items_to_supply_d
            self.fishers_request[0] = 'requests supplying'
            time.sleep(2)
            # print('++++++++++++++++FISHER IS requests supplying', self.fishing_service.fishers_request)
            # self.supply_request_proceed[0] = True
            # self.current_state[0] = 'busy'
            # self.trading_is_allowed[0] = True
        else:
            return False
        return True

    def allow_to_trade(self):
        self.trading_is_allowed[0] = True
        self.send_message('TRADING IS ALLOWED BOY BOY BOY')

    def process_supply_request(self):
        self.supply_request_proceed[0] = True
        self.send_message('SUPPLY REQUEST IS PROCEED BOY BOY BOY')

    def process_overweight_request(self):
        self.overweight_request_proceed[0] = True
        self.send_message('OVERWEIGHT REQUEST IS PROCEED BOY BOY BOY')

    def trading(self):
        self.send_message('--------------TRADING -----------------')
        self.current_state[0] = 'requests overweight check'

        while not self.overweight_request_proceed[0]:
            time.sleep(0.5)

        self.send_message('requests overweight check has been proceed')

        if not self.overweight_baits_soski_correction():
            self.send_message('overweight_baits_soski_correction FAILURE')
            return

        self.send_message('requests supplying')
        self.fishers_request[0] = 'requests supplying'
        # self.current_state[0] = 'requests supplying'

        while not self.supply_request_proceed[0]:
            time.sleep(0.5)

        self.send_message('request has been proceed')
        self.fishers_request[0] = ''

        self.current_state[0] = 'busy'
        self.send_message('waiting for trade permission')

        while not self.trading_is_allowed[0]:
            time.sleep(0.5)

        self.send_message('trading is allowed')
        self.move_to_supplier()

        self.pause_thread(1)

        # waiting_time2 = 15
        # temp_timer2 = time.time()
        # while time.time() - temp_timer2 < waiting_time2 and not self.fishing_window.is_exchange_menu():
        #     self.send_trade_to_supplier()
        #     self.pause_thread(6)

        if not self.search_object_with_click(self.fishing_window.is_exchange_menu,
                                             self.fishing_window.get_object('trade_supplier', False), 20, 4):
            self.fishing_window.start_accurate_search()
            self.pause_thread(1)
            return False

        self.send_message('exchange_menu found')
        self.pause_thread(16)
        tim = time.time()
        self.send_fish_to_supplier(self.fishing_window.is_exchange_menu())
        while time.time() - tim < 15:
            self.pause_thread(1)

        self.smart_press_button('ok', self.fishing_window.is_exchange_menu, searching_time=5)

        # if not self.search_object_without_click(self.fishing_window.is_exchange_menu, 120):
        #     self.fishing_window.start_accurate_search()
        #     self.pause_thread(1)
        #     return False

        # waiting_time = 15
        # temp = time.time()
        # while self.fishing_window.is_exchange_menu and time.time() - temp < waiting_time:
        #     time.sleep(0.5)

        answer = self.hold_the_object_in_vision(self.fishing_window.is_exchange_menu, 120)

        if answer:
            self.press_button('cancel')

        self.supplying_request[0] = False
        self.supply_request_proceed[0] = False
        self.trading_is_allowed[0] = False
        self.overweight_request_proceed[0] = False
        # self.requested_items_to_supply.pop()
        # self.requested_items_to_supply.pop()
        # self.requested_items_to_supply.pop()

        self.requested_items_to_supply_d['dbaits'] = 0
        self.requested_items_to_supply_d['nbaits'] = 0
        self.requested_items_to_supply_d['soski'] = 0
        self.requested_items_to_supply_d['alacrity'] = 0
        self.requested_items_to_supply_d['soski_pet'] = 0
        self.requested_items_to_supply_d['potion'] = 0
        self.fishers_requested_supps[0] = {}

        self.next_supplying_counter = self.attempt_counter[0] + self.send_counter
        self.send_message(f'NEXT SUPPLYING ATTEMPT {self.next_supplying_counter}')

        # self.send_counter += 3

        self.fishing_window.start_accurate_search()

        self.pause_thread(1)
        self.current_state[0] = 'fishing'

    def send_fish_to_supplier(self, exchange_menu_pos):
        self.send_message('send_fish_to_supplier')
        list_pos = []
        for x in self.fishing_window.catched_fish_database:
            catched_fish_pos_list = self.fishing_window.find(x[0])
            # print('catched_fish_pos_list', catched_fish_pos_list)
            if catched_fish_pos_list:
                # y1point = self.fishing_window.is_exchange_menu
                for catched_fish_pos in catched_fish_pos_list:
                    (x_temp, y_temp) = catched_fish_pos
                    if not list_pos:
                        list_pos.append(catched_fish_pos)
                        continue
                    else:
                        apnd = True
                        for elem in list_pos:
                            (elem_x, elem_y) = elem
                            if abs(x_temp - elem_x) < 10 and abs(y_temp - elem_y) < 10:
                                apnd = False
                                break
                        if apnd:
                            list_pos.append(catched_fish_pos)
        if not list_pos:
            return
        # self.send_message(f'original {list_pos}')
        decorated = [(tup[1], tup) for tup in list_pos]
        decorated.sort(reverse=True)
        sorted = [tup for second, tup in decorated]
        # self.send_message(f'sorted y {sorted}')
        (temp_x_0, temp_y_0) = sorted[0]
        for i in range(len(sorted)):
            (x, y) = sorted[i]
            # print('temp_y_0', temp_y_0)
            if abs(y - temp_y_0) < 10 and y != temp_y_0:
                print('abs(y - temp_y_0)', abs(y - temp_y_0))
                sorted[i] = (x, temp_y_0)
            else:
                temp_y_0 = y

        # self.send_message(f'sorted y cleaned {sorted}')
        decorated = [(tup[1], tup) for tup in sorted]
        decorated.sort(reverse=True)
        sorted2 = [tup for second, tup in decorated]
        # self.send_message(f'sorted x {sorted2}')
        # decorated = [(tup[1], tup) for tup in sorted1]
        # decorated.sort(reverse=True)
        # sorted2 = [tup for second, tup in decorated]
        # self.send_message(f'sorted {sorted2}')

        for elem in sorted2:
            # print('elem', elem)
            self.drag_and_drop_fish([elem], exchange_menu_pos)

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
                        [self.fishing_window.get_object('attack', False), True, 'LEFT', False, False, False],
                        self.fishing_window)
        self.pause_thread(0.1)
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
                        [self.fishing_window.get_object('fishing', False), True, 'LEFT', False, False, False],
                        self.fishing_window)

    def pumping(self):
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('pumping', False), True, 'LEFT', False, False, False],
                        self.fishing_window)
        # self.q.new_task('mouse', [[(100, 100)], True, 'LEFT', False, False, False], self.fishing_window)

    def reeling(self):
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('reeling', False), True, 'LEFT', False, False, False],
                        self.fishing_window)

    def rebuff(self, search=False):
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('buff', search), True, 'LEFT', False, False, False],
                        self.fishing_window)
        self.buff_time = time.time()
        self.pause_thread(1.5)

    def drag_and_drop_fish(self, pos_fish, pos_trade_window):
        # print('pos1', pos_fish)

        [(target_pos_x, target_pos_y)] = pos_trade_window
        target_pos = [(target_pos_x, target_pos_y - 220)]
        # print('pos2', target_pos)
        self.q.new_task('mouse',
                        [pos_fish, target_pos, 'LEFT', False, 'drag_and_drop_alt', False],
                        self.fishing_window)
        self.pause_thread(.5)

    def switch_soski(self, search=False):
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('soski', search), False, 'RIGHT', False, False, False],
                        self.fishing_window)

    def choose_night_bait(self, search=False):
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('luminous', search)[1], False, 'RIGHT', False, False, False],
                        self.fishing_window)
        self.current_baits = 'n_baits'
        self.pause_thread(0.7)

    def choose_day_bait(self, search=False):
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('colored', search)[0], False, 'RIGHT', False, False, False],
                        self.fishing_window)
        self.current_baits = 'd_baits'
        self.pause_thread(0.7)

    def equipment_bag(self):
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('equipment_bag', False), False, 'RIGHT', False, False, False],
                        self.fishing_window)

    def record_game_time(self):
        self.send_message('record_game_time')
        return True

    def update_current_attempt(self):
        self.attempt_counter[0] += 1
        self.send_message(f'Attempt # {self.attempt_counter[0]}')

    def send_mail(self):
        pass

    def receive_mail(self):
        pass

    def send_trade(self):
        pass

    def activate_soski(self):
        soski = self.fishing_window.get_object('soski')
        if soski:
            self.send_message('soski activated')
            self.q.new_task('mouse', [soski, False, 'RIGHT', False, False, False], self.fishing_window)
            self.pause_thread(0.5)

    def activate_soski_pet(self):
        soski_pet = self.fishing_window.get_object('soski_pet')
        if soski_pet:
            self.send_message('soski_pet activated')
            self.q.new_task('mouse', [soski_pet, False, 'RIGHT', False, False, False], self.fishing_window)
            self.pause_thread(0.5)

    # def wait_for_trade(self):
    #     pass

    def change_bait(self):
        pass

    def map(self, search=False):
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('map_button', search), False, 'RIGHT', False, False, False],
                        self.fishing_window)

    def is_day_time(self):
        # if self.game_time is not None:
        return True

    def if_rebuff_time(self):
        if time.time() - self.buff_hawkeye_timer > self.buff_hawkeye_rebufftime:
            self.attack()
            self.rebuff_hawkeye()
        if time.time() - self.fishing_potion_timer > self.fishing_potion_rebufftime:
            self.rebuff_fishing_potion()
        if time.time() - self.alacrity_potion_timer > self.alacrity_potion_rebufftime:
            self.rebuff_warlock_wex()
        pass

    def rebuff_hawkeye(self):

        self.buff_hawkeye_timer = time.time()
        temp = self.fishing_window.is_hawk_buff()
        if temp:
            self.send_message('rebuff hawkeye')
            self.reeling_skill_CD = 1.9
            self.pumping_skill_CD = 1.9
            self.q.new_task('mouse', [temp, False, 'LEFT', False, False, False], self.fishing_window)
            self.pause_thread(2.5)
        else:
            self.buff_hawkeye_rebufftime = 10000000

    def rebuff_warlock_wex(self):
        self.send_message('rebuff warclock wex alacrity')
        self.alacrity_potion_timer = time.time()
        alacrity_dex_warlock = self.fishing_window.get_object('alacrity_dex_warlock')
        if alacrity_dex_warlock:
            self.q.new_task('mouse', [alacrity_dex_warlock, False, 'LEFT', False, False, False], self.fishing_window)
            self.pause_thread(6)

    def rebuff_fishing_potion(self):
        self.send_message('rebuff fishing potion')
        self.fishing_potion_timer = time.time()
        if self.fisher_id == 0:
            return
        fishing_potion_white = self.fishing_window.get_object('fishing_potion_white')
        if fishing_potion_white:
            self.q.new_task('mouse',
                            [fishing_potion_white, False, 'LEFT', False, False, False],
                            self.fishing_window)
            self.pause_thread(0.4)

    def move_to_supplier(self, search=False):
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('move_to_supplier', search), False, 'LEFT', False, False,
                         False],
                        self.fishing_window)
        self.pause_thread(2)

    def camera_top_zoom_in(self):
        window_center_pos = self.fishing_window.window_center_pos()
        [(x, y)] = window_center_pos

        self.q.new_task('mouse',
                        [[(x, y)], [(x, y + 100)], 'AutoHotPy', False, False, False],
                        self.fishing_window)
        # self.q.turn(x, y)
        self.pause_thread(1 + self.number_of_fishers * 7 - self.fisher_id * 7)

    def register_nickname(self):
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('move_to_supplier'), False, 'LEFT', False, False, 'Alt+T'],
                        self.fishing_window)
        self.pause_thread(1)
        self_nickname = self.fishing_window.get_self_nickname()
        if self_nickname:
            self.nickname[0] = self_nickname
            self.send_message(f'my name is !!!!!!!!!!!!! {self_nickname}')
        else:
            self.send_message('Error registering nickname')
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('move_to_supplier'), False, 'LEFT', False, False, 'Alt+N'],

                        self.fishing_window)

    def hide_mouse(self):
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('a_sign'), False, 'LEFT', 'no click', False, False],
                        self.fishing_window)
        self.pause_thread(0.5)

    def activate_window(self):
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('a_sign', search=True), False, 'LEFT', False, False, False],
                        self.fishing_window)
        self.pause_thread(0.5)
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('a_sign'), False, 'LEFT', False, False, False],
                        self.fishing_window)
        self.pause_thread(0.7)

    def init_setup(self):
        self.send_message('initializing setup...')
        self.activate_window()
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('a_sign'), False, 'LEFT', False, False, 'Alt+L'],
                        self.fishing_window)
        self.pause_thread(1.5)
        self.hide_mouse()
        if not self.fishing_window.init_search():
            self.stop_fisher()
            return False
        self.pause_thread(1.5)
        self.q.new_task('mouse',
                        [self.fishing_window.get_object('a_sign'), False, 'LEFT', False, False, 'Alt+1'],
                        self.fishing_window)
        self.pause_thread(0.5)

        # self.register_nickname()
        self.camera_top_zoom_in()

        fishing_potion_white = self.fishing_window.get_object('fishing_potion_white', search=True)
        if fishing_potion_white:
            self.fishing_potion_timer = 0
        else:
            # self.send_message('NO fishing_potion_white')
            self.fishing_potion_rebufftime = time.time() + 999999

        soski = self.fishing_window.get_object('soski', search=True)
        if soski:
            pass
            # self.send_message('soski recorded')
        else:
            self.send_message('Error soski search')

        soski_pet = self.fishing_window.get_object('soski_pet', search=True)
        if soski_pet:
            pass
            # self.send_message('soski_pet recorded')
        else:
            self.send_message('Error soski_pet search')

        baits = self.fishing_window.get_object('baits', search=True)
        if baits:
            pass
            # self.send_message('baits recorded')
        else:
            self.send_message('Error baits search')

        status_bar = self.fishing_window.get_object('status_bar', search=True)
        if status_bar:
            # self.send_message('status_bar')
            self.q.new_task('mouse', [self.fishing_window.get_object('move_to_supplier'), False, 'LEFT', False, False,
                                      'Alt+Shift+s'], self.fishing_window)
            self.pause_thread(0.5)

        radar = self.fishing_window.get_object('mini_map', search=True)
        if radar:
            # self.send_message('radar')
            self.q.new_task('mouse', [self.fishing_window.get_object('move_to_supplier'), False, 'LEFT', False, False,
                                      'Alt+Shift+r'], self.fishing_window)
            self.pause_thread(0.5)

        alacrity_dex_warlock = self.fishing_window.get_object('alacrity_dex_warlock', search=True)
        if alacrity_dex_warlock:
            # self.send_message('alacrity_dex_warlock')
            self.alacrity_potion_timer = 0
        else:
            self.alacrity_potion_timer = time.time() + 999999

        hawk_buff = self.fishing_window.is_hawk_buff()
        if hawk_buff:
            self.buff_hawkeye_timer = 0
        else:
            # self.send_message('NO hawk_buff')
            self.buff_hawkeye_rebufftime = time.time() + 999999

        self.pause_thread(0.5)

    def supply_now_function(self):
        self.supply_now[0] = True

    def init_buff(self):
        pass

    def recognize_number(self, coordinates):
        self.q.new_task('mouse',
                        [coordinates, False, 'LEFT', 'no click', False, False], self.fishing_window, priority='High')
        time.sleep(1.5)
        recognition_time = 6
        timer = time.time()
        while time.time() - timer < recognition_time:
            result = self.fishing_window.recognize_number(coordinates)
            if result is not None:
                print(result)
                return result
            self.pause_thread(2)
        return 0
