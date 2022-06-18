from otree.api import *
import csv
import logging
from datetime import date
import helpers

c = Currency
doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    NUM_OF_TABLES = 50
    # Dev threshold
    # TASK_THRESHOLD = 0
    # Real threshold
    TASK_THRESHOLD = 5
    COMPREHENSION_QUESTION_BONUS = 0.10

    with open('tables.csv', encoding='utf-8-sig') as table_file:
        TABLES = list(csv.DictReader(table_file))


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    logging.info("Creating intro session")

    # Initializing participant's fields
    for player in subsession.get_players():
        player.participant.exceeded_task_threshold = True
        player.participant.solved_tables_for_ending_module = 0
        player.participant.force_end = False
        player.participant.is_dropout = False
        player.participant.has_reached_main = False

    # Get 50 randomly selected TABLES for the practice round
    subsession.session.vars['tables_practice'],  subsession.session.vars['answers_practice'] = \
        helpers.get_random_tables(C)
    # Get 50 randomly selected TABLES for the real task
    subsession.session.vars['tables_real_task'],  subsession.session.vars['answers_real_task'] = \
        helpers.get_random_tables(C)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    table_0 = models.IntegerField()
    table_1 = models.IntegerField()
    table_2 = models.IntegerField()
    table_3 = models.IntegerField()
    table_4 = models.IntegerField()
    table_5 = models.IntegerField()
    table_6 = models.IntegerField()
    table_7 = models.IntegerField()
    table_8 = models.IntegerField()
    table_9 = models.IntegerField()
    table_10 = models.IntegerField()
    table_11 = models.IntegerField()
    table_12 = models.IntegerField()
    table_13 = models.IntegerField()
    table_14 = models.IntegerField()
    table_15 = models.IntegerField()
    table_16 = models.IntegerField()
    table_17 = models.IntegerField()
    table_18 = models.IntegerField()
    table_19 = models.IntegerField()
    table_20 = models.IntegerField()
    table_21 = models.IntegerField()
    table_22 = models.IntegerField()
    table_23 = models.IntegerField()
    table_24 = models.IntegerField()
    table_25 = models.IntegerField()
    table_26 = models.IntegerField()
    table_27 = models.IntegerField()
    table_28 = models.IntegerField()
    table_29 = models.IntegerField()
    table_30 = models.IntegerField()
    table_31 = models.IntegerField()
    table_32 = models.IntegerField()
    table_33 = models.IntegerField()
    table_34 = models.IntegerField()
    table_35 = models.IntegerField()
    table_36 = models.IntegerField()
    table_37 = models.IntegerField()
    table_38 = models.IntegerField()
    table_39 = models.IntegerField()
    table_40 = models.IntegerField()
    table_41 = models.IntegerField()
    table_42 = models.IntegerField()
    table_43 = models.IntegerField()
    table_44 = models.IntegerField()
    table_45 = models.IntegerField()
    table_46 = models.IntegerField()
    table_47 = models.IntegerField()
    table_48 = models.IntegerField()
    table_49 = models.IntegerField()
    correct_counter = models.IntegerField()
    incorrect_counter = models.IntegerField()
    number_of_consecutive_timeout_pages = models.IntegerField(initial=0)

    question_mobility_across_rounds = models.IntegerField(
        choices=[1, 2, 3],
        widget=widgets.RadioSelect
    )

    question_final_income = models.IntegerField(
        choices=[1, 2, 3, 4],
        widget=widgets.RadioSelect
    )
    question_moving_round = models.IntegerField(
        choices=[1, 2, 3, 4],
        widget=widgets.RadioSelect
    )

    def get_task_results(self, correct_answers):
        submitted_answers = [self.table_0, self.table_1, self.table_2, self.table_3, self.table_4, self.table_5,
                             self.table_6, self.table_7, self.table_8, self.table_9, self.table_10, self.table_11,
                             self.table_12, self.table_13, self.table_14, self.table_15, self.table_16, self.table_17,
                             self.table_18, self.table_19, self.table_20, self.table_21, self.table_22, self.table_23,
                             self.table_24, self.table_25, self.table_26, self.table_27, self.table_28, self.table_29,
                             self.table_30, self.table_31, self.table_32, self.table_33, self.table_34, self.table_35,
                             self.table_36, self.table_37, self.table_38, self.table_39, self.table_40, self.table_41,
                             self.table_42, self.table_43, self.table_44, self.table_45, self.table_46, self.table_47,
                             self.table_48, self.table_49
                             ]
        self.correct_counter = 0
        self.incorrect_counter = 0
        for i in range(len(correct_answers)):
            if submitted_answers[i] == correct_answers[i]:
                self.correct_counter += 1
            else:
                self.incorrect_counter += 1

    def check_comprehension_questions(self, given_answer, correct_answer):
        if given_answer == correct_answer:
            self.payoff += cu(C.COMPREHENSION_QUESTION_BONUS)


