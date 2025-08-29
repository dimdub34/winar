from otree.models import Participant

from . import *


class PlayerBot(Bot):
    def play_round(self):
        yield Welcome
        yield Presentation
        yield Part1
