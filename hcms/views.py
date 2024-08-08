from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from logging import getLogger
from .models import Appointment, Patient, Doctor
from .serializers import DoctorSerializer, AppointmentSerializer, PatientSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class AppointmentMarkAsCompleted(generics.UpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

logger = getLogger(__name__)
@api_view(['POST'])
def mark_appointment_as_completed(request, pk):
    try:
        logger.warning(f'marking appointment {pk} as completed')
        appointment = Appointment.objects.select_related('doctor', 'patient').get(id=pk)
        appointment.is_completed = True
        appointment.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found!"}, status=status.HTTP_404_NOT_FOUND)