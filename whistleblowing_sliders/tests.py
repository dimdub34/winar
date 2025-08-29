from . import *


class PlayerBot(Bot):
    def play_round(self):
        yield Instructions
        yield Submission(SlidersTask, timeout_happened=True, check_html=False)
        yield Submission(SlidersEstimation, timeout_happened=True)
