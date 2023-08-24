from django.urls import path
from .views import (
    home_view,
    room_view,
    create_room,
    update_room,
    delete_room,
    login_view,
    logout_view,
    register_view,
    my_rooms_view,
    add_topic_view,
)

app_name = "media"

urlpatterns = [
    path("", home_view, name="home"),
    path("room/<int:pk>/", room_view, name="room"),
    path("create_room/", create_room, name="create_room"),
    path("update_room/<int:pk>/", update_room, name="update_room"),
    path("delete_room/<int:pk>/", delete_room, name="delete_room"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("my_rooms/", my_rooms_view, name="my_rooms"),
    path("add_topic/", add_topic_view, name="add_topic"),
]
