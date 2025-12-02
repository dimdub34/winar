import random
from collections import Counter
from pathlib import Path

from otree.api import *

from settings import LANGUAGE_CODE
from whistleblowing_commons.config import Config, language, _
from . import understanding

doc = """
Stealing / Taking game
"""

app_name = Path(__file__).parent.name


def get_appropriate():
    return [
        (0, _(dict(en="Very inappropriate", fr="Très inapproprié"))),
        (1, _(dict(en="Inappropriate", fr="Inapproprié"))),
        (2, _(dict(en="Rather inappropriate", fr="Plutôt inapproprié"))),
        (3, _(dict(en="Rather appropriate", fr="Plutôt approprié"))),
        (4, _(dict(en="Appropriate", fr="Approprié"))),
        (5, _(dict(en="Very appropriate", fr="Très approprié"))),
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
        label=_(dict(
            en="Do you want to steal ECU from the Passive group?",
            fr="Souhaitez-vous voler des ECU au groupe Passif ?",
        )), widget=widgets.RadioSelectHorizontal)
    estimation_reporting = models.IntegerField(
        label=_(dict(
            en="Please indicate what you think is the likelihood that a Blue Player reports the Red Player:",
            fr="Veuillez indiquer quelles sont les chances qu'un joueur Bleu dénonce le joueur Rouge :",
        )), min=0, max=100)
    reporting_decision = models.BooleanField(
        label=_(dict(
            en="Do you want to report the Red Player?",
            fr="Souhaitez-vous signaler le joueur Rouge ?",
        )), widget=widgets.RadioSelectHorizontal)
    audit_draw = models.FloatField()
    audit = models.BooleanField()
    payoff_ecu = models.FloatField()

    # Questions
    taker_motivation = models.LongStringField(
        label=_(dict(
            en="Can you tell us what motivated your decision (as Red Player):",
            fr="Pouvez-vous nous expliquer ce qui a motivé votre décision (comme joueur Rouge) :",
        )))
    reporter_motivation = models.LongStringField(
        label=_(dict(
            en="Can you tell us what motivated your decision (as Blue Player) to report or not the Red Player:",
            fr="Pouvez-vous nous expliquer ce qui a motivé votre décision (comme joueur Bleu) de signaler ou non "
               "le joueur Rouge :",
        )))
    personal_opinion = models.IntegerField(
        label=_(dict(
            en="Please evaluate according to your own opinion and independently of the opinion of others whether "
               "it is appropriate or not to report the Red Player. "
               "“Appropriate” behavior means the behavior that you personally consider to be “correct” or “moral”. "
               "The standard is, hence, your personal opinion, independently of the opinion of others. "
               "We kindly ask you to answer as precisely as possible with your own honest opinion. "
               "There is no right or wrong answer; you will not get any additional payment for your answer to this "
               "question.",
            fr="Veuillez évaluer, selon votre propre opinion et indépendamment de l'opinion des autres, s'il est "
               "approprié ou non de signaler le joueur Rouge. Un comportement 'approprié' signifie un comportement "
               "que vous considérez personnellement "
               "comme 'correct' ou 'moral'. La norme est donc votre opinion personnelle, indépendamment de celle "
               "des autres. Nous vous demandons de répondre aussi précisément que possible avec votre propre opinion "
               "honnête. Il n'y a pas de bonne ou de mauvaise réponse ; vous ne recevrez aucun paiement "
               "supplémentaire pour votre réponse à cette question.",
        )),
        choices=[
            (0, _(dict(en="Very inappropriate", fr="Très inapproprié"))),
            (1, _(dict(en="Inappropriate", fr="Inapproprié"))),
            (2, _(dict(en="Rather inappropriate", fr="Plutôt inapproprié"))),
            (3, _(dict(en="Rather appropriate", fr="Plutôt approprié"))),
            (4, _(dict(en="Appropriate", fr="Approprié"))),
            (5, _(dict(en="Very appropriate", fr="Très approprié"))),
        ], widget=widgets.RadioSelect)
    society_opinion = models.IntegerField(
        label=_(dict(
            en=f"Now, please evaluate the opinion of the society and independently of your opinion whether "
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
               f"Note: all other participants have received the same instructions.",
            fr=f"Veuillez maintenant évaluer l'opinion de la société, indépendamment de votre propre opinion, sur le fait "
               f"qu'il soit approprié ou non de signaler le joueur Rouge. Un comportement 'approprié' signifie un comportement "
               f"que vous considérez comme étant généralement accepté par la majorité des gens comme 'correct' ou 'moral'. "
               f"La norme n'est donc pas votre opinion personnelle, mais votre évaluation de l'opinion de la société. "
               f"Nous vous demandons de répondre aussi précisément que possible. Pour cette question, vous pouvez "
               f"gagner {Config.SOCIETY_OPTION_PAYOFF} ECU en plus de vos gains des autres parties de l'expérience, "
               f"en fonction de votre réponse. Les réponses des autres participants influenceront votre paiement pour cette "
               f"question. À la fin, nous déterminerons quelle réponse à cette question a été donnée par la majorité des autres "
               f"participants. Vous obtiendrez {Config.SOCIETY_OPTION_PAYOFF} ECU si vous avez donné la même réponse que la majorité des "
               f"autres participants. Exemple : supposons que vous évaluez l'action de dénoncer le joueur Rouge "
               f"comme 'Plutôt approprié' et que la majorité des autres participants dans cette salle évaluent également cette "
               f"action comme 'Plutôt approprié'. Dans ce cas, vous gagnez {Config.SOCIETY_OPTION_PAYOFF} ECU pour cette question. "
               f"Note : tous les autres participants ont reçu les mêmes instructions.",
        )),
        choices=get_appropriate(), widget=widgets.RadioSelect)

    def compute_payoffs(self):
        # --- Active group ---
        if self.group.active:
            txt_final = _(dict(
                en=f"Your group has been randomly selected to be an Active group. "
                   f"Inside your group you had the role of a {'Red' if self.taker else 'Blue'} Player. ",
                fr=f"Votre groupe a été tiré au sort pour être un groupe Actif. "
                   f"Dans votre groupe, vous avez eu le rôle de joueur "
                   f"{'Rouge' if self.taker else 'Bleu'}. "))

            if self.taker:  # Red Player
                if self.taking_decision:  # Taker
                    txt_final += _(dict(
                        en=f"You decided to steal ECU from the Passive group. ",
                        fr=f"Vous avez décidé de voler des ECU au groupe Passif. "))

                    if self.group.reporter_has_reported:  # Reported
                        txt_final += _(dict(
                            en=f"The selected Blue Player has decided to report you. ",
                            fr=f"Le joueur Bleu sélectionné a décidé de vous signalez. "))

                        if self.group.taker_audited:  # Audited
                            txt_final += _(dict(
                                en=f"You were audited and fined {Config.STEALING_PENALTY} ECU. ",
                                fr=f"Vous avez été pénalisé d'un montant de {Config.STEALING_PENALTY} ECU. "))
                            self.payoff_ecu = Config.STEALING_AMOUNT - Config.STEALING_PENALTY

                        else:  # Not Audited
                            txt_final += _(dict(
                                en=f"You were not audited. ",
                                fr=f"Vous n'avez pas été pénalisé. "))
                            self.payoff_ecu = Config.STEALING_AMOUNT

                    else:  # Not Reported
                        txt_final += _(dict(
                            en=f"You were not reported. ",
                            fr=f"Vous n'avez pas été signalé. "))
                        self.payoff_ecu = Config.STEALING_AMOUNT

                else:  # Not Taker
                    txt_final += _(dict(
                        en=f"You decided not to steal some ECU from the Passive group. ",
                        fr=f"Vous avez décidé de ne pas voler d'ECU au groupe Passif. "))
                    self.payoff_ecu = 0

            else:  # Blue Player
                # Initialisation par sécurité (couvre le cas "Not Reporter" et "Reporter non sélectionné")
                self.payoff_ecu = 0

                if self.reporting_decision:  # Reporter
                    txt_final += _(dict(
                        en=f"You decided to report the Red Player. ",
                        fr=f"Vous avez décidé de signaler le joueur Rouge. "))

                    # Case 1 : Blue Player is selected
                    if self.group.selected_reporter == self.id_in_group:
                        txt_final += _(dict(
                            en=f"You were selected to be the reporter. ",
                            fr=f"Votre décision de signalement a été sélectionnée. "))

                        if self.group.taker_has_taken:  # Taker stole
                            txt_final += _(dict(
                                en="The Red Player has stolen some ECU from the Passive group. ",
                                fr="Le joueur Rouge a volé des ECU au groupe Passif. "))
                            self.payoff_ecu = -Config.REPORTING_COST  # Paye le coût de reporting

                            if self.group.taker_audited:  # Audited
                                txt_final += _(dict(
                                    en="The Red Player was audited and fined. ",
                                    fr="Le joueur Rouge a été pénalisé. "))

                                if self.subsession.reward:  # With reward
                                    txt_final += _(dict(
                                        en=f"You received a reward of {Config.REPORTING_REWARD} ECU. ",
                                        fr=f"Vous avez reçu une récompense de {Config.REPORTING_REWARD} ECU. "))
                                    self.payoff_ecu += Config.REPORTING_REWARD

                            else:  # Not audited
                                txt_final += _(dict(
                                    en="The Red Player was not audited. ",
                                    fr="Le joueur Rouge n'a pas été pénalisé. "))

                        else:  # Taker did not steal
                            txt_final += _(dict(
                                en="The Red Player did not steal some ECU from the Passive group. ",
                                fr="Le joueur Rouge n'a pas volé d'ECU au groupe Passif. "))
                            # Pas de changement de payoff_ecu (reste à 0)

                    # Case 2 : Blue Player is not selected
                    else:
                        txt_final += _(dict(
                            en="You were not selected to be the reporter. ",
                            fr="Votre décision de signalement n'a pas été sélectionnée. "))

                        # Payoff reste à 0, mais on informe quand même de ce qu'a fait le Rouge
                        if self.group.taker_has_taken:
                            txt_final += _(dict(
                                en="The Red Player has stolen some ECU from the Passive group. ",
                                fr="Le joueur Rouge a volé des ECU au groupe Passif. "))

                        else:
                            txt_final += _(dict(
                                en="The Red Player did not steal some ECU from the Passive group. ",
                                fr="Le joueur Rouge n'a pas volé d'ECU au groupe Passif. ",
                            ))

                else:  # Not Reporter
                    txt_final += _(dict(
                        en=f"You decided not to report the Red Player. ",
                        fr=f"Vous avez décidé de ne pas signaler le joueur Rouge. "))
                    # self.payoff_ecu est déjà à 0

        # --- Passive group ---
        else:
            txt_final = _(dict(
                en=f"Your group has been randomly selected to be a Passive group. ",
                fr=f"Votre groupe a été tiré au sort pour être un groupe Passif. ",
            ))

            if self.subsession.num_of_takers > 0:  # At least one taker
                if self.subsession.num_of_takers == 1:
                    txt_final += _(dict(
                        en=f"{self.subsession.num_of_takers} Red Player has decided to steal some ECU from your group. ",
                        fr=f"{self.subsession.num_of_takers} joueur Rouge a décidé de voler des ECU à votre groupe. ",
                    ))
                else:
                    txt_final += _(dict(
                        en=f"{self.subsession.num_of_takers} Red Players have decided to steal some ECU from your group. ",
                        fr=f"{self.subsession.num_of_takers} joueurs Rouges ont décidé de voler des ECU à votre groupe. ",
                    ))
            else:
                txt_final += _(dict(
                    en="No Red Player has decided to steal ECU from your group. ",
                    fr="Aucun joueur Rouge n'a décidé de voler des ECU à votre groupe. ",
                ))
            self.payoff_ecu = -self.subsession.num_of_takers * Config.STEALING_LOSS_INDIV

        game_payoff = self.payoff_ecu

        # -- payoff for norm (question society_opinion) ---
        txt_final += "<br>" + _(dict(
            fr=f"A la question sur votre évaluation de l'opinion de la société, vous avez répondu "
               f"<i>{get_appropriate()[self.society_opinion][1]}</i>. La majorité des participants a répondu "
               f"<i>{get_appropriate()[self.subsession.society_opinion_majority][1]}</i>.",
            en=f"In the question on your assessment of the society's opinion, you have responded "
               f"<i>{get_appropriate()[self.society_opinion][1]}</i>. The majority of participants have responded "
               f"<i>{get_appropriate()[self.subsession.society_opinion_majority][1]}</i>."
        ))

        norm_payoff = 0
        if self.society_opinion == self.subsession.society_opinion_majority:
            norm_payoff = Config.SOCIETY_OPTION_PAYOFF
            self.payoff_ecu += norm_payoff
            txt_final += " " + _(dict(
                fr=f"Vous gagnez donc {Config.SOCIETY_OPTION_PAYOFF} ECU pour votre réponse.",
                en=f"You earn {Config.SOCIETY_OPTION_PAYOFF} ECU for your answer."
            ))

        txt_final += "<br>" + _(
            dict(
                en=f"Your payoff for part 2 of the experiment is {self.payoff_ecu} ECU "
                   f"(Game: {game_payoff} ECU + Opinion: {norm_payoff} ECU).",
                fr=f"Votre gain pour la partie 2 de l'expérience est de {self.payoff_ecu} ECU "
                   f"(Jeu : {game_payoff} ECU + Opinion : {norm_payoff} ECU).",
            )
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
            instructions_template_title=_(dict(en="Part 2 - Instructions", fr="Partie 2 - Instructions")),
            **language,
            **Config.get_parameters()
        )

    @staticmethod
    def js_vars(player: Player):
        return dict(
            fill_auto=player.session.config.get("fill_auto", False),
            **Config.get_parameters(),
            **language
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
        existing.update(understanding=understanding.get_understanding(parameters, LANGUAGE_CODE))
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
