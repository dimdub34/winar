from otree.api import *
import random

doc = """
Transition between part 1 and part 2 of the experiment.
"""


class C(BaseConstants):
    NAME_IN_URL = 'whtrans'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    def set_effort_task(self):
        for g in self.get_groups():
            players = g.get_players()
            effort_tasks = ["whistleblowing_counting", "whistleblowing_maths", "whistleblowing_sliders"]
            g.selected_effort_task_name = random.choice(effort_tasks)
            g.selected_effort_task_num = effort_tasks.index(g.selected_effort_task_name) + 1
            for p in players:
                p.set_txt_final()


    def creating_session(self):
        if "groups" not in self.session.vars:
            self.group_randomly()
            self.session.vars["groups"] = self.get_group_matrix()
        self.set_group_matrix(self.session.vars["groups"])

def creating_session(subsession: Subsession):
    subsession.creating_session()

class Group(BaseGroup):
    selected_effort_task_name = models.StringField()
    selected_effort_task_num = models.IntegerField()


class Player(BasePlayer):
    def set_txt_final(self):
        txt_final = (f"Task {self.group.selected_effort_task_num} has been randomly selected by the computer program "
                     f"to determine the payoff of your group.")
        txt_final += "<br>" + self.participant.vars[self.group.selected_effort_task_name]["txt_final"]

        self.participant.vars["whistleblowing_effort"] = dict(
            txt_final=txt_final,
            payoff_ecu=self.participant.vars[self.group.selected_effort_task_name]["payoff_ecu"],
            payoff=self.participant.vars[self.group.selected_effort_task_name]["payoff"]
        )


# PAGES
class Transition(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict()

    @staticmethod
    def js_vars(player: Player):
        return dict(
            fill_auto=player.session.config.get("fill_auto", False),
        )


class TransitionWaitForAll(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        subsession.set_effort_task()


page_sequence = [Transition, TransitionWaitForAll]
