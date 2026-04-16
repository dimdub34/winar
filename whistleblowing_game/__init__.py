import random
from collections import Counter
from pathlib import Path

from otree.api import *

from whistleblowing_commons.config import Config
from . import understanding

doc = """
Stealing / Taking game
"""

app_name = Path(__file__).parent.name


def get_appropriate():
    return [
        (0, "Very inappropriate"),
        (1, "Inappropriate"),
        (2, "Rather inappropriate"),
        (3, "Rather appropriate"),
        (4, "Appropriate"),
        (5, "Very appropriate"),
    ]


class C(BaseConstants):
    NAME_IN_URL = "whgame"
    PLAYERS_PER_GROUP = Config.PLAYERS_PER_GROUP
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    reward = models.BooleanField()
    num_of_takers = models.IntegerField()
    num_of_reporters = models.IntegerField()
    society_opinion_majority = models.IntegerField()

    def creating_session(self):
        self.reward = self.session.config.get("reward", False)

        if "groups" not in self.session.vars:
            self.group_randomly()
            self.session.vars["groups"] = self.get_group_matrix()
        self.set_group_matrix(self.session.vars["groups"])

        inactive_group = random.choice(self.get_groups())
        for g in self.get_groups():
            g.active = g != inactive_group

        active_groups = [g for g in self.get_groups() if g.active]
        for g in active_groups:
            players = g.get_players()
            taker = random.choice(players)
            for p in players:
                p.taker = p == taker

    def compute_payoffs(self):
        active_groups = [g for g in self.get_groups() if g.active]
        for g in active_groups:
            players = g.get_players()
            reporters = [p for p in players if not p.taker]
            selected_reporter = random.choice(reporters)
            g.selected_reporter = selected_reporter.id_in_group
            g.reporter_has_reported = selected_reporter.reporting_decision

            if g.taker_has_taken and g.reporter_has_reported:
                g.audit_draw = random.uniform(0, 1)
                g.taker_audited = g.audit_draw < Config.AUDIT_PROBABILITY

        self.num_of_takers = sum([g.taker_has_taken for g in active_groups])
        self.num_of_reporters = sum(
            [p.reporting_decision for p in self.get_players() if p.group.active and not p.taker])

        soc_op_maj = [p.society_opinion for p in self.get_players()]
        soc_op_maj_count = Counter(soc_op_maj)
        self.society_opinion_majority = int(soc_op_maj_count.most_common(1)[0][0])

        for p in self.get_players():
            p.compute_payoffs()


def creating_session(subsession: Subsession):
    subsession.creating_session()


class Group(BaseGroup):
    active = models.BooleanField()
    taker_has_taken = models.BooleanField(initial=False)
    selected_reporter = models.IntegerField()
    reporter_has_reported = models.BooleanField(initial=False)
    audit_draw = models.FloatField()
    taker_audited = models.BooleanField(initial=False)


