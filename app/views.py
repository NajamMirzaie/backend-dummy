from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Patient
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from django.http import JsonResponse
import json
from django.core.paginator import Paginator
from django.views import View
from django.core.serializers import serialize
from django.db.models import Q
from django.db.models import Count, Avg
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import update_session_auth_hash
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()


class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        
        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            # The authentication was successful
            login(request, user)  # Log the user in
            # Specify the redirect URL in the response
            return Response({
                "message": "Login successful",
                "redirect": "/dashboard"  # Specify the URL to redirect to
            }, status=status.HTTP_200_OK)
        else:
            # Authentication failed
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth import update_session_auth_hash
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ChangePasswordView(APIView):
  def post(self, request, *args, **kwargs):
    user = request.user
    old_password = request.data.get("oldPassword")
    new_password = request.data.get("newPassword")

    if not request.user.is_authenticated:
      return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
      if user.check_password(old_password):
        user.set_password(new_password)
        user.save()  # Save the updated user object with the new password
        update_session_auth_hash(request, user)
        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
      else:
        return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
      # Handle any unexpected exceptions during password change
      return Response({"error": "An error occurred during password change"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class PredictorAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        
        try:
            age = int(data.get('age'))
            gender = data.get('gender')  # Ensure 'MALE' or 'FEMALE' are correctly handled
            # Assuming the client sends direct integer values for these fields
            total_cholesterol = int(data.get('total_cholesterol'))
            hdl_cholesterol = int(data.get('hdl_cholesterol'))
            blood_pressure = int(data.get('blood_pressure'))
            is_smoker = data.get('is_smoker')  # 'YES' or 'NO'

            # print all data
            # print(f"Age: {age}")
            # print(f"Gender: {gender}")
            # print(f"Total Cholesterol: {total_cholesterol}")
            
            # Risk calculation logic placeholder
            points, risk = self.calculate_risk(age, gender, total_cholesterol, hdl_cholesterol, blood_pressure, is_smoker)

            result = {'score': points, 'risk': risk}

            #Convert risk% to float
            risk = float(risk.replace('%', ''))

            # print (f"Risk: {risk}")
            #Create and save the Patient instance
            patient = Patient(
                age=age,
                gender=gender,
                total_cholesterol=total_cholesterol,
                hdl_cholesterol=hdl_cholesterol,
                blood_pressure=blood_pressure,
                is_smoker=is_smoker,
                risk = risk
            )

            # patient = Patient(gender="Female", age=25, total_cholesterol=200, hdl_cholesterol=50, blood_pressure=120, is_smoker="No", risk=5)

            patient.full_clean()
            patient.save()

            return Response(result, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({"error": "Invalid input data"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def calculate_risk(self, age, gender, total_cholesterol, hdl_cholesterol, blood_pressure, is_smoker):
        # Placeholder for your complex risk calculation logic
        # This function should return the calculated points and risk category based on inputs
        points = 0  # Example calculation result
        risk = 0  # This should be determined based on the calculated points

        age_ranges = {
                'Female' : {
                    (20, 34): -7,
                    (35, 39): -3,
                    (40, 44): 0,
                    (45, 49): 3,
                    (50, 54): 6,
                    (55, 59): 8,
                    (60, 64): 10,
                    (65, 69): 12,
                    (70, 74): 14,
                    (75, 79): 16
                    },

                'Male' : {
                    (20, 34): -9,
                    (35, 39): -4,
                    (40, 44): 0,
                    (45, 49): 3,
                    (50, 54): 6,
                    (55, 59): 8,
                    (60, 64): 10,
                    (65, 69): 11,
                    (70, 74): 12,
                    (75, 79): 13
                }
            }

        if gender in age_ranges:
            for age_range, point_value in age_ranges[gender].items():
                if age >= age_range[0] and age <= age_range[1]:
                    points += point_value
                    break

        cholesterol_ranges = {
            'Female': {
                (20, 39): {160: 0, 200: 4, 240: 7, 280: 9},
                (40, 49): {160: 0, 200: 3, 240: 5, 280: 6},
                (50, 59): {160: 0, 200: 2, 240: 3, 280: 4},
                (60, 69): {160: 0, 200: 1, 240: 1, 280: 2},
                (70, 79): {160: 0, 200: 0, 240: 0, 280: 1},
            },
            'Male': {
                (20, 39): {160: 0, 200: 4, 240: 8, 280: 11},
                (40, 49): {160: 0, 200: 3, 240: 6, 280: 8},
                (50, 59): {160: 0, 200: 2, 240: 4, 280: 5},
                (60, 69): {160: 0, 200: 1, 240: 2, 280: 3},
                (70, 79): {160: 0, 200: 1, 240: 1, 280: 2},
            }
        }

        if gender in cholesterol_ranges:
            for age_range, cholesterol_points in cholesterol_ranges[gender].items():
                if age >= age_range[0] and age <= age_range[1]:
                    for cholesterol_threshold, point_value in cholesterol_points.items():
                        if total_cholesterol == cholesterol_threshold:
                            points = point_value
                            break
        
        if hdl_cholesterol < 40:
            points += 2
        elif hdl_cholesterol >= 40 and hdl_cholesterol <= 49:
            points += 1
        elif hdl_cholesterol >= 50 and hdl_cholesterol <= 59:
            points += 0
        elif hdl_cholesterol >= 60:
            points += -1
            
        bp_ranges = {
            'Female': {
                (0, 119): 0,
                (120, 129): 1,
                (130, 139): 2,
                (140, 159): 3,
                (160, float('inf')): 4
            },
            'Male': {
                (0, 119): 0,
                (120, 129): 1,
                (130, 139): 2,
                (140, 159): 3,
                (160, float('inf')): 4
            }
        }

        for range, point in bp_ranges[gender].items():
            if range[0] <= blood_pressure <= range[1]:
                points += point
                break

        smoking_ranges = {
            'Female': {
                (20, 39): 9,
                (40, 49): 7,
                (50, 59): 4,
                (60, 69): 2,
                (70, 80): 1
            },
            'Male': {
                (20, 39): 8,
                (40, 49): 5,
                (50, 59): 3,
                (60, 69): 1,
                (70, 80): 1
            }
        }
            
        if is_smoker == "YES":
            if gender in smoking_ranges:
                for smoking_range, point in smoking_ranges[gender].items():
                    if smoking_range[0] <= age <= smoking_range[1]:
                        points += point
                        break
            
        risk_ranges = {
            'Female': {
                (0, 8): '<1%',
                (9, 12): '1%',
                (13, 14): '2%',
                (15, 15): '3%',
                (16, 16): '4%',
                (17, 17): '5%',
                (18, 18): '6%',
                (19, 19): '8%',
                (20, 20): '11%',
                (21, 21): '14%',
                (22, 22): '17%',
                (23, 23): '22%',
                (24, 24): '27%',
                (25, float('inf')): 'Over 30%'
            },
            'Male': {
                (0, 0): '<1%',
                (1, 4): '1%',
                (5, 6): '2%',
                (7, 7): '3%',
                (8, 8): '4%',
                (9, 9): '5%',
                (10, 10): '6%',
                (11, 11): '8%',
                (12, 12): '10%',
                (13, 13): '12%',
                (14, 14): '16%',
                (15, 15): '20%',
                (16, 16): '25%',
                (17, float('inf')): 'Over 30%'
            }
        }

        if gender in risk_ranges:
            for risk_range, result in risk_ranges[gender].items():
                if risk_range[0] <= points <= risk_range[1]:
                    risk = result
        
        print(f"Your Framingham Risk Score is: {points}.")
        print(f"Your estimated 10-year risk of developing CVD is: {risk}.")

        return [points, risk]
    
# @method_decorator(login_required, name='dispatch')
class PatientsAPIView(View):
    def get(self, request, *args, **kwargs):
        patients = Patient.objects.all()

        # Optional: Implement Pagination
        # page_size = request.GET.get('pageSize', 10)
        # paginator = Paginator(patients, page_size)
        # page_number = request.GET.get('page')
        # page_obj = paginator.get_page(page_number)
        
        patients_data = [{
            'id': patient.id,
            'age': patient.age,
            'gender': patient.gender,
            'hdl_cholesterol': patient.hdl_cholesterol,
            'total_cholesterol': patient.total_cholesterol,
            'blood_pressure': patient.blood_pressure,
            'is_smoker': patient.is_smoker,  # Assuming is_smoker is a method
            'risk': patient.risk,
            'date': patient.date
        } for patient in patients]

        # Serialize the queryset
        # data = serialize('json', patients, fields=('age', 'gender', 'hdl_cholesterol', 'total_cholesterol', 'blood_pressure', 'is_smoker'))

        # print(data)

        return JsonResponse({'patients': patients_data}, safe=False)
    
@method_decorator(csrf_exempt, name='dispatch')
# @method_decorator(login_required, name='dispatch')
class DeletePatientsAPIView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            ids = data.get('ids', [])
            # Delete the patients with the given ids
            Patient.objects.filter(id__in=ids).delete()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

# @method_decorator(login_required, name='dispatch')
class PatientStatsAPIView(View):
    def get(self, request, *args, **kwargs):
        patients = Patient.objects.all()
        now = datetime.now()
        start_of_year = datetime(now.year, 1, 1)

        # Initialize the extended response data structure
        response_data = {
            'total_patients': patients.count(),
            'gender_count': {
                'male': patients.filter(gender='Male').count(),
                'female': patients.filter(gender='Female').count(),
            },
            'average_age_by_gender': {},
            'smokers_percentage_by_gender': { 'male_smokers': patients.filter(gender='Male').filter(is_smoker='Yes').count(),
                                              'male_non_smokers': patients.filter(gender='Male').filter(is_smoker='No').count(),
                                              'female_smokers': patients.filter(gender='Female').filter(is_smoker='Yes').count(),
                                              'female_non_smokers': patients.filter(gender='Female').filter(is_smoker='No').count(),},
            'records_last_7_days_by_gender': {},
            'records_this_year_by_gender': {},
            'average_risk_score_by_gender': list(patients.values('gender').annotate(avg_risk=Avg('risk'))),
            'average_cholesterol_by_gender': {},
            'average_hdl_cholesterol_by_gender': {},
            'average_blood_pressure_by_gender': {},
            'risk_distribution_by_age_gender': {},

            # Add overall averages here
            'overall_average_age': patients.aggregate(Avg('age'))['age__avg'] or 0,
            'overall_average_total_cholesterol': patients.aggregate(Avg('total_cholesterol'))['total_cholesterol__avg'] or 0,
            'overall_average_hdl_cholesterol': patients.aggregate(Avg('hdl_cholesterol'))['hdl_cholesterol__avg'] or 0,
            'overall_average_blood_pressure': patients.aggregate(Avg('blood_pressure'))['blood_pressure__avg'] or 0,
        }

        for gender in ['Male', 'Female']:
            gender_patients = patients.filter(gender=gender)

            # Calculations split by gender
            response_data['average_age_by_gender'][gender] = gender_patients.aggregate(Avg('age'))['age__avg'] or 0
            # response_data['average_age_by_gender']['avg'] = patients.aggregate(Avg('age'))['age__avg'] or 0
            total_gender_patients = gender_patients.count()
            smokers_count = gender_patients.filter(is_smoker='Yes').count()
            response_data['smokers_percentage_by_gender'][gender] = (smokers_count / total_gender_patients * 100) if total_gender_patients else 0
            response_data['records_last_7_days_by_gender'][gender] = gender_patients.filter(date__gte=now - timedelta(days=7)).count()
            response_data['records_this_year_by_gender'][gender] = gender_patients.filter(date__gte=start_of_year).count()

            # Cholesterol and blood pressure
            response_data['average_cholesterol_by_gender'][gender] = gender_patients.aggregate(Avg('total_cholesterol'))['total_cholesterol__avg'] or 0
            # response_data['average_cholesterol_by_gender']['avg'] = patients.aggregate(Avg('total_cholesterol'))['total_cholesterol__avg'] or 0

            response_data['average_hdl_cholesterol_by_gender'][gender] = gender_patients.aggregate(Avg('hdl_cholesterol'))['hdl_cholesterol__avg'] or 0
            # response_data['average_hdl_cholesterol_by_gender']['avg'] = patients.aggregate(Avg('hdl_cholesterol'))['hdl_cholesterol__avg'] or 0

            response_data['average_blood_pressure_by_gender'][gender] = gender_patients.aggregate(Avg('blood_pressure'))['blood_pressure__avg'] or 0
            # response_data['average_blood_pressure_by_gender']['avg'] = patients.aggregate(Avg('blood_pressure'))['blood_pressure__avg'] or 0

        # Risk distribution by age group and gender
        age_ranges = [(20, 40), (41, 60), (61, 80)]
        for start_age, end_age in age_ranges:
            age_range_key = f"{start_age}-{end_age}"
            for gender in ['Male', 'Female']:
                avg_risk = patients.filter(age__gte=start_age, age__lte=end_age, gender=gender).aggregate(avg_risk=Avg('risk'))['avg_risk'] or 0
                response_data['risk_distribution_by_age_gender'].setdefault(age_range_key, {})[gender] = avg_risk

        return JsonResponse(response_data, status=200)
