from django.apps import AppConfig


class HandsEvaluatorConfig(AppConfig):
    name = 'hands_evaluator'

    DEALER_SERVICE_END_POINT = 'http://dealer.internal.comparaonline.com:8080'
    DEALER_SERVICE_MAX_TRIES = 3
    HANDS_NUMBER_PER_DEAL = 2
    CARD_AMOUNT_PER_HAND = 5
