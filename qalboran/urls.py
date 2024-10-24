from django.conf.urls.static import static
from django.urls import path

from TechParkBMSTU_1sem import settings
from qalboran.views import IndexPageView, QuestionPageView, AskPageView

app_name = "home"

urlpatterns = [
    path("", IndexPageView.as_view(), name="index"),
    path("question/123/", QuestionPageView.as_view(), name="question"),
    path("ask/", AskPageView.as_view(), name="ask"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