class Player(BasePlayer):
    # understanding questionnaire
    game_q1_faults = models.IntegerField()
    game_q2_faults = models.IntegerField()
    game_q3_faults = models.IntegerField()
    game_q4_faults = models.IntegerField()
    game_total_faults = models.IntegerField()

    taker = models.BooleanField()
    taking_decision = models.BooleanField(
        label="Do you want to steal ECU from the Passive group?",
        widget=widgets.RadioSelectHorizontal,
    )
    estimation_reporting = models.IntegerField(
        label="Please indicate what you think is the likelihood that a Blue Player reports the Red Player:",
        min=0,
        max=100,
    )
    reporting_decision = models.BooleanField(
        label="Do you want to report the Red Player?",
        widget=widgets.RadioSelectHorizontal,
    )
    audit_draw = models.FloatField()
    audit = models.BooleanField()
    payoff_ecu = models.FloatField()

    # Questions
    taker_motivation = models.LongStringField(
        label="Can you tell us what motivated your decision (as Red Player):"
    )
    reporter_motivation = models.LongStringField(
        label="Can you tell us what motivated your decision (as Blue Player) to report or not the Red Player:"
    )
    personal_opinion = models.IntegerField(
        label="Please evaluate according to your own opinion and independently of the opinion of others whether "
              "it is appropriate or not to report the Red Player. "
              "'Appropriate' behavior means the behavior that you personally consider to be 'correct' or 'moral'. "
              "The standard is, hence, your personal opinion, independently of the opinion of others. "
              "We kindly ask you to answer as precisely as possible with your own honest opinion. "
              "There is no right or wrong answer; you will not get any additional payment for your answer to this "
              "question.",
        choices=get_appropriate(),
        widget=widgets.RadioSelect,
    )
    society_opinion = models.IntegerField(
        label=f"Now, please evaluate the opinion of society and independently of your own opinion whether "
              f"it is appropriate or not to report the Red Player. 'Appropriate' behavior means behavior "
              f"that you think most people would agree is 'correct' or 'moral'. "
              f"The standard is therefore not your personal opinion, but your assessment of society's opinion. "
              f"Please answer as precisely as possible. For this question, you can earn "
              f"{Config.SOCIETY_OPTION_PAYOFF} ECU on top of your gains from the other parts of the experiment, "
              f"depending on your answer. The answers of the other participants will influence your payment for this "
              f"question. At the end, we will determine which answer to this question most participants gave. "
              f"You will obtain {Config.SOCIETY_OPTION_PAYOFF} ECU if you gave the same answer as most participants. "
              f"Example: suppose that you evaluate reporting the Red Player as 'Rather appropriate' and most "
              f"participants in this room evaluate it the same way. Then you earn "
              f"{Config.SOCIETY_OPTION_PAYOFF} ECU for this question. "
              f"Note: all participants received the same instructions.",
        choices=get_appropriate(), widget=widgets.RadioSelect)

    def compute_payoffs(self):
        # --- Active group ---
        if self.group.active:
            txt_final = (
                f"Your group has been randomly selected to be an Active group. "
                f"Inside your group you had the role of a {'Red' if self.taker else 'Blue'} Player. "
            )

            if self.taker:  # Red Player
                if self.taking_decision:  # Taker
                    txt_final += "You decided to steal ECU from the Passive group. "

                    if self.group.reporter_has_reported:  # Reported
                        txt_final += "The selected Blue Player has decided to report you. "

                        if self.group.taker_audited:  # Audited
                            txt_final += f"You were audited and fined {Config.STEALING_PENALTY} ECU. "
                            self.payoff_ecu = Config.STEALING_AMOUNT - Config.STEALING_PENALTY

                        else:  # Not Audited
                            txt_final += "You were not audited. "
                            self.payoff_ecu = Config.STEALING_AMOUNT

                    else:  # Not Reported
                        txt_final += "You were not reported. "
                        self.payoff_ecu = Config.STEALING_AMOUNT

                else:  # Not Taker
                    txt_final += "You decided not to steal ECU from the Passive group. "
                    self.payoff_ecu = 0

            else:  # Blue Player
                # Defensive initialization for all Blue Player branches.
                self.payoff_ecu = 0

                if self.reporting_decision:  # Reporter
                    txt_final += "You decided to report the Red Player. "

                    # Case 1: Blue Player is selected.
                    if self.group.selected_reporter == self.id_in_group:
                        txt_final += "You were selected to be the reporter. "

                        if self.group.taker_has_taken:  # Taker stole
                            txt_final += "The Red Player has stolen ECU from the Passive group. "
                            self.payoff_ecu = -Config.REPORTING_COST

                            if self.group.taker_audited:  # Audited
                                txt_final += "The Red Player was audited and fined. "

                                if self.subsession.reward:  # With reward
                                    txt_final += f"You received a reward of {Config.REPORTING_REWARD} ECU. "
                                    self.payoff_ecu += Config.REPORTING_REWARD

                            else:  # Not audited
                                txt_final += "The Red Player was not audited. "

                        else:  # Taker did not steal
                            txt_final += "The Red Player did not steal ECU from the Passive group. "

                    # Case 2: Blue Player is not selected.
                    else:
                        txt_final += "You were not selected to be the reporter. "

                        # Keep payoff at 0, but still inform the player about the Red decision.
                        if self.group.taker_has_taken:
                            txt_final += "The Red Player has stolen ECU from the Passive group. "

                        else:
                            txt_final += "The Red Player did not steal ECU from the Passive group. "

                else:  # Not Reporter
                    txt_final += "You decided not to report the Red Player. "

        # --- Passive group ---
        else:
            txt_final = "Your group has been randomly selected to be a Passive group. "

            if self.subsession.num_of_takers > 0:  # At least one taker
                if self.subsession.num_of_takers == 1:
                    txt_final += f"{self.subsession.num_of_takers} Red Player has decided to steal ECU from your group. "
                else:
                    txt_final += f"{self.subsession.num_of_takers} Red Players have decided to steal ECU from your group. "
            else:
                txt_final += "No Red Player has decided to steal ECU from your group. "
            self.payoff_ecu = -self.subsession.num_of_takers * Config.STEALING_LOSS_INDIV

        game_payoff = self.payoff_ecu

        # -- payoff for norm (question society_opinion) ---
        txt_final += (
            "<br>"
            f"In the question on your assessment of society's opinion, you responded "
            f"<i>{get_appropriate()[self.society_opinion][1]}</i>. "
            f"The majority of participants responded "
            f"<i>{get_appropriate()[self.subsession.society_opinion_majority][1]}</i>."
        )

        norm_payoff = 0
        if self.society_opinion == self.subsession.society_opinion_majority:
            norm_payoff = Config.SOCIETY_OPTION_PAYOFF
            self.payoff_ecu += norm_payoff
            txt_final += f" You earn {Config.SOCIETY_OPTION_PAYOFF} ECU for your answer."

        txt_final += (
            "<br>"
            f"Your payoff for part 2 of the experiment is {self.payoff_ecu} ECU "
            f"(Game: {game_payoff} ECU + Opinion: {norm_payoff} ECU)."
        )
        self.participant.vars[app_name] = dict(
            txt_final=txt_final,
            payoff_ecu=self.payoff_ecu,
            payoff=self.payoff_ecu * self.session.config["real_world_currency_per_point"])


