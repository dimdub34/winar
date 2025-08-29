from . import *


class PlayerBot(Bot):
    def play_round(self):
        yield Submission(Questionnaire1, timeout_happened=True)
        yield Submission(Questionnaire2, timeout_happened=True)
        yield Submission(Demog, timeout_happened=True)
