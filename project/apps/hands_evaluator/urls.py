from django.conf.urls import url
from apps.hands_evaluator.views import StartDealView
from apps.hands_evaluator.views import NextDealView

urlpatterns = [
    url(r'^deals/start/$', StartDealView.as_view()),
    url(r'^deals/next/$', NextDealView.as_view()),
]
