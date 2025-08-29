from otree.api import *
import random

doc = """
IOS11 <br/>
Baader, M., Starmer, C., Tufano, F. et al. Introducing IOS11 as an extended interactive version of the 
‘Inclusion of Other in the Self’ scale to estimate relationship closeness. 
Sci Rep 14, 8901 (2024). https://doi.org/10.1038/s41598-024-58042-6
"""


class C(BaseConstants):
    NAME_IN_URL = 'whios'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        if "groups" not in self.session.vars:
            self.group_randomly()
            self.session.vars["groups"] = self.get_group_matrix()
        self.set_group_matrix(self.session.vars["groups"])


def creating_session(subsession: Subsession):
    subsession.creating_session()

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    ios_value = models.IntegerField()


# PAGES
class IOSPage(Page):
    form_model = 'player'
    form_fields = ['ios_value']

    @staticmethod
    def vars_for_template(player: Player):
        return dict()

    @staticmethod
    def js_vars(player: Player):
        return dict(
            fill_auto=player.session.config.get("fill_auto", False),
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.participant._is_bot = True
            player.ios_value = random.randint(1, 11)


page_sequence = [IOSPage]
