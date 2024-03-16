from datetime import datetime
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Room, Reservation
from .serializers import RoomSerializer, ReservationSerializer

class AvailableRoomsView(generics.ListAPIView):
    serializer_class= RoomSerializer
    
    def get_queryset(self):
        start_date_str= self.request.query_params.get('start_date')
        end_date_str= self.request.query_params.get('end_date')
        attendees= self.request.query_params.get('attendees')
        
        
        if not start_date_str or not end_date_str or not attendees:
            raise ValidationError({"message": "Invalid input"})
        
        try:
            start_date= datetime.strptime(start_date_str, '%Y-%m-%d %H:%M')
            end_date= datetime.strptime(end_date_str, '%Y-%m-%d %H:%M')
            attendees = int(attendees)
        except ValueError:
            raise ValidationError({"message": "Invalid date format"})
        
        if start_date < datetime.now():
            raise ValidationError({"message": "Invalid start date"})
        
        if start_date > end_date:
            raise ValidationError({"message": "Invalid date range"})
        
        
        rooms= Room.objects.filter(max_occupancy__gte=attendees)
        reservations= Reservation.objects.filter(
            start_time__lt=end_date, 
            end_time__gt=start_date
        )
        reserved_room_ids= reservations.values_list('room_id', flat=True)
        
        return rooms.exclude(id__in=reserved_room_ids)
    
class RoomListView(generics.ListAPIView):
    queryset= Room.objects.all()
    serializer_class= RoomSerializer

class RoomCreateView(generics.CreateAPIView):
    serializer_class= RoomSerializer
    
class RoomRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset= Room.objects.all()
    serializer_class= RoomSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Room deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class ReservationRoomView(generics.CreateAPIView):
    queryset= Reservation.objects.all()
    serializer_class= ReservationSerializer
    def perform_create(self, serializer):
        room_id= self.request.data.get('room')
        try:
            room= Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            raise ValidationError({"message": "Room does not exist"})
        
        start_date_str= self.request.data.get('start_time')
        end_date_str= self.request.data.get('end_time')
        attendees= self.request.data.get('attendees')
        try:
            start_date= datetime.strptime(start_date_str, '%Y-%m-%d %H:%M')
            end_date= datetime.strptime(end_date_str, '%Y-%m-%d %H:%M')
        except ValueError:
            raise ValidationError({"message": "Invalid date format"})
        
        if start_date < datetime.now():
            raise ValidationError({"message": "Invalid start date"})
        
        if start_date > end_date:
            raise ValidationError({"message": "Invalid date range"})
        
        
        if int(attendees) > room.max_occupancy:
            raise ValidationError({"message": "Room is not big enough for the given number of attendees"})
        
        # Check if the room is available for the given time
        overlapping_reservations = Reservation.objects.filter(
            room=room,
            start_time__lt=end_date,
            end_time__gt=start_date
        )
        
        if overlapping_reservations.exists():
            raise ValidationError({"message": "Room is not available for the given time"})
        
        reservation= Reservation(room=room, start_time=start_date, end_time=end_date, attendees=attendees)
        reservation.save()
    
        
  
        