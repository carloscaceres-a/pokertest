from django.views.generic import TemplateView
from apps.hands_evaluator.models import Deck
from django.shortcuts import render


class StartDealView(TemplateView):

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        try:
            self._get_new_deck(request)

        except Exception as exception:
            context['message'] = exception
            return render(request, 'oops.html', context=context)

        return render(request, 'start.html', context=context)

    def _get_new_deck(self, request):
        if 'deck_token' in request.session:
            del request.session['deck_token']

        deck = Deck()
        request.session['deck_token'] = deck.token
