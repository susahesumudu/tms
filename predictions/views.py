from django.shortcuts import render

# Create your views here.
import joblib
from django.shortcuts import render
from django.http import JsonResponse

import os
model_path = os.path.join(os.path.dirname(__file__), 'Decision_Tree_vocational_model.pkl')
model = joblib.load(model_path)



def predict_grade(request):
    prediction = None  # Initialize prediction variable
    if request.method == 'POST':
        try:
            # Extract input values from the form
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
            prediction = model.predict(input_data)
            prediction = "Pass" if prediction[0] == 1 else "Fail"

        except Exception as e:
            prediction = f"Error: {str(e)}"

    return render(request, 'predict.html', {'prediction': prediction})
