from django.urls import path
from . import views

urlpatterns = [
    path("chat/", views.ChatView.as_view(), name="chat-page"),
    path("chat/create/",views.ChatCreateView.as_view(),name="chat-create"),
    path("chat/<uuid:uuid>/", views.ChatDetailView.as_view(), name="chat-detail-page"),
    path("chat/<uuid:uuid>/handle-message", views.ChatMessageView.as_view(), name="handle-message"),
]
