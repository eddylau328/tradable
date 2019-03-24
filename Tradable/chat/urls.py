from django.urls import path, re_path


from chat.views import ThreadView, InboxView

app_name = 'chat'
urlpatterns = [
    path('inbox/', InboxView.as_view(template_name='chat/inbox.html'), name='inbox'),
    re_path(r"^(?P<username>[\w.@+-]+)", ThreadView.as_view()),
]
