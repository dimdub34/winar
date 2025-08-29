from . import *


class PlayerBot(Bot):
    def play_round(self):
        yield Submission(BeforeFinal, check_html=False)
        yield Submission(Final, timeout_happened=True, check_html=False)
        yield Submission(FinalAfterComments, check_html=False)
