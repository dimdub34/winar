from otree.api import *
from enum import Enum
import random
from settings import LANGUAGE_CODE
from pathlib import Path
from whistleblowing_commons.config import Config, language, _
from whistleblowing_commons.functions import seconds_to_minutes

doc = """
Maths effort task
"""

app_name = Path(__file__).parent.name


class C(BaseConstants):
    NAME_IN_URL = 'whmaths'
    PLAYERS_PER_GROUP = Config.PLAYERS_PER_GROUP
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    treatment = models.StringField()

    def compute_payoffs(self):
        if self.treatment == Config.INDIVIDUAL:
            for p in self.get_players():
                p.payoff_ecu = p.maths_performance * Config.PIECE_RATE
                p.set_txt_final()
        else:
            for g in self.get_groups():
                g.maths_performance_group = max(p.maths_performance for p in g.get_players())
                for p in g.get_players():
                    p.payoff_ecu = g.maths_performance_group * Config.PIECE_RATE
                    p.set_txt_final()

    def creating_session(self):
        self.treatment = self.session.config['treatment']
        if "groups" not in self.session.vars:
            self.group_randomly()
            self.session.vars["groups"] = self.get_group_matrix()
        self.set_group_matrix(self.session.vars["groups"])

        # creation of operations
        for group in self.get_groups():
            operations = list()
            for i in range(Config.NUM_OPERATIONS):
                numbers = [random.randint(10, 99) for _ in range(Config.OPERATION_SIZE)]
                operations.append(dict(numbers=numbers, total=sum(numbers), number=i + 1))
            self.session.vars[f"operations_g_{group.id_in_subsession}"] = operations


def creating_session(subsession: Subsession):
    subsession.creating_session()


class Group(BaseGroup):
    maths_performance_group = models.IntegerField()


class Player(BasePlayer):
    maths_performance = models.IntegerField()
    maths_estimation = models.IntegerField(label=_(dict(en="Your guess:", fr="Votre estimation :")), min=0, max=100)
    payoff_ecu = models.FloatField()

    def set_txt_final(self):
        pluriel = lambda x: "s" if x > 1 else ""
        txt_final = _(dict(
            en=f"You resolved {self.maths_performance} operation{pluriel(self.maths_performance)}.",
            fr=f"Vous avez résolu {self.maths_performance} opération{pluriel(self.maths_performance)}."
        ))
        txt_final += " "

        if self.subsession.treatment == Config.INDIVIDUAL:
            txt_final += _(dict(en=f"Your payoff_ecu is therefore equal to "
                                   f"{self.maths_performance} x {Config.PIECE_RATE} = {self.payoff_ecu} ECU.",
                                fr=f"Votre gain est donc égal à "
                                   f"{self.maths_performance} x {Config.PIECE_RATE} = {self.payoff_ecu} ECU."
                                ))

        else:  # COOPERATION
            txt_final += _(dict(
                en=f"The best scorer in your group resolved {self.group.maths_performance_group} "
                   f"operation{pluriel(self.group.maths_performance_group)}. The payoff of each member of your "
                   f"group is therefore equal to {self.group.maths_performance_group} x "
                   f"{Config.PIECE_RATE} = {self.payoff_ecu} ECU.",
                fr=f"Le membre de votre groupe avec le meilleur score a résolu {self.group.maths_performance_group} "
                   f"opération{pluriel(self.group.maths_performance_group)}. Le gain de chaque membre de votre groupe "
                   f"est donc égal à "
                   f"{self.group.maths_performance_group} x {Config.PIECE_RATE} = {self.payoff_ecu} ECU."
            ))

        self.participant.vars[app_name] = dict(
            txt_final=txt_final,
            payoff_ecu=self.payoff_ecu,
            payoff=self.payoff_ecu * self.session.config["real_world_currency_per_point"]

        )


# ======================================================================================================================
#
# -- PAGES --
#
# ======================================================================================================================

class MyPage(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            instructions_template_path="whistleblowing_maths/InstructionsTemplate.html",
            instructions_template_title=_(dict(en="Task 2 - Instructions", fr="Tâche 2 - Instructions")),
            effort_duration=seconds_to_minutes(Config.EFFORT_DURATION),
            **language,
            **Config.get_parameters()
        )

    @staticmethod
    def js_vars(player: Player):
        return dict(
            fill_auto=player.session.config.get("fill_auto", False),
            **language,
            **Config.get_parameters()
        )


class Instructions(MyPage):
    template_name = "global/Instructions.html"


class InstructionsWaitForAll(WaitPage):
    wait_for_all_groups = True
    template_name = "global/InstructionsWaitPage.html"

    @staticmethod
    def vars_for_template(player):
        return MyPage.vars_for_template(player)


class MathsTask(MyPage):
    form_model = "player"
    form_fields = ["maths_performance"]
    timeout_seconds = Config.EFFORT_DURATION
    timer_text = _(dict(en="Remaining time:", fr="Temps restant :"))

    @staticmethod
    def vars_for_template(player: Player):
        existing = MyPage.vars_for_template(player)
        existing.update(
            dict(
                time=seconds_to_minutes(Config.EFFORT_DURATION),
                operations=player.session.vars[f"operations_g_{player.group.id_in_subsession}"],
            )
        )
        return existing

    @staticmethod
    def js_vars(player: Player):
        existing = MyPage.js_vars(player)
        existing["operations"] = player.session.vars[f"operations_g_{player.group.id_in_subsession}"]
        return existing

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened and player.session.config.get("test", False):
            player.participant._is_bot = True
            player.maths_performance = random.randint(0, 100)


class MathsEstimation(MyPage):
    form_model = "player"
    form_fields = ["maths_estimation"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.participant._is_bot = True
            player.maths_estimation = random.randint(0, 100)


class MathsWaitForAll(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        subsession.compute_payoffs()


page_sequence = [
    Instructions, InstructionsWaitForAll,
    MathsTask, MathsEstimation, MathsWaitForAll,
]