# PAGES
class Introduction(Page):
    @staticmethod
    def vars_for_template(player):
        return dict(
            compr_bonus=cu(player.session.config['compr_ques_bonus'])
        )


class Introduction2(Page):
    pass


class InformedConsent(Page):
    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return helpers.dropout_handler_app_after_this_page(player, upcoming_apps)

    @staticmethod
    def vars_for_template(player):
        return dict(
            today=str(date.today())
        )


class IncomeProductionPhase(Page):
    timeout_seconds = 120

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return helpers.dropout_handler_app_after_this_page(player, upcoming_apps)


class PracticeRoundIntro(Page):
    timeout_seconds = 60

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return helpers.dropout_handler_app_after_this_page(player, upcoming_apps)


class PracticeRound(Page):
    timeout_seconds = 30

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.get_task_results(player.session.vars['answers_practice'])
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return helpers.dropout_handler_app_after_this_page(player, upcoming_apps)

    timer_text = "This page will be submitted automatically in:"

    form_model = 'player'
    form_fields = ['table_%s' % i for i in range(C.NUM_OF_TABLES)]

    @staticmethod
    def vars_for_template(player):
        table_image_paths = list()
        for table in player.session.vars['tables_practice']:
            table_image_paths.append('intro/'+table+'.jpg')
        return dict(
            tables_in_round=table_image_paths
        )


class PracticeRoundResults(Page):
    timeout_seconds = 60

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return helpers.dropout_handler_app_after_this_page(player, upcoming_apps)


class RealTaskIntro(Page):
    timeout_seconds = 60

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return helpers.dropout_handler_app_after_this_page(player, upcoming_apps)


class RealTask(Page):
    timeout_seconds = 120

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.get_task_results(player.session.vars['answers_real_task'])
        if player.correct_counter < C.TASK_THRESHOLD:
            player.participant.exceeded_task_threshold = False
            player.participant.solved_tables_for_ending_module = player.correct_counter
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.participant.is_dropout or not player.participant.exceeded_task_threshold:
            return upcoming_apps[-1]

    timer_text = "This page will be submitted automatically in:"

    form_model = 'player'
    form_fields = ['table_%s' % i for i in range(C.NUM_OF_TABLES)]

    @staticmethod
    def vars_for_template(player):
        table_image_paths = list()
        for table in player.session.vars['tables_real_task']:
            table_image_paths.append('intro/'+table+'.jpg')
        return dict(
            tables_in_round=table_image_paths
        )


class TaskResults(Page):
    timeout_seconds = 60

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return helpers.dropout_handler_app_after_this_page(player, upcoming_apps)


class TwoGroups(Page):
    timeout_seconds = 120

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return helpers.dropout_handler_app_after_this_page(player, upcoming_apps)


class GroupingResults(Page):
    timeout_seconds = 70

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return helpers.dropout_handler_app_after_this_page(player, upcoming_apps)


class ActionPoints(Page):
    timeout_seconds = 180

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return helpers.dropout_handler_app_after_this_page(player, upcoming_apps)


class ApUsageExample(Page):
    timeout_seconds = 120

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return helpers.dropout_handler_app_after_this_page(player, upcoming_apps)


class TwelveIndependentRounds(Page):
    timeout_seconds = 180

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return helpers.dropout_handler_app_after_this_page(player, upcoming_apps)


class RedistributingIncomeFirst(Page):
    timeout_seconds = 180

    @staticmethod
    def is_displayed(player: Player):
        return player.session.config['order'] != 'mobility_first'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return helpers.dropout_handler_app_after_this_page(player, upcoming_apps)


