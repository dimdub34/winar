import random

from otree.api import *

doc = """
Climate questionnaire
"""


def get_scale_action():
    return [[-2, "Not at all"], [-1, "-1"], [0, "Moderately"], [1, "1"], [2, "A great deal"]]


def get_scale_policy():
    return [[-2, "Strongly oppose"], [-1, "Somewhat oppose"], [0, "Neither support nor oppose"],
            [1, "Somewhat support"], [2, "Strongly support"]]


class C(BaseConstants):
    NAME_IN_URL = 'clquest'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    skip = models.BooleanField()

    # Narrative elicitation -----------
    narrative_elicitation = models.LongStringField(
        label=(
            "Please explain your reasoning in full sentences, describing the contributing factors and their possible "
            "links.")
    )
    # Climate knowledge ---------------
    climate_knowledge = models.IntegerField(
        label="How knowledgeable do you consider yourself about climate change?",
        choices=[
            [0, "Not at all"], [1, "A little"], [2, "Moderately"], [3, "A lot"], [4, "A great deal"]],
        widget=widgets.RadioSelectHorizontal,
    )
    rank_coal = models.IntegerField(
        label="Rank of Coal-fired power station", choices=[1, 2, 3], widget=widgets.RadioSelectHorizontal)
    rank_gas = models.IntegerField(
        label="Rank of Gas-fired power plant", choices=[1, 2, 3], widget=widgets.RadioSelectHorizontal)
    rank_nuclear = models.IntegerField(
        label="Rank of Nuclear power plant", choices=[1, 2, 3], widget=widgets.RadioSelectHorizontal)
    # Media ---------------------------
    climate_info_freq = models.StringField(
        choices=[[3, "Daily"], [2, "Several times"], [1, "Once"], [0, "Never"]],
        label="How often did you acquire information about climate change over the past week?",
        widget=widgets.RadioSelect
    )
    use_tv = models.IntegerField(
        label="Television (e.g., national news, cable news)", choices=range(1, 8), widget=widgets.RadioSelectHorizontal)
    use_newspapers = models.IntegerField(
        label="Printed Newspapers", choices=range(1, 8), widget=widgets.RadioSelectHorizontal)
    use_radio = models.IntegerField(
        label="Radio", choices=range(1, 8), widget=widgets.RadioSelectHorizontal)
    use_social = models.IntegerField(
        label="Social media platforms", choices=range(1, 8), widget=widgets.RadioSelectHorizontal)
    use_online = models.IntegerField(
        label="Online news", choices=range(1, 8), widget=widgets.RadioSelectHorizontal)
    use_newsletters = models.IntegerField(
        label="Newsletters or email subscriptions", choices=range(1, 8), widget=widgets.RadioSelectHorizontal)
    use_left_sources = models.BooleanField(
        label="Left-leaning sources?", widget=widgets.CheckboxInput, blank=True)
    use_right_sources = models.BooleanField(
        label="Right-leaning sources?", widget=widgets.CheckboxInput, blank=True)
    use_neutral_sources = models.BooleanField(
        label="Neutral/centrist sources?", widget=widgets.CheckboxInput, blank=True)
    unknown_sources_orientation = models.BooleanField(
        label="I don’t know the political orientation of my news sources", widget=widgets.CheckboxInput, blank=True)
    news_preference = models.IntegerField(
        label="If given the choice, would you prefer to read news that...",
        choices=[
            [1, "Confirm your beliefs"],
            [2, "Challenge your beliefs"],
            [3, "Provide neutral and factual information"]
        ], widget=widgets.RadioSelect)
    subscribe_newsletter = models.BooleanField(
        choices=[[True, "Yes"], [False, "No"]],
        label=("Would you be willing to subscribe to a newsletter that covers top stories on climate policy "
               "from sources across the political spectrum?"), widget=widgets.RadioSelectHorizontal)
    willingness_to_pay = models.IntegerField(
        label="How much would you be willing to pay for exclusive, reliable climate news? (one-time payment)",
        choices=[[0, f"{cu(0)}"], [1, f"{cu(0.5)}"], [2, f"{cu(1)}"], [3, f"{cu(2)}"], [4, f"More than {cu(2)}"]],
        widget=widgets.RadioSelectHorizontal
    )
    # Concern -------------------------
    climate_threat = models.IntegerField(
        choices=[
            [3, "Very serious threat"],
            [2, "Somewhat serious threat"],
            [1, "Not a threat at all"],
            [0, "Don’t know"]
        ],
        label="Do you think climate change will be a threat to people in your country in the next 20 years?",
        widget=widgets.RadioSelectHorizontal)
    # Willingness to act --------------
    limit_flying = models.IntegerField(
        label="Limit flying", choices=get_scale_action(), widget=widgets.RadioSelectHorizontal)
    limit_driving = models.IntegerField(
        label="Limit driving", choices=get_scale_action(), widget=widgets.RadioSelectHorizontal)
    electric_vehicle = models.IntegerField(
        label="Have an electric vehicle", choices=get_scale_action(), widget=widgets.RadioSelectHorizontal)
    limit_beef = models.IntegerField(
        label="Limit beef consumption", choices=get_scale_action(), widget=widgets.RadioSelectHorizontal)
    limit_heating = models.IntegerField(
        label="Limit heating or cooling your home", choices=get_scale_action(), widget=widgets.RadioSelectHorizontal)
    # Policy support ------------------
    tax_flying = models.StringField(
        label="A tax on flying (that increases ticket prices by 20%)", choices=get_scale_policy(),
        widget=widgets.RadioSelectHorizontal)
    tax_fossil = models.StringField(
        label="A national tax on fossil fuels (increasing gasoline prices by 40 cents per gallon)",
        choices=get_scale_policy(), widget=widgets.RadioSelectHorizontal)
    ban_polluting = models.StringField(
        label="A ban of polluting vehicles in dense areas, like city centers", choices=get_scale_policy(),
        widget=widgets.RadioSelectHorizontal)
    subsidy_lowcarbon = models.StringField(
        label="Subsidies for low-carbon technologies (renewable energy, carbon capture...)",
        choices=get_scale_policy(), widget=widgets.RadioSelectHorizontal)
    climate_fund = models.StringField(
        label="A contribution to a global climate fund to finance clean energy in low-income countries",
        choices=get_scale_policy(), widget=widgets.RadioSelectHorizontal)


