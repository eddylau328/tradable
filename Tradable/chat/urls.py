from django.urls import path, re_path


from chat.views import ThreadView, InboxView

app_name = 'chat'
urlpatterns = [
    path("inbox/", InboxView.as_view(), name='inbox'),
    re_path(r"^(?P<username>[\w.@+-]+)", ThreadView.as_view()),
]
