from . import *


class PlayerBot(Bot):
    def play_round(self):
        yield Submission(IOSPage, timeout_happened=True)
