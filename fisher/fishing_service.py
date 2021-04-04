from fisher.fisher import Fisher
from fisher.fishing_window import FishingWindow


class FishingService:
    def __init__(self, number_of_fishers):
        if number_of_fishers < 1 or number_of_fishers > 2:
            #warning
            del self

        #
        for i in range(number_of_fishers):
            self.fishing_window.append(FishingWindow(500*i, 0, 500, 500))

        for i in range(number_of_fishers):
            self.fishers.append(Fisher(self.fishing_window[i], number_of_fishers))


    @staticmethod
    def startFishing():
    
        for fisher in fishers:
            fisher.start()

    fishers = []
    fishing_window = []
