from django.conf.urls.static import static
from django.urls import path

from ask_markov import settings
from ask.views import *

app_name = "home"

urlpatterns = [
    path("", IndexPageView.as_view(), name="index"),
    path("hot/", HotQuestionsPageView.as_view(), name="hot"),
    path("question/35/", QuestionPageView.as_view(), name="question"),
    path("ask/", AskPageView.as_view(), name="ask"),
    path("signup/", RegisterPageView.as_view(), name="register"),
    path("login/", LoginPageView.as_view(), name="login"),
    path("logout/", LogoutPageView.as_view(), name="logout"),
    path("settings/", SettingsPageView.as_view(), name="settings"),
    path("tag/blablabla/", TagPageView.as_view(), name="tag"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