# ======================================================================================================================
#
# -- PAGES --
#
# ======================================================================================================================


class MyPage(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            instructions_template_path="whistleblowing_game/InstructionsTemplate.html",
            instructions_template_title="Part 2 - Instructions",
            en=True,
            fr=False,
            **Config.get_parameters()
        )

    @staticmethod
    def js_vars(player: Player):
        return dict(
            fill_auto=player.session.config.get("fill_auto", False),
            **Config.get_parameters(),
            en=True,
            fr=False,
        )


class Instructions(MyPage):
    template_name = "global/Instructions.html"


class InstructionsWaitMonitor(MyPage):
    template_name = "global/InstructionsWaitMonitor.html"

    @staticmethod
    def is_displayed(player):
        return Instructions.is_displayed(player)


class InstructionsWaitForAll(WaitPage):
    wait_for_all_groups = True
    template_name = "global/InstructionsWaitPage.html"

    @staticmethod
    def vars_for_template(player: Player):
        return MyPage.vars_for_template(player)


class Understanding(MyPage):
    template_name = "global/Understanding.html"
    form_model = "player"
    form_fields = [f"game_q{i}_faults" for i in range(1, 5)]

    @staticmethod
    def vars_for_template(player: Player):
        existing = MyPage.vars_for_template(player)
        parameters = Config.get_parameters()
        parameters.update(reward=player.subsession.reward)
        existing.update(understanding=understanding.get_understanding(parameters))
        return existing

    @staticmethod
    def js_vars(player: Player):
        existing = MyPage.js_vars(player)
        existing["understanding"] = Understanding.vars_for_template(player)["understanding"]
        return existing

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.participant._is_bot = True
            for i in range(1, 5):
                setattr(player, f"game_q{i}_faults", random.randint(0, 2))
        player.game_total_faults = sum(
            getattr(player, f"game_q{i}_faults") for i in range(1, 5)
        )


class UnderstandingWaitForAll(WaitPage):
    wait_for_all_groups = True


class GroupRole(MyPage):
    pass


class DecisionTaking(MyPage):
    form_model = "player"
    form_fields = ["taking_decision"]

    @staticmethod
    def is_displayed(player):
        return player.group.active and player.taker

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.participant._is_bot = True
            player.taking_decision = random.choice([True, False])
        player.group.taker_has_taken = player.taking_decision


class EstimationReportingByTaker(MyPage):
    form_model = "player"
    form_fields = ["estimation_reporting"]

    @staticmethod
    def is_displayed(player: Player):
        return player.group.active and player.taker

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.participant._is_bot = True
            player.estimation_reporting = random.randint(0, 100)


class DecisionReporting(MyPage):
    form_model = "player"
    form_fields = ["reporting_decision"]

    @staticmethod
    def is_displayed(player):
        return player.group.active and not player.taker

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.participant._is_bot = True
            player.reporting_decision = random.choice([True, False])


class Questionnaire(MyPage):
    form_model = "player"

    @staticmethod
    def get_form_fields(player: Player):
        fields = []
        if player.group.active:
            if player.taker:
                fields.append("taker_motivation")
            else:
                fields.append("reporter_motivation")
        fields.extend(["personal_opinion", "society_opinion"])
        return fields

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.participant._is_bot = True
            fields = Questionnaire.get_form_fields(player)
            if "taker_motivation" in fields:
                player.taker_motivation = "Explanation for stealing decision"
            if "reporter_motivation" in fields:
                player.reporter_motivation = "Explanation for reporting decision"
            player.personal_opinion = random.randint(0, 5)
            player.society_opinion = random.randint(0, 5)


class BeforeFinalWaitForAll(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        subsession.compute_payoffs()


class Final(MyPage):
    pass


page_sequence = [
    Instructions, InstructionsWaitForAll,
    # InstructionsWaitMonitor,
    Understanding, UnderstandingWaitForAll,
    GroupRole,
    DecisionTaking, EstimationReportingByTaker,
    DecisionReporting,
    Questionnaire,
    BeforeFinalWaitForAll, Final,
]
