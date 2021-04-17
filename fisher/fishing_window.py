from system.screen_analyzer import ScreenAnalyzer
from system.l2window import L2window


class FishingWindow(L2window):
    def __init__(self, x_left_top, y_left_top, width, height):
        self.send_message(f'TEST FishingWindow(L2window) calling')
        self.left_top_x = x_left_top
        self.left_top_y = y_left_top
        self.width = width
        self.height = height

    @classmethod
    def send_message(cls, message):
        print(message)

    # pos_variables
    vision_fishing_pos = 0
    vision_pumping_pos = 0
    vision_reeling_pos = 0
    vision_blue_bar_pos = 0
    vision_clock_pos = 0
    vision_fishing_window_pos = 0
    vision_red_bar_pos = 0
    vision_cdbuff_pos = 0
    vision_bait_pos = 0
    vision_colored_pos = 0
    vision_luminous_pos = 0
    vision_soski_pos = 0
    vision_soski_activated_pos = 0
    vision_map_button_pos = 0
    vision_sun_pos = 0
    vision_moon_pos = 0
    vision_disconnect_EN_pos = 0
    vision_menu_pos = 0
    vision_equipment_bag_pos = 0
    vision_weight_icon_pos = 0
    vision_login_pos = 0
    vision_mailbox_pos = 0
    vision_sendmail_button_pos = 0
    vision_send_button_pos = 0
    vision_confirm_button_pos = 0
    vision_claim_items_button_pos = 0

    vision_catcheditem_pos = [0] * 4
