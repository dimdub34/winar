from os import environ

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []
USE_POINTS = False
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')
DEMO_PAGE_INTRO_HTML = """ """
SECRET_KEY = '5249757042491'
SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=5.00,
    fill_auto=False,
    test=False
)
DEBUG = True

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'

SESSION_CONFIGS = [
    dict(
        name='whistleblowing_no_reward',
        display_name='Whistleblowing - No Reward',
        app_sequence=[
            'whistleblowing_welcome',
            'whistleblowing_counting', 'whistleblowing_maths', 'whistleblowing_sliders', 'whistleblowing_ios',
            'whistleblowing_transition', 'whistleblowing_game',
            'whistleblowing_questionnaires',
            'whistleblowing_final'
        ],
        num_demo_participants=6,
        real_world_currency_per_point=0.1,
        participation_fee=5.00,
        country="France",
        treatment='cooperation',
        reward=False
    ),
    dict(
        name='whistleblowing_with_reward',
        display_name="Whistleblowing - With Reward",
        app_sequence=[
            'whistleblowing_welcome',
            'whistleblowing_counting', 'whistleblowing_maths', 'whistleblowing_sliders', 'whistleblowing_ios',
            'whistleblowing_transition', 'whistleblowing_game',
            'whistleblowing_questionnaires',
            'whistleblowing_final'
        ],
        num_demo_participants=6,
        real_world_currency_per_point=0.1,
        participation_fee=5.00,
        country="France",
        treatment='cooperation',
        reward=True
    ),
]
