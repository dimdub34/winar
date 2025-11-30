from otree.api import *
from pathlib import Path
import random
from whistleblowing_commons.config import language, _

doc = """
Questionnaires
"""
app_name = Path(__file__).parent.name


class C(BaseConstants):
    NAME_IN_URL = "whquest"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass




class Player(BasePlayer):
    @staticmethod
    def relevant_likert():
        return [
            (0, _(dict(
                en="not at all relevant (this consideration has nothing to do with my judgments of right or wrong)",
                fr="pas du tout pertinent (cette considération n'a rien à voir avec mes jugements de bien ou de mal)",
            ))),
            (1, _(dict(en="not very relevant", fr="pas très pertinent"))),
            (2, _(dict(en="slightly relevant", fr="légèrement pertinent"))),
            (3, _(dict(en="somewhat relevant", fr="assez pertinent"))),
            (4, _(dict(en="very relevant", fr="très pertinent"))),
            (5, _(dict(en="extremely relevant", fr="extrêmement pertinent"))),
        ]

    @staticmethod
    def agreement_likert():
        return [
            (0, _(dict(en="Strongly disagree", fr="Fortement en désaccord"))),
            (1, _(dict(en="Moderately disagree", fr="Modérément en désaccord"))),
            (2, _(dict(en="Slightly disagree", fr="Légèrement en désaccord"))),
            (3, _(dict(en="Slightly agree", fr="Légèrement d'accord"))),
            (4, _(dict(en="Moderately agree", fr="Modérément d'accord"))),
            (5, _(dict(en="Strongly agree", fr="Fortement d'accord"))),
        ]


    # ----- questionnaire 1 -----
    fairness_1 = models.IntegerField(
        label=_(dict(
            en="... whether or not someone acted unfairly",
            fr="... si oui ou non quelqu'un a agi de manière injuste",
        )),
        choices=relevant_likert(), widget=widgets.RadioSelect())
    fairness_2 = models.IntegerField(
        label=_(dict(
            en="... whether or not someone was denied his or her rights",
            fr="... si oui ou non quelqu'un a renié à ses droits",
        )), choices=relevant_likert(), widget=widgets.RadioSelect())
    fairness_3 = models.IntegerField(
        label=_(dict(
            en="Justice is the most important requirement for a society",
            fr="La justice est primordiale pour une société",
        )), choices=agreement_likert(), widget=widgets.RadioSelect())
    loyalty_1 = models.IntegerField(
        label=_(dict(
            en="... whether or not someone did something to betray his or her group",
            fr="... si oui ou non quelqu'un a fait quelque chose pour trahir son groupe",
        )), choices=relevant_likert(), widget=widgets.RadioSelect())
    loyalty_2 = models.IntegerField(
        label=_(dict(
            en="... whether or not someone showed a lack of loyalty",
            fr="... si oui ou non quelqu'un a fait preuve d'un manque de loyauté",
        )), choices=relevant_likert(), widget=widgets.RadioSelect())
    loyalty_3 = models.IntegerField(
        label=_(dict(
            en="People should be loyal to their family members, even when they have done something wrong",
            fr="Les gens doivent être loyaux avec les membres de leur famille, même lorsqu'ils ont fait quelque "
               "chose de mal",
        )), choices=agreement_likert(), widget=widgets.RadioSelect())
    morally_good_person = models.IntegerField(
        label=_(dict(
            en="Objectively speaking, who do you think is the more morally good person?",
            fr="Objectivement parlant, qui est la personne la plus morale selon toi ?",
        )),
        choices=[
            (1, _(dict(
                en="Someone who is fair and just, impartial and unprejudiced",
                fr="Quelqu'un qui est juste et équitable, impartial et sans préjugés",
            ))),
            (0, _(dict(
                en="Someone who is loyal and faithful, devoted and dependable",
                fr="Quelqu'un qui est loyal et fidèle, dévoué et fiable",
            ))),
        ], widget=widgets.RadioSelect())
    friend_choice = models.IntegerField(
        label=_(dict(
            en="Who would you rather be friends with?",
            fr="Avec qui préféreriez-vous être ami(e) ?",
        )),
        choices=[
            (1, _(dict(
                en="Someone who is fair and just to others, who is impartial and unprejudiced regardless of "
                   "how it affects their family and friends",
                fr="Quelqu'un qui est juste et équitable envers les autres, impartial et sans préjugés, même "
                   "si cela affecte sa famille et ses amis",
            ))),
            (0, _(dict(
                en="Someone who is loyal and faithful to their family and friends, who is devoted and "
                   "dependable regardless of how it affects outsiders",
                fr="Quelqu'un qui est loyal et fidèle à sa famille et à ses amis, dévoué et fiable même si "
                   "cela affecte des personnes extérieures",
            )))], widget=widgets.RadioSelect())
    # ----- questionnaire 2 -----
    share_friend_stranger = models.IntegerField(
        label=_(dict(
            en=f"How much of your {cu(1000)} would you give to your friend, if the rest goes to a "
               "random stranger from your country?",
            fr=f"Sur vos {cu(1000)}, combien donneriez-vous à votre ami(e), si le reste allait à un(e) "
               f"inconnu(e) pris(e) au hasard dans votre pays ?",
        )), min=0, max=1000)
    # corruption = models.IntegerField(
    #     label=_(dict(
    #         en="In your opinion, how widespread is corruption in your country?",
    #         fr="À votre avis, quelle est l'étendue de la corruption dans votre pays ?",
    #     )),
    #     choices=[
    #         (0, _(dict(en="Not at all widespread", fr="Pas du tout répandue"))),
    #         (1, _(dict(en="Somewhat widespread", fr="Assez répandue"))),
    #         (2, _(dict(en="Very widespread", fr="Très répandue"))),
    #         (3, _(dict(en="Extremely widespread", fr="Extrêmement répandue"))),
    #     ], widget=widgets.RadioSelect())

    # ----- demographics -----
    age = models.IntegerField(
        label=_(dict(en="What is your age?", fr="Quel est votre âge ?")),
        choices=range(16, 121))
    gender = models.StringField(
        label=_(dict(en="What is your gender?", fr="Quel est votre genre ?")),
        choices=[
            ("F", _(dict(en="Female", fr="Femme"))),
            ("M", _(dict(en="Male", fr="Male"))),
            ("NB", _(dict(en="Non-binary", fr="Non binaire"))),
            ("NSP", _(dict(en="Prefer no to say", fr="Ne souhaite pas répondre"))),
        ], widget=widgets.RadioSelect())
    highest_diploma = models.IntegerField(
        label=_(dict(
            en="What is the highest level of education you have completed?",
            fr="Quel est le niveau d'études le plus élevé que vous ayez terminé ?",
        )),
        choices=[
            (0, _(dict(en="No formal education", fr="Aucune éducation formelle"))),
            (1, _(dict(en="Primary education", fr="Enseignement primaire"))),
            (2, _(dict(en="Secondary education", fr="Enseignement secondaire"))),
            (3, _(dict(en="Bachelor’s degree", fr="Licence"))),
            (4, _(dict(en="Master’s degree", fr="Master"))),
            (5, _(dict(en="Doctorate or higher", fr="Doctorat ou supérieur"))),
        ], widget=widgets.RadioSelect())
    # interest_politics = models.IntegerField(
    #     label=_(dict(
    #         en="To what extent are you interested in politics?",
    #         fr="Dans quelle mesure vous intéressez-vous à la politique ?"
    #     )),
    #     choices=[
    #         [0, _(dict(en="Not at all", fr="Pas du tout"))],
    #         [1, _(dict(en="A little", fr="Un peu"))],
    #         [2, _(dict(en="Moderately", fr="Modérément"))],
    #         [3, _(dict(en="A lot", fr="Beaucoup"))],
    #         [4, _(dict(en="A great deal", fr="Énormément"))]
    #     ], widget=widgets.RadioSelectHorizontal)
    # member_env_org = models.BooleanField(
    #     label=_(dict(
    #         en="Are you a member of an environmental organization?",
    #         fr="Êtes-vous membre d'une organisation environnementale ?"
    #     )),
    #     choices=[
    #         [True, _(dict(en="Yes", fr="Oui"))],
    #         [False, _(dict(en="No", fr="Non"))]
    #     ], widget=widgets.RadioSelectHorizontal)
    #
    # political_orientation = models.IntegerField(
    #     label=_(dict(
    #         en="On economic and social issues, where would you place yourself?",
    #         fr="Sur les questions économiques et sociales, où vous situeriez-vous ?"
    #     )),
    #     choices=[
    #         [1, _(dict(en="Clearly Left", fr="Clairement à gauche"))],
    #         [2, _(dict(en="Somewhat Left", fr="Plutôt à gauche"))],
    #         [3, _(dict(en="Center / Moderate", fr="Centre / Modéré"))],
    #         [4, _(dict(en="Somewhat Right", fr="Plutôt à droite"))],
    #         [5, _(dict(en="Clearly Right", fr="Clairement à droite"))],
    #         [0, _(dict(en="Prefer not to say", fr="Préfère ne pas répondre"))]
    #     ], widget=widgets.RadioSelectHorizontal)