# ======================================================================================================================
#
# -- PAGES
#
# ======================================================================================================================

class MyPage(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict()

    @staticmethod
    def js_vars(player: Player):
        return dict(
            fill_auto=player.session.config.get("fill_auto", False),
        )


class Presentation(MyPage):
    form_model = 'player'
    form_fields = ["skip"]

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.skip:
            return upcoming_apps[-1]


class NarrativeElicitation(MyPage):
    form_model = 'player'
    form_fields = ['narrative_elicitation']


class ClimateKnowledge(MyPage):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player):
        fields = ["climate_knowledge"]
        ranks = ["rank_coal", "rank_gas", "rank_nuclear"]
        random.shuffle(ranks)
        fields += ranks
        return fields

    def error_message(self, values):
        ranks = [values['rank_coal'], values['rank_gas'], values['rank_nuclear']]
        if sorted(ranks) != [1, 2, 3]:
            return _(dict(
                en="Please assign a unique rank (1, 2, and 3) to each energy source.",
                fr="Veuillez assigner un classement unique (1, 2 ou 3) à chaque source d'énergie."
            ))
        return None


class MediaConsumption(MyPage):
    form_model = 'player'
    form_fields = [
        'climate_info_freq',
        'use_tv', 'use_newspapers', 'use_radio', 'use_social', 'use_online', 'use_newsletters',
        'use_left_sources', "use_right_sources", "use_neutral_sources", "unknown_sources_orientation",
        'news_preference', 'subscribe_newsletter', 'willingness_to_pay'
    ]


class ClimateConcern(MyPage):
    form_model = 'player'
    form_fields = [
        'climate_threat', 'limit_flying', 'limit_driving', 'electric_vehicle', 'limit_beef', 'limit_heating',
        'tax_flying', 'tax_fossil', 'ban_polluting', 'subsidy_lowcarbon', 'climate_fund'
    ]

    @staticmethod
    def vars_for_template(player: Player):
        existing = MyPage.vars_for_template(player)
        existing["scale_policy"] = [s[1] for s in get_scale_policy()]
        return existing


page_sequence = [Presentation, NarrativeElicitation, ClimateKnowledge, MediaConsumption, ClimateConcern]
