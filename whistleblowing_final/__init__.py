from otree.api import *
from pathlib import Path
from whistleblowing_commons.config import Config
from whistleblowing_commons.functions import clean_number

doc = """
Final
"""

app_name = Path(__file__).parent.name


class C(BaseConstants):
    NAME_IN_URL = "whfin"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


def vars_for_admin_report(subsession: Subsession):
    players_infos = list()
    for p in subsession.get_players():
        players_infos.append(
            dict(
                code=p.participant.code,
                label=p.participant.label,
                effort_payoff=p.effort_payoff,
                game_payoff=p.game_payoff,
                payoff_ecu=p.payoff_ecu,
                payoff=p.payoff

            )
        )
    return dict(players_infos=players_infos)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    effort_payoff = models.FloatField(initial=0)
    game_payoff = models.FloatField(initial=0)
    payoff_ecu = models.FloatField(initial=0)
    comments = models.LongStringField(
        blank=True,
        label="You can write comments about the experiment in the area below. Then, click on Save.")

    def compute_payoffs(self):
        self.effort_payoff = self.participant.vars["whistleblowing_effort"]["payoff_ecu"]
        self.game_payoff = self.participant.vars["whistleblowing_game"]["payoff_ecu"]
        self.payoff_ecu = Config.ENDOWMENT + self.effort_payoff + self.game_payoff
        self.payoff = self.payoff_ecu * self.session.config["real_world_currency_per_point"]
        self.participant.payoff = self.payoff

    def get_txt_final(self):
        txt_final = (
            f"Your final payoff for this experiment is equal to {clean_number(Config.ENDOWMENT)} + "
            f"{clean_number(self.effort_payoff)} "
            f"{'+' if self.game_payoff >= 0 else ''} {clean_number(self.game_payoff)} = "
            f"{clean_number(self.payoff_ecu)} ECU, which corresponds to {self.payoff}."
        )
        self.participant.vars["whistleblowing_final"] = dict(
            txt_final=txt_final,
            payoff_ecu=self.payoff_ecu,
            payoff=self.payoff,
        )
        return txt_final


# ======================================================================================================================
#
# --PAGES --
#
# ======================================================================================================================
class MyPage(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict()


class BeforeFinal(MyPage):
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.compute_payoffs()


class Final(MyPage):
    form_model = "player"
    form_fields = ["comments"]

    @staticmethod
    def vars_for_template(player: Player):
        existing = MyPage.vars_for_template(player)
        existing["txt_final"] = player.get_txt_final()
        return existing

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.comments = "Automatic message"


class FinalAfterComments(MyPage):
    @staticmethod
    def vars_for_template(player: Player):
        existing = MyPage.vars_for_template(player)
        existing["txt_final"] = player.get_txt_final()
        return existing


page_sequence = [BeforeFinal, Final, FinalAfterComments]
