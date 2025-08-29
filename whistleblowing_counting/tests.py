from . import *


class PlayerBot(Bot):
    def play_round(self):
        yield Instructions
        yield Submission(CountingTask, timeout_happened=True, check_html=False)
        yield Submission(CountingEstimation, timeout_happened=True)
