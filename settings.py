from os import environ

SESSION_CONFIGS = [
    dict(
        name='intro',
        num_demo_participants=2,
        app_sequence=['intro'],
    ),
    dict(
        name='main',
        num_demo_participants=4,
        app_sequence=['main', 'ending']
    ),
    dict(
        name='experiment',
        num_demo_participants=8,
        app_sequence=['intro', 'main', 'ending']
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=2.5,
    low_income=1,
    high_income=5,
    ap_to_money_cu=0.05,
    compr_ques_bonus=0.10,
    initial_action_points=10,
    max_cons_timeout_pages=2,
    order='mobility_first',
    efficacy='high',
    mobility='low',
    prolific_completion_url="https://app.prolific.co/submissions/complete?cc=7F39861F",
    doc="<p><b>Study url:</b> After the given url add: ?participant_label"
        "={{%PROLIFIC_PID%}}&STUDY_ID={{%STUDY_ID%}}&SESSION_ID={{%SESSION_ID%}}"
)

ROOMS = [
    dict(
        name='low_mobility_high_efficacy',
        display_name='Room 1: low mobility high efficacy'
    ),
    dict(
        name='low_mobility_low_efficacy',
        display_name='Room 2: low mobility low efficacy'
    ),
    dict(
        name='high_mobility_high_efficacy',
        display_name='Room 3: high mobility high efficacy'
    ),
    dict(
        name='high_mobility_low_efficacy',
        display_name='Room 4: high mobility low efficacy'
    ),
]

PARTICIPANT_FIELDS = ['is_dropout', 'exceeded_task_threshold', 'solved_tables_for_ending_module',
                      'has_restate_consent', 'is_overbooked', 'has_reached_main']
SESSION_FIELDS = ['prolific_completion_url']

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '9809316262073'

INSTALLED_APPS = ['intro', 'main', 'ending']