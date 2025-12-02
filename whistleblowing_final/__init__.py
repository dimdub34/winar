from pathlib import Path

from otree.api import *

from whistleblowing_commons.config import Config, language, _

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
                grids=p.participant.vars.get("whistleblowing_counting", {}).get("payoff_ecu", 0),
                maths=p.participant.vars.get("whistleblowing_maths", {}).get("payoff_ecu", 0),
                sliders=p.participant.vars.get("whistleblowing_sliders", {}).get("payoff_ecu", 0),
                effort_payoff=p.participant.vars.get("whistleblowing_effort", {}).get("payoff_ecu", 0),
                game_payoff=p.game_payoff,
                endowment=Config.ENDOWMENT,
                payoff_ecu=p.payoff_ecu,
                payoff=p.participant.payoff,
                payoff_with_fee=p.participant.payoff_plus_participation_fee()
            )
        )
    return dict(players_infos=players_infos)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    effort_payoff = models.FloatField(initial=0)
    game_payoff = models.FloatField(initial=0)
    payoff_ecu = models.FloatField(initial=0)

    def compute_payoffs(self):
        self.effort_payoff = self.participant.vars["whistleblowing_effort"]["payoff_ecu"]
        self.game_payoff = self.participant.vars["whistleblowing_game"]["payoff_ecu"]
        self.payoff_ecu = Config.ENDOWMENT + self.effort_payoff + self.game_payoff
        self.payoff = self.payoff_ecu * self.session.config["real_world_currency_per_point"]
        self.participant.payoff = self.payoff

        txt_final = _(dict(
            en=f"Your final payoff for this experiment is equal to {Config.ENDOWMENT} (endowment) + "
               f"{self.effort_payoff} (part 1) "
               f"{'+' if self.game_payoff >= 0 else ''} {self.game_payoff} (part 2) = "
               f"{self.payoff_ecu} ECU, which corresponds to {self.payoff}. "
               f"With the show-up fee, your total payoff is {self.participant.payoff_plus_participation_fee()}.",
            fr=f"Votre gain pour cette expérience est égal à {Config.ENDOWMENT} (dotation) + "
               f"{self.effort_payoff} (partie 1) "
               f"{'+' if self.game_payoff >= 0 else ''} {self.game_payoff} (partie 2) = "
               f"{self.payoff_ecu} ECU, soit {self.payoff}. Avec le forfait de participation, votre gain total est de "
               f"{self.participant.payoff_plus_participation_fee()}.",
        ))
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
        return dict(**language)


class BeforeFinal(MyPage):
    template_name = "global/EmptyPage.html"

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.compute_payoffs()


class Final(MyPage):
    pass


page_sequence = [BeforeFinal, Final]
