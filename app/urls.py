from django.urls import path
from .views import PredictorAPIView, LoginAPIView, PatientsAPIView, DeletePatientsAPIView, PatientStatsAPIView, ChangePasswordView

urlpatterns = [
    path('predictor', PredictorAPIView.as_view(), name='predictor'),
    path('login', LoginAPIView.as_view(), name = 'login'),
    path('patients', PatientsAPIView.as_view(), name='patients'),
    path('delete_patients', DeletePatientsAPIView.as_view(), name='delete_patients'),
    path('patient_stats', PatientStatsAPIView.as_view(), name='patient_stats'),
    path('change_password', ChangePasswordView.as_view(), name='change_password'),
]
