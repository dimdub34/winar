from otree.api import *
import random
from settings import LANGUAGE_CODE

doc = """
IOS11 <br/>
Baader, M., Starmer, C., Tufano, F. et al. Introducing IOS11 as an extended interactive version of the 
‘Inclusion of Other in the Self’ scale to estimate relationship closeness. 
Sci Rep 14, 8901 (2024). https://doi.org/10.1038/s41598-024-58042-6
"""

language = {"en": False, "fr": False}
language[LANGUAGE_CODE] = True
_ = lambda s: s[LANGUAGE_CODE]


class C(BaseConstants):
    NAME_IN_URL = 'whios'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    if "groups" not in subsession.session.vars:
        subsession.group_randomly()
        subsession.session.vars["groups"] = subsession.get_group_matrix()
    subsession.set_group_matrix(subsession.session.vars["groups"])


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    ios_value = models.IntegerField(min=1, max=11)


# PAGES
class IOSPage(Page):
    form_model = 'player'
    form_fields = ['ios_value']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            **language
        )

    @staticmethod
    def js_vars(player: Player):
        return dict(
            fill_auto=player.session.config.get("fill_auto", False),
            **language
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.participant._is_bot = True
            player.ios_value = random.randint(1, 11)


page_sequence = [IOSPage]
