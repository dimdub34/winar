import random
from pathlib import Path

from otree.api import *

doc = """
Questionnaires
"""
app_name = Path(__file__).parent.name


def relevant_likert():
    return [
        (0, "not at all relevant (this consideration has nothing to do with my judgments of right or wrong)"),
        (1, "not very relevant"),
        (2, "slightly relevant"),
        (3, "somewhat relevant"),
        (4, "very relevant"),
        (5, "extremely relevant"),
    ]


def agreement_likert():
    return [
        (0, "Strongly disagree"),
        (1, "Moderately disagree"),
        (2, "Slightly disagree"),
        (3, "Slightly agree"),
        (4, "Moderately agree"),
        (5, "Strongly agree"),
    ]


class C(BaseConstants):
    NAME_IN_URL = "whquest"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # ----- questionnaire 1 -----
    fairness_1 = models.IntegerField(
        label="... whether or not someone acted unfairly",
        choices=relevant_likert(), widget=widgets.RadioSelect())
    fairness_2 = models.IntegerField(
        label="... whether or not someone was denied his or her rights", choices=relevant_likert(),
        widget=widgets.RadioSelect())
    fairness_3 = models.IntegerField(
        label="Justice is the most important requirement for a society", choices=agreement_likert(),
        widget=widgets.RadioSelect())
    loyalty_1 = models.IntegerField(
        label="... whether or not someone did something to betray his or her group", choices=relevant_likert(),
        widget=widgets.RadioSelect())
    loyalty_2 = models.IntegerField(
        label="... whether or not someone showed a lack of loyalty", choices=relevant_likert(),
        widget=widgets.RadioSelect())
    loyalty_3 = models.IntegerField(
        label="People should be loyal to their family members, even when they have done something wrong",
        choices=agreement_likert(), widget=widgets.RadioSelect())
    morally_good_person = models.IntegerField(
        label="Objectively speaking, who do you think is the more morally good person?",
        choices=[
            (1, "Someone who is fair and just, impartial and unprejudiced"),
            (0, "Someone who is loyal and faithful, devoted and dependable"),
        ], widget=widgets.RadioSelect())
    friend_choice = models.IntegerField(
        label="Who would you rather be friends with?",
        choices=[
            (1, "Someone who is fair and just to others, who is impartial and unprejudiced regardless of "
                "how it affects their family and friends"),
            (0, "Someone who is loyal and faithful to their family and friends, who is devoted and "
                "dependable regardless of how it affects outsiders"),
        ], widget=widgets.RadioSelect())
    # ----- questionnaire 2 -----
    share_friend_stranger = models.IntegerField(
        label=f"How much of your {cu(1000)} would you give to your friend, if the rest goes to a "
              "random stranger from your country?",
        min=0,
        max=1000,
    )

    # ----- demographics -----
    age = models.IntegerField(
        label="What is your age?",
        choices=range(16, 121))
    gender = models.StringField(
        label="What is your gender?",
        choices=[
            ("F", "Female"),
            ("M", "Male"),
            ("NB", "Non-binary"),
            ("NSP", "Prefer not to say"),
        ], widget=widgets.RadioSelect())
    highest_diploma = models.IntegerField(
        label="What is the highest level of education you have completed?",
        choices=[
            (0, "No formal education"),
            (1, "Primary education"),
            (2, "Secondary education"),
            (3, "Bachelor's degree"),
            (4, "Master's degree"),
            (5, "Doctorate or higher"),
        ], widget=widgets.RadioSelect())


# ======================================================================================================================
#
# -- PAGES --
#
# ======================================================================================================================


class MyPage(Page):

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
