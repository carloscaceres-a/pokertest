from django.conf.urls import include, url

urlpatterns = [
    url(r'^hands_evaluator/', include('apps.hands_evaluator.urls')),
]
