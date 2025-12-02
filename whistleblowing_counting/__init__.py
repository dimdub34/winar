from otree.api import *
from enum import Enum
import random
from settings import LANGUAGE_CODE
from pathlib import Path
from whistleblowing_commons.config import Config, language, _
from whistleblowing_commons.functions import seconds_to_minutes

doc = """
Counting effort task
"""

app_name = Path(__file__).parent.name


class C(BaseConstants):
    NAME_IN_URL = 'whcount'
    PLAYERS_PER_GROUP = Config.PLAYERS_PER_GROUP
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    treatment = models.StringField()

    def creating_session(self):
        self.treatment = self.session.config['treatment']
        if "groups" not in self.session.vars:
            self.group_randomly()
            self.session.vars["groups"] = self.get_group_matrix()
        self.set_group_matrix(self.session.vars["groups"])

        # creation of grids
        for group in self.get_groups():
            grids = list()
            for i in range(Config.NUM_GRIDS):
                g = dict(grid=[], total=0)
                for row in range(Config.GRID_SIZE[0]):
                    g["grid"].append([random.randint(0, 1) for _ in range(Config.GRID_SIZE[1])])
                    g["total"] += sum(g["grid"][-1])
                    g["number"] = i + 1
                grids.append(g)
            self.session.vars[f"grids_g_{group.id_in_subsession}"] = grids

    def compute_payoffs(self):
        if self.treatment == Config.INDIVIDUAL:
            for p in self.get_players():
                p.payoff_ecu = p.counting_performance * Config.PIECE_RATE
                p.set_txt_final()
        else:
            for g in self.get_groups():
                g.counting_performance_group = max([p.counting_performance for p in g.get_players()])
                for p in g.get_players():
                    p.payoff_ecu = g.counting_performance_group * Config.PIECE_RATE
                    p.set_txt_final()


def creating_session(subsession: Subsession):
    subsession.creating_session()


class Group(BaseGroup):
    counting_performance_group = models.IntegerField()


class Player(BasePlayer):
    counting_performance = models.IntegerField()
    counting_estimation = models.IntegerField(label=_(dict(en="Your guess:", fr="Votre estimation :")), min=0, max=100)
    payoff_ecu = models.FloatField()

    def set_txt_final(self):
        pluriel = lambda x: "s" if x > 1 else ""
        txt_final = _(dict(
            en=f"You found the right number of 1's in {self.counting_performance} grid{pluriel(self.counting_performance)}.",
            fr=f"Vous avez trouvé le bon nombre de 1 dans {self.counting_performance} grille{pluriel(self.counting_performance)}.",
        ))

        txt_final += "<br>"

        if self.subsession.treatment == Config.INDIVIDUAL:
            txt_final += _(dict(
                en=f"Your payoff is therefore equal to "
                   f"{self.counting_performance} x {Config.PIECE_RATE} = {self.payoff_ecu} ECU.",
                fr=f"Votre gain est donc égal à "
                   f"{self.counting_performance} x {Config.PIECE_RATE} = {self.payoff_ecu} ECU."
            ))

        else:  # ccoperation
            txt_final += _(dict(
                en=f"The best scorer in your group found the right number of 1's in "
                   f"{self.group.counting_performance_group} grid{pluriel(self.group.counting_performance_group)}. "
                   f"The payoff of each member of your "
                   f"group is therefore equal to {self.group.counting_performance_group} x "
                   f"{Config.PIECE_RATE} = {self.payoff_ecu} ECU.",
                fr=f"Le membre de votre groupe avec le meilleur score a trouvé le bon nombre de 1 dans "
                   f"{self.group.counting_performance_group} grille{pluriel(self.group.counting_performance_group)}. "
                   f"Le gain de chaque membre de votre groupe est donc égal à "
                   f"{self.group.counting_performance_group} x "
                   f"{Config.PIECE_RATE} = {self.payoff_ecu} ECU."
            ))
        self.participant.vars[app_name] = dict(
            txt_final=txt_final,
            payoff_ecu=self.payoff_ecu,
            payoff=self.payoff_ecu * self.session.config["real_world_currency_per_point"]
        )
        # print(self.participant.vars[app_name])


# ======================================================================================================================
#
# -- PAGES --
#
# ======================================================================================================================

class MyPage(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            instructions_template_path="whistleblowing_counting/InstructionsTemplate.html",
            instructions_template_title="" + _(dict(en="Task 1 - Instructions", fr="Tâche 1 - Instructions")),
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


class CountingTask(MyPage):
    form_model = "player"
    form_fields = ["counting_performance"]
    timeout_seconds = Config.EFFORT_DURATION
    timer_text = _(dict(en="Remaining time:", fr="Temps restant :"))

    @staticmethod
    def vars_for_template(player: Player):
        existing = MyPage.vars_for_template(player)
        existing.update(
            dict(
                time=seconds_to_minutes(Config.EFFORT_DURATION),
                loop_grid_number=list(range(Config.NUM_GRIDS)),
                loop_rows=list(range(Config.GRID_SIZE[0])),
                loop_cols=list(range(Config.GRID_SIZE[1])),
            )
        )
        return existing

    @staticmethod
    def js_vars(player: Player):
        existing = MyPage.js_vars(player)
        existing["grids"] = player.session.vars[f"grids_g_{player.group.id_in_subsession}"]
        return existing

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened and player.session.config.get("test", False):
            player.participant._is_bot = True
            player.counting_performance = random.randint(0, 100)


class CountingEstimation(MyPage):
    form_model = "player"
    form_fields = ["counting_estimation"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.participant._is_bot = True
            player.counting_estimation = random.randint(0, 100)


class CountingWaitForAll(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        subsession.compute_payoffs()


page_sequence = [
    Instructions, InstructionsWaitForAll,
    CountingTask, CountingEstimation, CountingWaitForAll,
]
