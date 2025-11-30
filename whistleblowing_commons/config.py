from settings import LANGUAGE_CODE

language = {"en": False, "fr": False, LANGUAGE_CODE: True}
_ = lambda s: s[LANGUAGE_CODE]


class Config:
    PLAYERS_PER_GROUP = 3

    ENDOWMENT = 75

    # --- TREATMENTS ---
    INDIVIDUAL = "individual"
    COOPERATION = "cooperation"

    # --- PART 1 - EFFORT TASK PARAMETERS ---
    EFFORT_DURATION = 120  # seconds
    PIECE_RATE = 10

    # counting task parameters
    GRID_SIZE = (10, 10)
    NUM_GRIDS = 100

    # addition task parameters
    OPERATION_SIZE = 3
    NUM_OPERATIONS = 100

    # slider task parameters
    NUM_SLIDERS = 100

    # --- PART 2 - WHISTLEBLOWING GAME PARAMETERS ---
    STEALING_AMOUNT = 30
    STEALING_LOSS = 45
    STEALING_LOSS_INDIV = int(STEALING_LOSS / PLAYERS_PER_GROUP)
    STEALING_PENALTY = 45
    REPORTING_COST = 10
    REPORTING_REWARD = 45
    AUDIT_PROBABILITY = 2 / 3
    AUDIT_PROBABILITY_STR = "2/3"
    NON_AUDIT_PROBABILITY_STR = "1/3"
    DECISION_TIME = 90  # 1'30
    SOCIETY_OPTION_PAYOFF = 10


    @staticmethod
    def get_parameters():
        return {k: v for k, v in Config.__dict__.items() if not k.startswith("__") and not callable(v)}
