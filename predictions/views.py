from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Prediction
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.core.mail import send_mail  # Import send_mail
from django.conf import settings
import logging
import joblib
import os
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User


from channels.layers import get_channel_layer

# Initialize logger
logger = logging.getLogger(__name__)

# Load the ML model
model_path = os.path.join(os.path.dirname(__file__), 'best_random_forest_model.pkl')
model = joblib.load(model_path)

class PredictForRowView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # Get the specific Prediction object
        prediction = get_object_or_404(Prediction, pk=pk)

        # Prepare input data from the Prediction object
        input_data = [[
            prediction.assessment_score,
            prediction.industry_training_experience,
            prediction.average_time_per_task,
            prediction.completed_no_activity,
            prediction.total_task_completed,
            prediction.self_efficacy_score,
            prediction.practicals_hrs,
            prediction.theory_hrs,
        ]]

        # Make the prediction
        try:
            result = model.predict(input_data)
            prediction.predicted_grade = "Pass" if result[0] == 1 else "Fail"
            prediction.save()


            # Notify via WebSocket
            # Notify WebSocket clients via Redis
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "notifications",
                {
                    "type": "send_notification",
                    "message": f"Prediction made for student {prediction.student.username}: {prediction.predicted_grade}"
                }
            )


           
        except Exception as e:
            logger.error(f"Prediction failed for Prediction ID {pk}: {e}")
            return JsonResponse({'error': f"Prediction error: {e}"})

        # Redirect back to the predictions list
        return redirect('predictions:prediction_list')


class SendEmailNotificationView(LoginRequiredMixin, View):
    def get(self, request, pk):
        # Initialize progress
        progress = 0

        # Get the specific Prediction object
        try:
            prediction = get_object_or_404(Prediction, pk=pk)
            progress = 10
        except Exception as e:
            logger.error(f"Error retrieving prediction with ID {pk}: {e}")
          

        # Ensure the student has an email
        student_email = prediction.student.email
        if not student_email:
            progress = 50
         

        # Try sending the email
        if prediction.predicted_grade=="Pass":
            sub = "Congratulations on Your Academic Progress!"
            msg = f"""Dear {prediction.student.first_name},

Congratulations! Your predicted final grade is PASS. Keep up the great work and continue staying focused.

For more details, please log in to the student portal.
Best regards,
Your School Team"""

        else:
            sub = "Important Update on Your Academic Performance"
            msg = f"""Dear {prediction.student.first_name},

Our analysis indicates that you are at risk of failing your final assessment. Don’t worry—there’s still time to improve!

We recommend reviewing the feedback and improvement steps provided in your portal. Please log in promptly to take action and get back on track.

Best regards,
Your Training Team
"""

        try:


            progress = 70
            send_mail(
                subject=sub,
                message=msg,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[student_email],
                fail_silently=False,
            )
            progress = 100
            logger.info(f"Email sent successfully to student: {student_email}")
     
        except Exception as email_error:
            logger.error(f"Failed to send email to student: {student_email}. Error: {email_error}")
            progress = 80
            

        # Fallback redirect
        return redirect('predictions:prediction_list')


class PredictGradeView(LoginRequiredMixin,View):
    template_name = 'predict.html'

    def get(self, request):
        # Pass a list of students to the template for selection
        students = User.objects.all()
        return render(request, self.template_name, {'prediction': None, 'students': students})

    def post(self, request):
        prediction = None
        try:
            # Extract student and input values from the form
            student_id = request.POST['student']
            student = User.objects.get(id=student_id)  # Get the selected student

            data = {
                'assessment_score': float(request.POST['assessment_score']),
                'Industry_Training_Experience': float(request.POST['Industry_Training_Experience']),
                'Average_Time_Per_Task': float(request.POST['Average_Time_Per_Task']),
                'Completed_No_Activity': float(request.POST['Completed_No_Activity']),
                'Total_Task_Completed': float(request.POST['Total_Task_Completed']),
                'Self_Efficacy_Score': float(request.POST['Self_Efficacy_Score']),
                'Practicals_hrs': float(request.POST['Practicals_hrs']),
                'Theory_hrs': float(request.POST['Theory_hrs']),
            }

            # Prepare data for prediction
            input_data = [[
                data['assessment_score'],
                data['Industry_Training_Experience'],
                data['Average_Time_Per_Task'],
                data['Completed_No_Activity'],
                data['Total_Task_Completed'],
                data['Self_Efficacy_Score'],
                data['Practicals_hrs'],
                data['Theory_hrs']
            ]]

            # Predict the final grade
            prediction_result = model.predict(input_data)
            prediction = "Pass" if prediction_result[0] == 1 else "Fail"

            # Save the prediction in the database
            Prediction.objects.create(
                student=student,  # Use the selected student
                predicted_by=request.user,  # The teacher making the prediction
                assessment_score=data['assessment_score'],
                industry_training_experience=data['Industry_Training_Experience'],
                average_time_per_task=data['Average_Time_Per_Task'],
                completed_no_activity=data['Completed_No_Activity'],
                total_task_completed=data['Total_Task_Completed'],
                self_efficacy_score=data['Self_Efficacy_Score'],
                practicals_hrs=data['Practicals_hrs'],
                theory_hrs=data['Theory_hrs'],
                predicted_grade=prediction,
            )

        except Exception as e:
            prediction = f"Error: {str(e)}"

        # Pass the list of students back to the template
        students = User.objects.all()
        return redirect('predictions:prediction_list')



from django.views.generic import ListView,DetailView
from .models import Prediction  # Import your Prediction model

class PredictionListView(LoginRequiredMixin,ListView):
    model = Prediction
    template_name = 'prediction_list.html'
    context_object_name = 'predictions'

class PredictionDetailView(LoginRequiredMixin,DetailView):
    model = Prediction
    template_name = 'prediction_detail.html'  # Specify your detail view template
    context_object_name = 'prediction'  # Use this name in the template to refer to the object

