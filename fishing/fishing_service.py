from fishing.fisher import Fisher
from fishing.fishing_window import FishingWindow


class FishingService:

    @staticmethod
    def startFishing():
        fishing_window1 = FishingWindow(0, 0, 500, 500)
        fishing_window2 = FishingWindow(600, 600, 900, 900)
        fisher1 = Fisher(fishing_window1, 1)
        fisher2 = Fisher(fishing_window2, 2)
        fisher1.start()
        fisher2.start()
