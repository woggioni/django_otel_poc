from django.urls import path, include

from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('doctor', views.DoctorViewSet)
router.register('patient', views.PatientViewSet)
router.register('appointment', views.AppointmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('doctor/', views.DoctorViewSet.as_view(), name='doctor-view'),
    # path('patient/', views.PatientViewSet.as_view(), name='patient-view'),
    # path('appointment/', views.AppointmentViewSet.as_view(), name='appointment-view'),
    path('appointment/<int:pk>/complete', views.mark_appointment_as_completed, name='appointment-mark-completed'),
]