# ======================================================================================================================
#
# -- PAGES --
#
# ======================================================================================================================


class MyPage(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(**language)

    @staticmethod
    def js_vars(player: Player):
        return dict(fill_auto=player.session.config.get("fill_auto", False))


class Questionnaire1(MyPage):
    form_model = "player"
    form_fields = ["fairness_1", "fairness_2", "loyalty_1", "loyalty_2", "fairness_3", "loyalty_3",
                   "morally_good_person", "friend_choice"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.participant._is_bot = True
            fields = [field for field in Questionnaire1.form_fields
                      if "fairness" in field or "loyalty" in field]
            for field in fields:
                setattr(player, field, random.randint(0, 5))
            player.morally_good_person = random.randint(0, 1)
            player.friend_choice = random.randint(0, 1)


class Questionnaire2(MyPage):
    form_model = "player"
    form_fields = ["share_friend_stranger"]

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.participant._is_bot = True
            player.share_friend_stranger = random.randint(0, 1000)


class Demographics(MyPage):
    form_model = "player"
    form_fields = ["gender", "age", "highest_diploma"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.participant._is_bot = True
            player.gender = random.choice(["M", "F", "NB", "NSP"])
            player.age = random.randint(16, 120)
            player.highest_diploma = random.randint(0, 5)


page_sequence = [Questionnaire1, Questionnaire2, Demographics]
