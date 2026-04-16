from otree.api import *

doc = """
Welcome App
"""

class C(BaseConstants):
    NAME_IN_URL = 'whwel'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1

    ENDOWMENT = 75


class Subsession(BaseSubsession):
    country = models.StringField()


def creating_session(subsession: Subsession):
    subsession.country = subsession.session.config["country"]
    subsession.group_randomly()
    subsession.session.vars["groups"] = subsession.get_group_matrix()


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
    pass

    @staticmethod
    def js_vars(player: Player):
        return dict(
            fill_auto=player.session.config.get("fill_auto", False),
        )


class Welcome(MyPage):
    pass


class Presentation(MyPage):
    pass


class Part1(MyPage):
    pass


page_sequence = [Welcome, Presentation, Part1]
