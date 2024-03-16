from django.urls import path
from .views import AvailableRoomsView, RoomCreateView, RoomListView, RoomRetrieveUpdateDestroyView, ReservationRoomView

urlpatterns = [
    path("avaliablerooms/", AvailableRoomsView.as_view(), name="available_rooms"),
    path("bookroom/", ReservationRoomView.as_view(), name="book_room"),
    path("listrooms/", RoomListView.as_view(), name="room_list"),
    path("addroom/", RoomCreateView.as_view(), name="add_room"),
    path("room/<int:pk>/", RoomRetrieveUpdateDestroyView.as_view(), name="room_detail"),
    
]