import random

from otree.api import *
from settings import LANGUAGE_CODE

doc = """
Climate questionnaire
"""

language = {"en": False, "fr": False, LANGUAGE_CODE: True}
_ = lambda x: x[LANGUAGE_CODE]


def get_scale_action():
    return [
        [-2, _(dict(en="Not at all", fr="Pas du tout"))],
        [-1, _(dict(en="-1", fr="-1"))],
        [0, _(dict(en="Moderately", fr="Modérément"))],
        [1, _(dict(en="1", fr="1"))],
        [2, _(dict(en="A great deal", fr="Énormément"))]
    ]


def get_scale_policy():
    return [
        [-2, _(dict(en="Strongly oppose", fr="Fortement opposé(e)"))],
        [-1, _(dict(en="Somewhat oppose", fr="Plutôt opposé(e)"))],
        [0, _(dict(en="Neither support nor oppose", fr="Ni favorable ni opposé(e)"))],
        [1, _(dict(en="Somewhat support", fr="Plutôt favorable"))],
        [2, _(dict(en="Strongly support", fr="Fortement favorable"))]
    ]


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
        label=_(dict(
            en=(
                "Please explain your reasoning in full sentences, describing the contributing factors and their possible "
                "links."),
            fr=("Veuillez s'il vous plaît expliquer votre raisonnement avec des phrases entières, en décrivant les "
                "facteurs qui contribuent au changement climatique, et les potentiels liens entre eux.")
        ))
    )
    # Climate knowledge ---------------
    climate_knowledge = models.IntegerField(
        label=_(
            dict(
                en="How knowledgeable do you consider yourself about climate change?",
                fr="À quel point vous considérez-vous informé(e) sur le changement climatique ?",
            )
        ),
        choices=[
            [0, _(dict(en="Not at all", fr="Pas du tout"))],
            [1, _(dict(en="A little", fr="Un peu"))],
            [2, _(dict(en="Moderately", fr="Modérément"))],
            [3, _(dict(en="A lot", fr="Beaucoup"))],
            [4, _(dict(en="A great deal", fr="Énormément"))]
        ],
        widget=widgets.RadioSelectHorizontal,
    )
    rank_coal = models.IntegerField(
        label=_(dict(
            en="Rank of Coal-fired power station",
            fr="Classement de la centrale à charbon"
        )),
        choices=[1, 2, 3],
        widget=widgets.RadioSelectHorizontal
    )
    rank_gas = models.IntegerField(
        label=_(dict(
            en="Rank of Gas-fired power plant",
            fr="Classement de la centrale à gaz"
        )),
        choices=[1, 2, 3],
        widget=widgets.RadioSelectHorizontal
    )
    rank_nuclear = models.IntegerField(
        label=_(dict(
            en="Rank of Nuclear power plant",
            fr="Classement de la centrale nucléaire"
        )),
        choices=[1, 2, 3],
        widget=widgets.RadioSelectHorizontal
    )
    # Media ---------------------------
    climate_info_freq = models.StringField(
        choices=[
            [3, _(dict(en="Daily", fr="Quotidiennement"))],
            [2, _(dict(en="Several times", fr="Plusieurs fois"))],
            [1, _(dict(en="Once", fr="Une fois"))],
            [0, _(dict(en="Never", fr="Jamais"))]
        ],
        label=_(
            dict(
                en="How often did you acquire information about climate change over the past week?",
                fr="À quelle fréquence avez-vous obtenu des informations sur le changement climatique au cours "
                   "de la semaine dernière ?"
            )
        ),
        widget=widgets.RadioSelect
    )
    use_tv = models.IntegerField(
        label=_(
            dict(
                en="Television (e.g., national news, cable news)",
                fr="Télévision (par exemple, actualités nationales, chaînes d'information)"
            )
        ),
        choices=range(1, 8),
        widget=widgets.RadioSelectHorizontal
    )
    use_newspapers = models.IntegerField(
        label=_(
            dict(
                en="Printed Newspapers",
                fr="Journaux imprimés"
            )
        ),
        choices=range(1, 8),
        widget=widgets.RadioSelectHorizontal
    )
    use_radio = models.IntegerField(
        label=_(
            dict(
                en="Radio",
                fr="Radio"
            )
        ),
        choices=range(1, 8),
        widget=widgets.RadioSelectHorizontal
    )
    use_social = models.IntegerField(
        label=_(
            dict(
                en="Social media platforms",
                fr="Plateformes de médias sociaux"
            )
        ),
        choices=range(1, 8),
        widget=widgets.RadioSelectHorizontal
    )
    use_online = models.IntegerField(
        label=_(
            dict(
                en="Online news",
                fr="Actualités en ligne"
            )
        ),
        choices=range(1, 8),
        widget=widgets.RadioSelectHorizontal
    )
    use_newsletters = models.IntegerField(
        label=_(
            dict(
                en="Newsletters or email subscriptions",
                fr="Newsletters ou abonnements par e-mail"
            )
        ),
        choices=range(1, 8),
        widget=widgets.RadioSelectHorizontal
    )
    use_left_sources = models.BooleanField(
        label=_(
            dict(
                en="Left-leaning sources?",
                fr="Sources orientées à gauche ?"
            )
        ),
        widget=widgets.CheckboxInput, blank=True
    )
    use_right_sources = models.BooleanField(
        label=_(
            dict(
                en="Rright-leaning sources?",
                fr="Sources orientées à droite ?"
            )
        ),
        widget=widgets.CheckboxInput, blank=True
    )
    use_neutral_sources = models.BooleanField(
        label=_(
            dict(
                en="Neutral/centrist sources?",
                fr="Sources neutres/centristes ?"
            )
        ),
        widget=widgets.CheckboxInput, blank=True
    )
    unknown_sources_orientation = models.BooleanField(
        label=_(
            dict(
                en="I don’t know the political orientation of my news sources",
                fr="Je ne connais pas l'orientation politique de mes sources d'information"
            )
        ),
        widget=widgets.CheckboxInput, blank=True
    )
    news_preference = models.IntegerField(
        label=_(
            dict(
                en="If given the choice, would you prefer to read news that...",
                fr="Si vous aviez le choix, préféreriez-vous lire des actualités qui..."
            )
        ),
        choices=[
            [1, _(dict(en="Confirm your beliefs", fr="Confirment vos croyances"))],
            [2, _(dict(en="Challenge your beliefs", fr="Remettent en question vos croyances"))],
            [3,
             _(dict(en="Provide neutral and factual information",
                    fr="Fournissent des informations neutres et factuelles"))]
        ],
        widget=widgets.RadioSelect
    )
    subscribe_newsletter = models.BooleanField(
        choices=[
            [True, _(dict(en="Yes", fr="Oui"))],
            [False, _(dict(en="No", fr="Non"))]
        ],
        label=_(
            dict(
                en="Would you be willing to subscribe to a newsletter that covers top stories on climate policy "
                   "from sources across the political spectrum?",
                fr="Seriez-vous prêt(e) à vous abonner à une newsletter couvrant les principales actualités sur "
                   "les politiques climatiques provenant de sources de tout le spectre politique ?"
            )
        ),
        widget=widgets.RadioSelectHorizontal
    )
    willingness_to_pay = models.IntegerField(
        label=_(
            dict(
                en="How much would you be willing to pay for exclusive, reliable climate news? (one-time payment)",
                fr="Combien seriez-vous prêt(e) à payer pour des actualités climatiques exclusives et fiables ? "
                   "(paiement unique)"
            )
        ),
        choices=[
            [0, _(dict(en=f"{cu(0)}", fr=f"{cu(0)}"))],
            [1, _(dict(en=f"{cu(0.5)}", fr=f"{cu(0.5)}"))],
            [2, _(dict(en=f"{cu(1)}", fr=f"{cu(1)}"))],
            [3, _(dict(en=f"{cu(2)}", fr=f"{cu(2)}"))],
            [4, _(dict(en=f"More than {cu(2)}", fr=f"Plus de {cu(2)}"))]
        ],
        widget=widgets.RadioSelectHorizontal
    )
    # Concern -------------------------
    climate_threat = models.IntegerField(
        choices=[
            [3, _(dict(en="Very serious threat", fr="Une menace très sérieuse"))],
            [2, _(dict(en="Somewhat serious threat", fr="Une menace assez sérieuse"))],
            [1, _(dict(en="Not a threat at all", fr="Pas une menace du tout"))],
            [0, _(dict(en="Don’t know", fr="Ne sais pas"))]
        ],
        label=_(
            dict(
                en="Do you think climate change will be a threat to people in your country in the next 20 years?",
                fr="Pensez-vous que le changement climatique sera une menace pour les gens de votre pays dans les "
                   "20 prochaines années ?"
            )
        ),
        widget=widgets.RadioSelectHorizontal
    )
    # Willingness to act --------------
    limit_flying = models.IntegerField(
        label=_(
            dict(
                en="Limit flying",
                fr="Limiter les vols"
            )
        ),
        choices=get_scale_action(),
        widget=widgets.RadioSelectHorizontal
    )
    limit_driving = models.IntegerField(
        label=_(
            dict(
                en="Limit driving",
                fr="Limiter la conduite"
            )
        ),
        choices=get_scale_action(),
        widget=widgets.RadioSelectHorizontal
    )
    electric_vehicle = models.IntegerField(
        label=_(
            dict(
                en="Have an electric vehicle",
                fr="Posséder un véhicule électrique"
            )
        ),
        choices=get_scale_action(),
        widget=widgets.RadioSelectHorizontal
    )
    limit_beef = models.IntegerField(
        label=_(
            dict(
                en="Limit beef consumption",
                fr="Limiter la consommation de bœuf"
            )
        ),
        choices=get_scale_action(),
        widget=widgets.RadioSelectHorizontal
    )
    limit_heating = models.IntegerField(
        label=_(
            dict(
                en="Limit heating or cooling your home",
                fr="Limiter le chauffage ou la climatisation de votre maison"
            )
        ),
        choices=get_scale_action(),
        widget=widgets.RadioSelectHorizontal
    )
    # Policy support ------------------
    tax_flying = models.StringField(
        label=_(
            dict(
                en="A tax on flying (that increases ticket prices by 20%)",
                fr="Une taxe sur les vols (qui augmente les prix des billets de 20%)"
            )
        ),
        choices=get_scale_policy(),
        widget=widgets.RadioSelectHorizontal
    )
    tax_fossil = models.StringField(
        label=_(
            dict(
                en="A national tax on fossil fuels (increasing gasoline prices by 40 cents per gallon)",
                fr="Une taxe nationale sur les combustibles fossiles (augmentant les prix de l'essence de 40 centimes par gallon)"
            )
        ),
        choices=get_scale_policy(),
        widget=widgets.RadioSelectHorizontal
    )
    ban_polluting = models.StringField(
        label=_(
            dict(
                en="A ban of polluting vehicles in dense areas, like city centers",
                fr="Une interdiction des véhicules polluants dans les zones denses, comme les centres-villes"
            )
        ),
        choices=get_scale_policy(),
        widget=widgets.RadioSelectHorizontal
    )
    subsidy_lowcarbon = models.StringField(
        label=_(
            dict(
                en="Subsidies for low-carbon technologies (renewable energy, carbon capture...)",
                fr="Des subventions pour les technologies à faible émission de carbone (énergies renouvelables, capture de carbone...)"
            )
        ),
        choices=get_scale_policy(),
        widget=widgets.RadioSelectHorizontal
    )
    climate_fund = models.StringField(
        label=_(
            dict(
                en="A contribution to a global climate fund to finance clean energy in low-income countries",
                fr="Une contribution à un fonds climatique mondial pour financer l'énergie propre dans les pays à faible revenu"
            )
        ),
        choices=get_scale_policy(),
        widget=widgets.RadioSelectHorizontal
    )

