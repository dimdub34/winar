from otree.api import *
from whistleblowing_commons.config import Config

doc = """
Welcome App
"""

class C(BaseConstants):
    NAME_IN_URL = 'whwel'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    country = models.StringField()
    
    def creating_session(self):
        self.country = self.session.config["country"]
        self.group_randomly()
        self.session.vars["groups"] = self.get_group_matrix()


def creating_session(subsession: Subsession):
    subsession.creating_session()

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# =======================================================================================================================
#
# PAGES
#
# =======================================================================================================================
class MyPage(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(**Config.get_parameters())

    @staticmethod
    def js_vars(player: Player):
        return dict(
            fill_auto=player.session.config.get("fill_auto", False),
            **Config.get_parameters()
        )


class Welcome(MyPage):
    pass


class Presentation(MyPage):
    pass


class Part1(MyPage):
    pass


page_sequence = [Welcome, Presentation, Part1]
