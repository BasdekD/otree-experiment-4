import helpers
from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'main'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 12
    MAX_AP = 10


class Subsession(BaseSubsession):
    initial_low_income = models.CurrencyField(initial=1)
    initial_high_income = models.CurrencyField(initial=5)
    final_low_income = models.CurrencyField(initial=1)
    final_high_income = models.CurrencyField(initial=5)


def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        for player in subsession.get_players():
            player.participant.exceeded_task_threshold = True
            player.participant.is_dropout = False
            player.participant.has_restate_consent = False
            player.participant.is_overbooked = False
        if subsession.session.config['mobility'] == 'high':
            subsession.session.vars['switching_rounds'] = [1, 10, 11, 12]
        else:
            subsession.session.vars['switching_rounds'] = [1, 11, 12]


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    public_pool_ap = models.IntegerField(
        max=C.MAX_AP,
        min=0
    )

    # The action points that the player decided to keep in order to increase his chances for a positive outcome in case
    # the current round is a switching round (positive = orange goes to blue, blue stays blue)
    personal_account_ap = models.IntegerField(
        max=C.MAX_AP,
        min=0
    )

    exchange_ap = models.IntegerField(
        max=C.MAX_AP,
        min=0
    )
    number_of_consecutive_timeout_pages = models.IntegerField(initial=0)
    timeout_on_contribution = models.BooleanField(initial=False)
    has_switched = models.BooleanField(initial=False)

    question_fair_unfair_inequality = models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )

    question_switching_likeliness = models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )

    question_achieve_raise = models.IntegerField()
    question_action_points_estimation = models.IntegerField()

    question_fair_unfair_conditions = models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )


    question_identify_with_group = models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )

    question_common_goals = models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelectHorizontal
    )

    question_politics = models.IntegerField(
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        widget=widgets.RadioSelectHorizontal,
        blank=True
    )

    question_mobility_probability = models.IntegerField(
        choices=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        widget=widgets.RadioSelectHorizontal
    )

    question_general_comment = models.LongStringField(
        label="Before completing this study, please write any general comment you would like to make about"
              " this study in the box below: ",
        blank=True
    )

    informed_consent = models.BooleanField()


