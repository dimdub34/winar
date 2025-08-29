from otree.api import *
import random
from pathlib import Path
from . import understanding
from collections import Counter
from whistleblowing_commons.config import Config

doc = """
Stealing / Taking game
"""

app_name = Path(__file__).parent.name


def get_appropriate():
    return [
        (0, "Very inappropriate"), (1, "Inappropriate"), (2, "Rather inappropriate"),
        (3, "Rather appropriate"), (4, "Appropriate"), (5, "Very appropriate")
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
    understanding_faults_q1 = models.IntegerField()
    understanding_faults_q2 = models.IntegerField()
    understanding_faults_q3 = models.IntegerField()
    understanding_faults_q4 = models.IntegerField()
    understanding_faults_total = models.IntegerField()

    taker = models.BooleanField()
    taking_decision = models.BooleanField(
        label="Do you want to steal ECU from the Passive group?", widget=widgets.RadioSelectHorizontal)
    estimation_reporting = models.IntegerField(
        label="Please indicate what you think is the likelihood that a Blue Player reports the Red Player:",
        min=0, max=100)
    reporting_decision = models.BooleanField(
        label="Do you want to report the Red Player?", widget=widgets.RadioSelectHorizontal)
    audit_draw = models.FloatField()
    audit = models.BooleanField()
    payoff_ecu = models.FloatField()

    # Questions
    taker_motivation = models.LongStringField(
        label="Can you tell us what motivated your decision (as Red Player):")
    reporter_motivation = models.LongStringField(
        label="Can you tell us what motivated your decision (as Blue Player):")
    personal_opinion = models.IntegerField(
        label=("Please evaluate according to your own opinion and independently of the opinion of others whether "
               "it is appropriate or not to report the Red Player. "
               "“Appropriate” behavior means the behavior that you personally consider to be “correct” or “moral”. "
               "The standard is, hence, your personal opinion, independently of the opinion of others. "
               "We kindly ask you to answer as precisely as possible with your own honest opinion. "
               "There is no right or wrong answer; you will not get any additional payment for your answer to this "
               "question."),
        choices=get_appropriate(), widget=widgets.RadioSelect)
    society_opinion = models.IntegerField(
        label=(
            f"Now, please evaluate the opinion of the society and independently of your your opinion whether "
            f"it is appropriate or not to report the Red Player. 'Appropriate' behavior means the behavior "
            f"that you consider most people would agree upon as being 'correct' or 'moral'. "
            f"The standard is, hence, not your personal opinion, but your assessment of the opinion of the "
            f"society. We kindly ask you to answer as precisely as possible. For this question, you can "
            f"earn {Config.SOCIETY_OPTION_PAYOFF} ECU on top of your gains from the other parts of the experiment, "
            f"depending on your answer. The answers of the other participants will influence your payment for this "
            f"question. At the end, we will determine which answer to this question most of the other "
            f"participants gave. You will obtain {Config.SOCIETY_OPTION_PAYOFF} ECU if you gave the same answer as most of the "
            f"other participants. Example: suppose that you evaluate the action of reporting the Red Player "
            f"as 'Rather appropriate' and most of the other participants in this room evaluate the same "
            f"action as 'Rather appropriate'. Then, you earn {Config.SOCIETY_OPTION_PAYOFF} ECU for this question. "
            f"Note: all other participants have received the same instructions."
        ),
        choices=get_appropriate(), widget=widgets.RadioSelect)

    def compute_payoffs(self):
        if self.group.active:  # Active group
            txt_final = (
                f"Your group has been randomly selected to be an Active group. "
                f"Inside your group you have been selected to be a {'Red' if self.taker else 'Blue'} Player. "
            )

            if self.taker:  # Red Player
                if self.taking_decision:  # Taker
                    txt_final += f"You decided to steal ECU from the Passive group. "
                    if self.group.reporter_has_reported:
                        txt_final += f"You were reported by a Blue Player. "
                        if self.group.taker_audited:
                            txt_final += f"You were penalized {Config.STEALING_PENALTY} ECU. "
                            self.payoff_ecu = Config.STEALING_AMOUNT - Config.STEALING_PENALTY
                        else:
                            txt_final += f"You were not penalized. "
                            self.payoff_ecu = Config.STEALING_AMOUNT
                    else:
                        txt_final += f"You were not reported. "
                        self.payoff_ecu = Config.STEALING_AMOUNT

                else:  # Not Taker
                    txt_final += f"You decided not to steal some ECU from the Passive group. "
                    self.payoff_ecu = 0

            else:  # Blue Player
                if self.reporting_decision:  # Reporter
                    txt_final += f"You decided to report the Red Player. "
                    if self.group.taker_has_taken:
                        txt_final += "The Red Player has stolen some ECU from the Passive group. "
                        if self.group.selected_reporter == self.id_in_group:  # Selected
                            txt_final += f"You were selected to be the reporter. "
                            if self.group.taker_audited:
                                txt_final += "The Red Player was penalized. "
                                self.payoff_ecu = -Config.REPORTING_COST
                                if self.subsession.reward:
                                    txt_final += f"You received a reward of {Config.REPORTING_REWARD} ECU. "
                                    self.payoff_ecu += Config.REPORTING_REWARD
                            else:  # Not audited
                                txt_final += "The Red Player was not penalized. "
                                self.payoff_ecu = 0
                        else:  # Not selected
                            txt_final += "You were not selected to be the reporter. "
                            self.payoff_ecu = 0
                    else:  # Not Taker
                        txt_final += "The Red Player did not steal some ECU from the Passive group. "
                        self.payoff_ecu = 0

                else:  # Not Reporter
                    txt_final += f"You decided not to report the Red Player. "
                    self.payoff_ecu = 0

        else:  # Passive group
            txt_final = f"Your group has been randomly selected to be a Passive group. "
            if self.subsession.num_of_takers > 0:
                if self.subsession.num_of_takers == 1:
                    txt_final += (f"{self.subsession.num_of_takers} Red Player has decided to steal some ECU "
                                  f"from your group. ")
                else:
                    txt_final += (f"{self.subsession.num_of_takers} Red Players have decided to steal some ECU "
                                  f"from your group. ")
            else:
                txt_final += "No Red Player has decided to steal ECU from your group. "
            self.payoff_ecu = -self.subsession.num_of_takers * Config.STEALING_LOSS_INDIV

        # payoff for norm (question society_opinion)
        txt_final += "<br>" + (
            f"In the question on your assessment of the society's opinion, you have responded "
            f"<i>{get_appropriate()[self.society_opinion][1]}</i>. The majority of participants have responded "
            f"<i>{get_appropriate()[self.subsession.society_opinion_majority][1]}</i>.")

        if self.society_opinion == self.subsession.society_opinion_majority:
            self.payoff_ecu += Config.SOCIETY_OPTION_PAYOFF
            txt_final += " " + f"You earn {Config.SOCIETY_OPTION_PAYOFF} ECU for your answer."
        else:
            txt_final += " " + "You do not earn any ECU for your answer."

        txt_final += "<br>" + f"Your payoff for part 2 of the experiment is {self.payoff_ecu} ECU."
        self.payoff = (self.payoff_ecu * self.session.config["real_world_currency_per_point"])
        self.participant.vars[app_name] = dict(
            txt_final=txt_final, payoff_ecu=self.payoff_ecu, payoff=self.payoff
        )


# ======================================================================================================================
#
# -- PAGES --
#
# ======================================================================================================================


class MyPage(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(**Config.get_parameters())

    @staticmethod
    def js_vars(player: Player):
        return dict(
            fill_auto=player.session.config["fill_auto"],
            **Config.get_parameters()
        )


class Instructions(MyPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class InstructionsWaitMonitor(MyPage):
    @staticmethod
    def is_displayed(player):
        return Instructions.is_displayed(player)


class Understanding(MyPage):
    form_model = "player"
    form_fields = [f"understanding_faults_q{i}" for i in range(1, 5)]

    @staticmethod
    def vars_for_template(player: Player):
        existing = MyPage.vars_for_template(player)
        parameters = Config.get_parameters()
        parameters['reward'] = player.subsession.reward
        existing["understanding"] = understanding.get_understanding(parameters)
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
                setattr(player, f"understanding_faults_q{i}", random.randint(0, 2))
        player.understanding_faults_total = sum(getattr(player, f"understanding_faults_q{i}") for i in range(1, 5))


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
    Instructions,
    InstructionsWaitMonitor,
    Understanding,
    UnderstandingWaitForAll,
    GroupRole,
    DecisionTaking,
    EstimationReportingByTaker,
    DecisionReporting,
    Questionnaire,
    BeforeFinalWaitForAll, Final,
]
