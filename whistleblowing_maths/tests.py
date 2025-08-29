from . import *


class PlayerBot(Bot):
    def play_round(self):
        yield Instructions
        yield Submission(MathsTask, timeout_happened=True, check_html=False)
        yield Submission(MathsEstimation, timeout_happened=True)
