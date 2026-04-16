import random
from pathlib import Path

from otree.api import *

from .fields_labels_choices import *

doc = """
Narratives on Climate Change
"""

app_name = Path(__file__).parent.name


# ======================================================================================================================
class C(BaseConstants):
    NAME_IN_URL = 'clquest'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    if "lang" not in subsession.session.vars:
        lang = subsession.session.config.get("language", "en")
        subsession.session.vars["lang"] = lang

    if app_name not in subsession.session.vars:
        subsession.session.vars[app_name] = dict()

    amounts = [0.01, 0.25, 0.5, 1, 1.5, 2, 2.5]
    subsession.session.vars[app_name]["amounts"] = amounts.copy()

    players = subsession.get_players()
    k = max(1, len(players) // 10)  # 10% of participants with a minimum of 1
    subsession.session.vars[app_name]["num_selected"] = k
    selected_players = random.sample(players, k=k)
    for p in players:
        p.is_selected = (p in selected_players)
        if p.is_selected:
            p.random_row = random.choice(range(len(amounts)))
            p.random_amount = subsession.session.vars[app_name]["amounts"][p.random_row]


class Group(BaseGroup):
    pass


# --- PLAYER ---

class Player(BasePlayer):
    skip = models.BooleanField()

    # Narrative elicitation --------------------------------------------------------------------------------------------
    climate_exists = models.BooleanField(widget=widgets.RadioSelectHorizontal)
    narrative_elicitation = models.LongStringField()
    narrative_confidence = models.IntegerField()

    # Narrative sharing ------------------------------------------------------------------------------------------------
    sharing_narrative = models.FloatField(max=10)

    # MPL fields -------------------------------------------------------------------------------------------------------
    choice_1 = models.StringField(widget=widgets.RadioSelectHorizontal)
    choice_2 = models.StringField(widget=widgets.RadioSelectHorizontal)
    choice_3 = models.StringField(widget=widgets.RadioSelectHorizontal)
    choice_4 = models.StringField(widget=widgets.RadioSelectHorizontal)
    choice_5 = models.StringField(widget=widgets.RadioSelectHorizontal)
    choice_6 = models.StringField(widget=widgets.RadioSelectHorizontal)
    choice_7 = models.StringField(widget=widgets.RadioSelectHorizontal)

    is_selected = models.BooleanField(initial=False)
    random_row = models.IntegerField(initial=None)
    random_amount = models.FloatField(initial=None)
    # payoff_mpl = models.FloatField()

    # Policy narrative -------------------------------------------------------------------------------------------------
    policy_fight = models.IntegerField(widget=widgets.RadioSelectHorizontal)
    policy_narrative = models.LongStringField()
    confidence_policy = models.IntegerField()

    # Policy expectations ----------------------------------------------------------------------------------------------
    expectations_policy_economy = models.IntegerField(widget=widgets.RadioSelectHorizontal)
    expectations_policy_cc = models.IntegerField(widget=widgets.RadioSelectHorizontal)
    expectations_policy_household = models.IntegerField(widget=widgets.RadioSelectHorizontal)
    agreement_policy = models.IntegerField(widget=widgets.RadioSelectHorizontal)

    # Climate knowledge ------------------------------------------------------------------------------------------------
    climate_knowledge = models.IntegerField(widget=widgets.RadioSelectHorizontal)
    rank_coal = models.IntegerField(choices=[1, 2, 3],
                                    widget=widgets.RadioSelectHorizontal)  # Choix numériques fixes OK
    rank_gas = models.IntegerField(choices=[1, 2, 3], widget=widgets.RadioSelectHorizontal)
    rank_nuclear = models.IntegerField(choices=[1, 2, 3], widget=widgets.RadioSelectHorizontal)

    # Media - Frequencies ----------------------------------------------------------------------------------------------
    info_freq = models.StringField(widget=widgets.RadioSelectHorizontal)
    climate_info_freq = models.StringField(widget=widgets.RadioSelectHorizontal)

    # Media - ----------------------------------------------------------------------------------------------------------
    use_tv = models.IntegerField(choices=range(1, 8), widget=widgets.RadioSelectHorizontal)
    use_newspapers = models.IntegerField(choices=range(1, 8), widget=widgets.RadioSelectHorizontal)
    use_radio = models.IntegerField(choices=range(1, 8), widget=widgets.RadioSelectHorizontal)
    use_social = models.IntegerField(choices=range(1, 8), widget=widgets.RadioSelectHorizontal)
    use_online = models.IntegerField(choices=range(1, 8), widget=widgets.RadioSelectHorizontal)
    use_newsletters = models.IntegerField(choices=range(1, 8), widget=widgets.RadioSelectHorizontal)

    use_tv_climate = models.IntegerField(choices=range(1, 8), widget=widgets.RadioSelectHorizontal)
    use_newspapers_climate = models.IntegerField(choices=range(1, 8), widget=widgets.RadioSelectHorizontal)
    use_radio_climate = models.IntegerField(choices=range(1, 8), widget=widgets.RadioSelectHorizontal)
    use_social_climate = models.IntegerField(choices=range(1, 8), widget=widgets.RadioSelectHorizontal)
    use_online_climate = models.IntegerField(choices=range(1, 8), widget=widgets.RadioSelectHorizontal)
    use_newsletters_climate = models.IntegerField(choices=range(1, 8), widget=widgets.RadioSelectHorizontal)

    # Concern ----------------------------------------------------------------------------------------------------------
    climate_threat = models.IntegerField(widget=widgets.RadioSelectHorizontal)

    # Willingness to act -----------------------------------------------------------------------------------------------
    limit_flying = models.IntegerField(widget=widgets.RadioSelectHorizontal)
    limit_driving = models.IntegerField(widget=widgets.RadioSelectHorizontal)
    electric_vehicle = models.IntegerField(widget=widgets.RadioSelectHorizontal)
    limit_beef = models.IntegerField(widget=widgets.RadioSelectHorizontal)
    limit_heating = models.IntegerField(widget=widgets.RadioSelectHorizontal)

    # Policy support ---------------------------------------------------------------------------------------------------
    tax_flying = models.StringField(widget=widgets.RadioSelectHorizontal)
    tax_fossil = models.StringField(widget=widgets.RadioSelectHorizontal)
    ban_polluting = models.StringField(widget=widgets.RadioSelectHorizontal)
    subsidy_lowcarbon = models.StringField(widget=widgets.RadioSelectHorizontal)
    climate_fund = models.StringField(widget=widgets.RadioSelectHorizontal)

    # Expectations -----------------------------------------------------------------------------------------------------
    expectations_droughts = models.StringField(widget=widgets.RadioSelectHorizontal)
    expectations_eruptions = models.StringField(widget=widgets.RadioSelectHorizontal)
    expectations_sea = models.StringField(widget=widgets.RadioSelectHorizontal)
    expectations_agriculture = models.StringField(widget=widgets.RadioSelectHorizontal)
    expectations_living = models.StringField(widget=widgets.RadioSelectHorizontal)
    expectations_migration = models.StringField(widget=widgets.RadioSelectHorizontal)
    expectations_conflicts = models.StringField(widget=widgets.RadioSelectHorizontal)
    expectations_extinction = models.StringField(widget=widgets.RadioSelectHorizontal)

    # Circadian --------------------------------------------------------------------------------------------------------
    circadian = models.StringField()

    # Demographics -----------------------------------------------------------------------------------------------------
    income = models.IntegerField()
    education = models.IntegerField()

    def set_payoff_mpl(self):
        lang = self.session.vars["lang"]
        amounts = self.session.vars[app_name]["amounts"]
        txt_final = ""
        if self.is_selected:
            choice_vars = [self.choice_1, self.choice_2, self.choice_3, self.choice_4,
                           self.choice_5, self.choice_6, self.choice_7]

            # Safety check for bot or missing data
            if self.random_row is not None and self.random_row < len(choice_vars):
                chosen_choice = choice_vars[self.random_row]

                # Explanation text
                # We add 1 to the row index to match human counting (1-based)
                row_display = self.random_row + 1

                txt_final += (f"For the incentivized task of the questionnaire, row #{row_display} of the "
                              f"questionnaire was randomly selected. ")

                if chosen_choice == "B":
                    self.payoff = cu(self.random_amount)
                    txt_final += (f"For this row, you chose Option B (Receive a monetary amount). "
                                  f"Therefore, your opinion will not be shared, and you receive {self.payoff}.")
                else:
                    self.payoff = cu(0)
                    txt_final += ("For this row, you chose Option A (Give my opinion). "
                                  "Therefore, your opinion will be shared with future participants, and you "
                                  "receive {self.payoff}.")
            else:
                self.payoff = cu(0)
                txt_final = ("An error occurred during the selection process of the incentivized task of "
                             "the questionnaire.")

        else:
            txt_final = "You were not selected for the incentivized task payment of the questionnaire."

        app_dict = self.participant.vars.setdefault(app_name, {})
        app_dict["is_selected"] = self.is_selected
        app_dict["txt_final"] = txt_final
        app_dict["payoff"] = self.payoff


# ======================================================================================================================
# -- PAGES --
# ======================================================================================================================

class MyPage(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
        )

    @staticmethod
    def js_vars(player: Player):
        return dict(
            fill_auto=player.session.config.get("fill_auto", False),
        )


class Presentation(MyPage):
    form_model = 'player'
    form_fields = ["skip"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.skip = random.choice([True, False])
        app_dict = player.participant.vars.setdefault(app_name, {})
        app_dict["skip"] = player.skip

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.skip:
            try:
                return upcoming_apps[-1]
            except IndexError:
                return None
        else:
            return None


class NarrativeElicitation_text(MyPage):
    pass


class NarrativeElicitation_question(MyPage):
    form_model = 'player'
    form_fields = ['climate_exists', 'narrative_elicitation']

    @staticmethod
    def vars_for_template(player: Player):
        existing = MyPage.vars_for_template(player)
        existing.update(
            fields_labels=Lexicon.get_fields_labels(
                ['climate_exists', 'narrative_elicitation']
            )
        )
        return existing

    @staticmethod
    def error_message(player, values):
        text = values['narrative_elicitation'] or ""
        word_count = len(text.split())
        if not player.session.config.get("fill_auto", False):
            if word_count < 50:
                return f"Please write at least 50 words (you wrote {word_count})."
        return None

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.climate_exists = random.choice([True, False])
            player.narrative_elicitation = "Bot content " * 50


class NarrativeElicitation_question_certain(MyPage):
    form_model = 'player'
    form_fields = ['narrative_confidence']

    @staticmethod
    def vars_for_template(player: Player):
        existing = MyPage.vars_for_template(player)
        existing.update(
            fields_labels=Lexicon.get_fields_labels(['narrative_confidence']))
        return existing

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.narrative_confidence = random.randint(0, 100)


class NarrativeSharing(MyPage):
    form_model = 'player'
    form_fields = [
        'choice_1', 'choice_2', 'choice_3',
        'choice_4', 'choice_5', 'choice_6', 'choice_7'
    ]

    @staticmethod
    def vars_for_template(player: Player):
        existing = MyPage.vars_for_template(player)
        amounts = player.session.vars[app_name]["amounts"]
        existing.update(
            num_selected=player.session.vars[app_name]["num_selected"],
            amount_example=amounts[0],
            fields_amounts={f'choice_{i}': am for i, am in enumerate(amounts, start=1)},
        )
        return existing

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            for i in range(1, 8):
                setattr(player, f'choice_{i}', random.choice(['A', 'B']))
        player.set_payoff_mpl()


class circadian(MyPage):
    form_model = 'player'
    form_fields = ['circadian']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.circadian = "Morning"


class Policy(MyPage):
    form_model = 'player'
    form_fields = ['policy_fight', 'policy_narrative']

    @staticmethod
    def vars_for_template(player: Player):
        existing = MyPage.vars_for_template(player)
        existing.update(
            fields_labels=Lexicon.get_fields_labels(['policy_fight', 'policy_narrative'])
        )
        return existing

    @staticmethod
    def error_message(player, values):
        text = values['policy_narrative'] or ""
        word_count = len(text.split())
        if not player.session.config.get("fill_auto", False):
            if word_count < 25:
                return f"Please write at least 25 words (you wrote {word_count})."
        return None

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.policy_fight = random.choice([0, 1, -1])
            player.policy_narrative = "Bot content " * 25


class Policy_question_certain(MyPage):
    form_model = 'player'
    form_fields = ['confidence_policy']

    @staticmethod
    def vars_for_template(player: Player):
        existing = MyPage.vars_for_template(player)
        existing.update(fields_labels=Lexicon.get_fields_labels(['confidence_policy']))
        return existing

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.confidence_policy = random.randint(0, 100)


class Policy_expectations(MyPage):
    form_model = 'player'
    form_fields = ['expectations_policy_economy', 'expectations_policy_cc', 'expectations_policy_household',
                   'agreement_policy']

    @staticmethod
    def vars_for_template(player: Player):
        existing = MyPage.vars_for_template(player)
        existing.update(fields_labels=Lexicon.get_fields_labels(
            ['expectations_policy_economy', 'expectations_policy_cc', 'expectations_policy_household',
             'agreement_policy']
        ))
        return existing

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.expectations_policy_economy = random.randint(-2, 2)
            player.expectations_policy_cc = random.randint(-2, 2)
            player.expectations_policy_household = random.randint(-2, 2)
            player.agreement_policy = random.randint(-2, 2)


class ClimateKnowledge(MyPage):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player):
        fields = ["climate_knowledge"]
        ranks = ["rank_coal", "rank_gas", "rank_nuclear"]
        random.shuffle(ranks)
        fields += ranks
        return fields

    @staticmethod
    def vars_for_template(player: Player):
        existing = MyPage.vars_for_template(player)
        existing.update(fields_labels=Lexicon.get_fields_labels(
            ["climate_knowledge", "rank_coal", "rank_gas", "rank_nuclear"]))
        return existing

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.climate_knowledge = random.randint(0, 4)
            player.rank_coal = random.randint(1, 3)
            player.rank_gas = random.randint(1, 3)
            player.rank_nuclear = random.randint(1, 3)


class MediaConsumption(MyPage):
    form_model = 'player'
    form_fields = ['info_freq',
                   'use_tv', 'use_newspapers', 'use_radio', 'use_social', 'use_online', 'use_newsletters',
                   'climate_info_freq',
                   'use_tv_climate', 'use_newspapers_climate', 'use_radio_climate', 'use_social_climate',
                   'use_online_climate', 'use_newsletters_climate',
                   ]

    @staticmethod
    def vars_for_template(player: Player):
        existing = MyPage.vars_for_template(player)
        existing.update(
            fields_labels=Lexicon.get_fields_labels(
                ['info_freq', 'use_tv', 'use_newspapers', 'use_radio', 'use_social', 'use_online',
                 'use_newsletters',
                 'climate_info_freq',
                 'use_tv_climate', 'use_newspapers_climate', 'use_radio_climate', 'use_social_climate',
                 'use_online_climate', 'use_newsletters_climate']
            ),
            fields_radios=['use_tv', 'use_newspapers', 'use_radio', 'use_social', 'use_online', 'use_newsletters'],
            fields_radios_climate=['use_tv_climate', 'use_newspapers_climate', 'use_radio_climate',
                                   'use_social_climate', 'use_online_climate', 'use_newsletters_climate']
        )
        return existing

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.info_freq = str(random.randint(0, 5))
            player.climate_info_freq = str(random.randint(0, 5))
            for f in ['use_tv', 'use_newspapers', 'use_radio', 'use_social', 'use_online', 'use_newsletters']:
                setattr(player, f, random.randint(1, 7))
                setattr(player, f'{f}_climate', random.randint(1, 7))


class ClimateExpectations(MyPage):
    form_model = 'player'
    form_fields = [
        'climate_threat',
        'expectations_droughts', 'expectations_eruptions', 'expectations_sea', 'expectations_agriculture',
        'expectations_living', 'expectations_migration', 'expectations_conflicts', 'expectations_extinction'
    ]

    @staticmethod
    def vars_for_template(player: Player):
        existing = MyPage.vars_for_template(player)
        existing.update(
            fields_labels=Lexicon.get_fields_labels(
                [
                    'climate_threat',
                    'expectations_droughts', 'expectations_eruptions', 'expectations_sea', 'expectations_agriculture',
                    'expectations_living', 'expectations_migration', 'expectations_conflicts', 'expectations_extinction'
                ]
            ),
            fields_expectations=[
                'expectations_droughts', 'expectations_eruptions', 'expectations_sea', 'expectations_agriculture',
                'expectations_living', 'expectations_migration', 'expectations_conflicts', 'expectations_extinction']
        )

        return existing

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.climate_threat = random.randint(0, 3)
            for field in ['expectations_droughts', 'expectations_eruptions', 'expectations_sea',
                          'expectations_agriculture',
                          'expectations_living', 'expectations_migration', 'expectations_conflicts',
                          'expectations_extinction']:
                setattr(player, field, str(random.randint(-2, 2)))


class ClimateConcern(MyPage):
    form_model = 'player'
    form_fields = [
        'limit_flying', 'limit_driving', 'electric_vehicle', 'limit_beef', 'limit_heating'
    ]

    @staticmethod
    def vars_for_template(player: Player):
        existing = MyPage.vars_for_template(player)
        existing.update(
            fields_labels=Lexicon.get_fields_labels(
                [
                    'limit_flying', 'limit_driving', 'electric_vehicle', 'limit_beef', 'limit_heating'
                ]))
        return existing

    @staticmethod
    def is_displayed(player: Player):
        return player.skip == False

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            for field in ['limit_flying', 'limit_driving', 'electric_vehicle', 'limit_beef', 'limit_heating']:
                setattr(player, field, random.randint(-2, 2))


class Demographics(MyPage):
    form_model = 'player'
    form_fields = ['income', 'education']

    @staticmethod
    def vars_for_template(player: Player):
        existing = MyPage.vars_for_template(player)
        existing.update(
            fields_labels=Lexicon.get_fields_labels(['income', 'education']))
        return existing

    @staticmethod
    def is_displayed(player: Player):
        return player.skip == False

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.income = random.randint(0, 6)
            player.education = random.randint(0, 4)


class End(MyPage):
    @staticmethod
    def vars_for_template(player: Player):
        existing = MyPage.vars_for_template(player)
        return existing


page_sequence = [
    Presentation,
    NarrativeElicitation_text, NarrativeElicitation_question, NarrativeElicitation_question_certain, NarrativeSharing,
    Policy, Policy_question_certain, Policy_expectations,
    ClimateKnowledge, MediaConsumption,
    ClimateExpectations,
    ClimateConcern,
    Demographics,
    End
]
