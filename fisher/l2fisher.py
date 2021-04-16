import threading


class Fisher(threading.Thread):
    def __init__(self, fishing_window, fisher_number):
        self.send_message(f'TEST fisher {fisher_number} calling')
        threading.Thread.__init__(self)
        self.fishing_window = fishing_window
        self.fisher_number = fisher_number

    @classmethod
    def send_message(cls, message):
        print(message)

    def start(self):
        self.send_message(f'TEST fisher {self.fisher_number} is fishing')

    def stop(self):
        self.send_message(f'TEST fisher {self.fisher_number} has finished fishing')

    def get_status(self):
        pass

    def pumping(self):
        pass

    def reeling(self):
        pass

    def turn_on_soski(self):
        pass

    def choose_nigtly_bait(self):
        pass

    def choose_daily_bait(self):
        pass

    def send_mail(self):
        pass

    def receive_mail(self):
        pass

    def change_bait(self):
        pass

    fishing_window = None
    fisher_number = None