# PAGES
class InitialWaitPage(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    template_name = "_templates/global/main/InitialWaitPage.html"

    @staticmethod
    def after_all_players_arrive(subsession):
        helpers.set_groups(subsession, C)

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.participant.is_overbooked:
            return upcoming_apps[-1]


class SetGroupWaitPage(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number != 1

    @staticmethod
    def after_all_players_arrive(subsession):
        subsession.group_like_round(1)


class IntroScreenRound(Page):
    @staticmethod
    def get_timeout_seconds(player: Player):
        return helpers.get_dropout_timeout(player, 180)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            player.timeout_on_contribution = True
            player.number_of_consecutive_timeout_pages += 1
        else:
            player.number_of_consecutive_timeout_pages = 0
        if player.number_of_consecutive_timeout_pages >= player.session.config['max_cons_timeout_pages']:
            participant.is_dropout = True

    form_model = 'player'
    form_fields = ['public_pool_ap', 'personal_account_ap', 'exchange_ap']

    @staticmethod
    def error_message(player, values):
        print('values is', values)
        if values['public_pool_ap'] + values['personal_account_ap'] + values['exchange_ap'] != player.session.config['initial_action_points']:
            return 'The number of contribution action points, the number of action points used for group switching ' \
                   'and the number of action points exchanged for money, must sum up to your total number of action' \
                   ' points (10).'


class ContributionHandling(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession):
        # Exchange ap for money and update player's payoff
        helpers.convert_exchange_ap_to_income(subsession)
        # Calculate public ap and adjust payrates
        helpers.adjust_payrates(subsession, C)
        # Conduct Switching
        if subsession.round_number in subsession.session.vars['switching_rounds']:
            helpers.switch_groups(subsession)
        # Calculate Incomes
        for player in subsession.get_groups()[0].get_players():
            player.payoff += subsession.final_low_income if not player.has_switched else subsession.final_high_income


class FeedbackIncomeRedistribution(Page):
    @staticmethod
    def get_timeout_seconds(player: Player):
        return helpers.get_dropout_timeout(player, 60)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)


class FeedbackSwitching(Page):
    @staticmethod
    def get_timeout_seconds(player: Player):
        return helpers.get_dropout_timeout(player, 60)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def vars_for_template(player):
        print(player.round_number in player.session.vars['switching_rounds'])
        return dict(
            is_current_round_switching = player.round_number in player.session.vars['switching_rounds']
        )


class FeedbackExchange(Page):
    @staticmethod
    def get_timeout_seconds(player: Player):
        return helpers.get_dropout_timeout(player, 60)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def vars_for_template(player):
        return dict(
            money_from_exchange=cu(player.session.config['ap_to_money_cu'] * player.exchange_ap)
        )


class QuestionFairUnfairInequality(Page):
    @staticmethod
    def get_timeout_seconds(player: Player):
        return helpers.get_dropout_timeout(player, 90)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1 or player.round_number == 10
    form_model = 'player'
    form_fields = ['question_fair_unfair_inequality']


class QuestionSwitchingLikeliness(Page):
    @staticmethod
    def get_timeout_seconds(player: Player):
        return helpers.get_dropout_timeout(player, 90)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1 or player.round_number == 10
    form_model = 'player'
    form_fields = ['question_switching_likeliness']


class QuestionAchieveRaise(Page):
    @staticmethod
    def get_timeout_seconds(player: Player):
        return helpers.get_dropout_timeout(player, 60)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1 or player.round_number == 10
    form_model = 'player'
    form_fields = ['question_achieve_raise']


class QuestionFairUnfairConditions(Page):
    @staticmethod
    def get_timeout_seconds(player: Player):
        return helpers.get_dropout_timeout(player, 90)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1 or player.round_number == 10
    form_model = 'player'
    form_fields = ['question_fair_unfair_conditions']



class QuestionActionPointsEstimation(Page):
    @staticmethod
    def get_timeout_seconds(player: Player):
        return helpers.get_dropout_timeout(player, 90)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1 or player.round_number == 10

    form_model = 'player'
    form_fields = ['question_action_points_estimation']


class QuestionIdentifyWithGroup(Page):
    @staticmethod
    def get_timeout_seconds(player: Player):
        return helpers.get_dropout_timeout(player, 90)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 10

    form_model = 'player'
    form_fields = ['question_identify_with_group']


class QuestionCommonGoals(Page):
    @staticmethod
    def get_timeout_seconds(player: Player):
        return helpers.get_dropout_timeout(player, 90)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 10

    form_model = 'player'
    form_fields = ['question_common_goals']


class QuestionPolitics(Page):
    @staticmethod
    def get_timeout_seconds(player: Player):
        return helpers.get_dropout_timeout(player, 90)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 10

    form_model = 'player'
    form_fields = ['question_politics']


class QuestionMobilityProbability(Page):
    @staticmethod
    def get_timeout_seconds(player: Player):
        return helpers.get_dropout_timeout(player, 90)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 10

    form_model = 'player'
    form_fields = ['question_mobility_probability']


class QuestionGeneralComment(Page):
    @staticmethod
    def get_timeout_seconds(player: Player):
        return helpers.get_dropout_timeout(player, 300)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS

    form_model = 'player'
    form_fields = ['question_general_comment']


class Debriefing(Page):
    @staticmethod
    def get_timeout_seconds(player: Player):
        return helpers.get_dropout_timeout(player, 300)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS


class InformedConsent(Page):
    @staticmethod
    def get_timeout_seconds(player: Player):
        return helpers.get_dropout_timeout(player, 300)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.has_restate_consent = player.informed_consent
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS

    form_model = 'player'
    form_fields = ['informed_consent']


page_sequence = [
      InitialWaitPage, SetGroupWaitPage, IntroScreenRound, ContributionHandling, QuestionFairUnfairInequality, QuestionSwitchingLikeliness, QuestionAchieveRaise, QuestionFairUnfairConditions, QuestionActionPointsEstimation, QuestionIdentifyWithGroup, QuestionCommonGoals, QuestionPolitics, QuestionMobilityProbability, FeedbackIncomeRedistribution, FeedbackSwitching, FeedbackExchange, QuestionGeneralComment, Debriefing, InformedConsent
    ]