class MovingGroupSecond(Page):
    timeout_seconds = 120

    @staticmethod
    def is_displayed(player: Player):
        return player.session.config['order'] != 'mobility_first'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return helpers.dropout_handler_app_after_this_page(player, upcoming_apps)


class MovingGroupFirst(Page):
    timeout_seconds = 120

    @staticmethod
    def is_displayed(player: Player):
        return player.session.config['order'] == 'mobility_first'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return helpers.dropout_handler_app_after_this_page(player, upcoming_apps)


class RedistributingIncomeSecond(Page):
    timeout_seconds = 180

    @staticmethod
    def is_displayed(player: Player):
        return player.session.config['order'] == 'mobility_first'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return helpers.dropout_handler_app_after_this_page(player, upcoming_apps)


class ExchangeApForMoney(Page):
    timeout_seconds = 60

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return helpers.dropout_handler_app_after_this_page(player, upcoming_apps)

    @staticmethod
    def vars_for_template(player):
        return dict(
            example_1_cu=2 * player.session.config['ap_to_money_cu'],
            example_2_cu=player.session.config['ap_to_money_cu'] * player.session.config['initial_action_points']
        )

class QuestionMobilityAcrossRounds(Page):
    timeout_seconds = 120

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        correct_answer = 2
        player.check_comprehension_questions(player.question_mobility_across_rounds, correct_answer)
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return helpers.dropout_handler_app_after_this_page(player, upcoming_apps)

    form_model = 'player'
    form_fields = ['question_mobility_across_rounds']


class QuestionMobilityAcrossRoundsResult(Page):
    timeout_seconds = 60

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return helpers.dropout_handler_app_after_this_page(player, upcoming_apps)

    @staticmethod
    def vars_for_template(player):
        correct_answer = 2
        if player.question_mobility_across_rounds == correct_answer:
            return dict(
                result="correct",
            )
        else:
            return dict(
                result="incorrect",
            )

class QuestionFinalIncome(Page):
    timeout_seconds = 120

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        correct_answer_index = helpers.question_final_income_get_answer_index(player)
        player.check_comprehension_questions(player.question_final_income, correct_answer_index)
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return helpers.dropout_handler_app_after_this_page(player, upcoming_apps)

    form_model = 'player'
    form_fields = ['question_final_income']


class QuestionFinalIncomeResult(Page):
    timeout_seconds = 120

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return helpers.dropout_handler_app_after_this_page(player, upcoming_apps)

    @staticmethod
    def vars_for_template(player):
        correct_answer_index = helpers.question_final_income_get_answer_index(player)
        correct_answer = helpers.question_final_income_get_answer(player)
        if player.question_final_income == correct_answer_index:
            return dict(
                result="correct",
                correct_answer=correct_answer
            )
        else:
            return dict(
                result="incorrect",
                correct_answer=correct_answer
            )


class QuestionMovingRound(Page):
    timeout_seconds = 120

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        correct_answer = 3
        player.check_comprehension_questions(player.question_moving_round, correct_answer)
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return helpers.dropout_handler_app_after_this_page(player, upcoming_apps)

    form_model = 'player'
    form_fields = ['question_moving_round']


class QuestionMovingRoundResult(Page):
    timeout_seconds = 60

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.has_reached_main = True
        helpers.dropout_handler_before_next_page(player, timeout_happened)

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return helpers.dropout_handler_app_after_this_page(player, upcoming_apps)

    @staticmethod
    def vars_for_template(player):
        correct_answer = 3
        if player.question_moving_round == correct_answer:
            return dict(
                result="correct",
            )
        else:
            return dict(
                result="incorrect",
            )


page_sequence = [Introduction, Introduction2, InformedConsent, IncomeProductionPhase, PracticeRoundIntro, PracticeRound,
                 PracticeRoundResults, RealTaskIntro, RealTask, TaskResults, TwoGroups, GroupingResults, ActionPoints,
                 ApUsageExample, TwelveIndependentRounds, RedistributingIncomeFirst, MovingGroupSecond, MovingGroupFirst, RedistributingIncomeSecond, ExchangeApForMoney, QuestionMobilityAcrossRounds, QuestionMobilityAcrossRoundsResult, QuestionFinalIncome, QuestionFinalIncomeResult, QuestionMovingRound, QuestionMovingRoundResult]