# ======================================================================================================================
#
# -- PAGES
#
# ======================================================================================================================

class MyPage(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            **language
        )

    @staticmethod
    def js_vars(player: Player):
        return dict(
            fill_auto=player.session.config.get("fill_auto", False),
            **language
        )


class Presentation(MyPage):
    form_model = 'player'
    form_fields = ["skip"]


class NarrativeElicitation(MyPage):
    form_model = 'player'
    form_fields = ['narrative_elicitation']

    @staticmethod
    def is_displayed(player: Player):
        return player.skip == False

class ClimateKnowledge(MyPage):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player):
        fields = ["climate_knowledge"]
        ranks = ["rank_coal", "rank_gas", "rank_nuclear"]
        random.shuffle(ranks)
        fields += ranks
        return fields

    # def error_message(self, values):
    #     ranks = [values['rank_coal'], values['rank_gas'], values['rank_nuclear']]
    #     if sorted(ranks) != [1, 2, 3]:
    #         return _(dict(
    #             en="Please assign a unique rank (1, 2, and 3) to each energy source.",
    #             fr="Veuillez assigner un classement unique (1, 2 ou 3) à chaque source d'énergie."
    #         ))
    #     return None

    @staticmethod
    def is_displayed(player: Player):
        return player.skip == False


class MediaConsumption(MyPage):
    form_model = 'player'
    form_fields = [
        'climate_info_freq',
        'use_tv', 'use_newspapers', 'use_radio', 'use_social', 'use_online', 'use_newsletters',
        'use_left_sources', "use_right_sources", "use_neutral_sources", "unknown_sources_orientation",
        'news_preference', 'subscribe_newsletter', 'willingness_to_pay'
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.skip == False


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


    @staticmethod
    def is_displayed(player: Player):
        return player.skip == False

page_sequence = [Presentation, NarrativeElicitation, ClimateKnowledge, MediaConsumption, ClimateConcern]
