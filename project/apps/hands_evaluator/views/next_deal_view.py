from django.views.generic import TemplateView
from django.shortcuts import render
from apps.hands_evaluator.models import Deck
from apps.hands_evaluator.exceptions import StateError
from apps.hands_evaluator.exceptions import WrongTokenError
from apps.hands_evaluator.exceptions import NotEnoughCardsError


class NextDealView(TemplateView):

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        try:
            deck = self._get_current_deck(request)
            ranked_hands = deck.get_next_hands()
            context['ranked_hands'] = ranked_hands

        except StateError as exception:
            context['message'] = 'You must start a new game'
            return render(request, 'restart.html', context=context)

        except WrongTokenError as exception:
            context['message'] = 'Dealer had just loose our deck'
            return render(request, 'restart.html', context=context)

        except NotEnoughCardsError as exception:
            context['message'] = 'Not enough cards left in deck'
            return render(request, 'restart.html', context=context)

        except Exception as exception:
            context['message'] = exception
            import traceback
            traceback.print_exc()
            return render(request, 'oops.html', context=context)

        return render(request, 'result.html', context=context)

    def _get_current_deck(self, request):
        deck_token = None

        if 'deck_token' in request.session:
            deck_token = request.session['deck_token']

        if deck_token is None:
            raise StateError('No deck available')

        print('current token' + '[' + deck_token + ']')

        deck = Deck(token=deck_token)
        return deck
