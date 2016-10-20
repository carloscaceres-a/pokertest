from django.apps import apps as django_apps
from apps.hands_evaluator.exceptions import WrongTokenError
from apps.hands_evaluator.exceptions import NotEnoughCardsError
from apps.hands_evaluator.exceptions import DealerServiceError
import requests
import json


class DealerService(object):
    config = django_apps.get_app_config('hands_evaluator')

    @classmethod
    def get_cards_from_deck(
            cls,
            deck_token,
            cards_amount=config.CARD_AMOUNT_PER_HAND):
        for try_number in range(0, cls.config.DEALER_SERVICE_MAX_TRIES):
            try:
                cards_from_deck = cls._get_cards_from_service(
                    deck_token, cards_amount)
                return cards_from_deck
            except DealerServiceError as exception:
                if (try_number + 1) == cls.config.DEALER_SERVICE_MAX_TRIES:
                    raise exception

                continue

    @classmethod
    def get_deck_token(cls):
        for try_number in range(0, cls.config.DEALER_SERVICE_MAX_TRIES):
            try:
                token = cls._get_deck_token_from_service()
                return token

            except DealerServiceError as exception:
                if (try_number + 1) == cls.config.DEALER_SERVICE_MAX_TRIES:
                    raise exception

                continue

    @classmethod
    def _get_deck_token_from_service(cls):
        try:
            request = requests.post('{}/deck'.format(cls._get_end_point()))
        except Exception as exception:
            raise DealerServiceError('Unknown error. Error was: {}'.format(exception.message))

        status_code = 200
        status_message = None
        response = None
        if request.status_code != 200:
            response = json.loads(request.text)
            if 'statusCode' in response:
                status_code = response['statusCode']
                status_message = response['message']
        else:
            response = request.text

        if status_code == 200:
            return response
        else:
            raise DealerServiceError('Cannot get new deck. Error was: {}'.format(status_message))

    @classmethod
    def _get_cards_from_service(
            cls,
            deck_token,
            cards_amount):

        try:
            request = requests.get('{}/deck/{}/deal/{}'.format(
                cls._get_end_point(),
                deck_token,
                cards_amount))

            response = json.loads(request.text)

        except Exception as exception:
            raise DealerServiceError('Unknown error. Error was: {}'.format(exception.message))

        status_code = 200
        status_message = None
        if 'statusCode' in response:
            status_code = response['statusCode']
            status_message = response['message']

        if status_code == 200:
            return response

        elif status_code == 404:
            raise WrongTokenError(status_message)

        elif status_code == 405:
            raise NotEnoughCardsError(status_message)

        else:
            raise DealerServiceError('Cannot get hand of cards. Error was: {}'.format(status_message))

    @classmethod
    def _get_end_point(cls):
        config = django_apps.get_app_config('hands_evaluator')
        return config.DEALER_SERVICE_END_POINT
