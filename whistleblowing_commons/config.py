from .functions import seconds_to_minutes


class Config:
    PLAYERS_PER_GROUP = 3
    ENDOWMENT = 75

    # Effort tasks -----------------------------------------------------------------------------------------------------
    # Counting
    GRID_SIZE = (10, 10)
    NUM_GRIDS = 100

    # Maths
    OPERATION_SIZE = 3  # number of additions
    NUM_OPERATIONS = 100

    # Sliders
    NUM_SLIDERS = 100

    TASKS_NUM_ROUNDS = 1
    EFFORT_DURATION = 120  # seconds
    EFFORT_DURATION_STR = seconds_to_minutes(EFFORT_DURATION)
    PIECE_RATE = 10

    # Treatments
    INDIVIDUAL = "individual"
    COOPERATION = "cooperation"

    # Stealing game
    STEALING_AMOUNT = 30
    STEALING_LOSS = 45
    STEALING_LOSS_INDIV = int(STEALING_LOSS / PLAYERS_PER_GROUP)
    STEALING_PENALTY = 60
    REPORTING_COST = 10
    REPORTING_REWARD = 45
    AUDIT_PROBABILITY = 2 / 3
    AUDIT_PROBABILITY_STR = "2/3"
    NON_AUDIT_PROBABILITY_STR = "1/3"
    DECISION_TIME = 90  # 1'30
    SOCIETY_OPTION_PAYOFF = 10


    @staticmethod
    def get_parameters():
        return {k: v for k, v in Config.__dict__.items() if
                not k.startswith('__') and not callable(v) and not isinstance(v, staticmethod)}
