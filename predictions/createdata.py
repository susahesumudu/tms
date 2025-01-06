# Creating mock datasets for calculating metrics based on the merged data
student_vle_mock = pd.DataFrame({
    'id_student': ['S001', 'S001', 'S002', 'S002'],
    'date': [7, 14, 7, 14],
    'id_site': ['R001', 'R002', 'R001', 'R002'],
    'sum_click': [15, 20, 10, 5]
})

student_assessment_mock = pd.DataFrame({
    'id_student': ['S001', 'S002'],
    'id_assessment': ['A001', 'A002'],
    'date_submitted': [10, 20],
    'date': [9, 19]
})

# Weekly Login Frequency
student_vle_mock['week'] = student_vle_mock['date'] // 7
login_frequency = student_vle_mock.groupby(['id_student', 'week']).size().reset_index(name='login_count')

# Resource Access Frequency
resource_access_frequency = student_vle_mock.groupby('id_student')['id_site'].count().reset_index(name='resource_access_count')

# Total Clicks per Student
total_clicks = student_vle_mock.groupby('id_student')['sum_click'].sum().reset_index(name='total_clicks')

# Engagement Consistency: Standard deviation of weekly clicks per student
weekly_clicks = student_vle_mock.groupby(['id_student', 'week'])['sum_click'].sum().reset_index()
engagement_consistency = weekly_clicks.groupby('id_student')['sum_click'].std().reset_index(name='clicks_std_dev')

# Days of Inactivity: Count weeks with zero clicks
inactive_weeks = weekly_clicks.groupby('id_student')['sum_click'].apply(lambda x: (x == 0).sum()).reset_index(name='inactive_weeks')

# Resource Diversity (Unique Resources Accessed)
resource_diversity = student_vle_mock.groupby('id_student')['id_site'].nunique().reset_index(name='unique_resources')

# Resource Completion Rate
total_resources = student_vle_mock['id_site'].nunique()
student_completions = student_vle_mock.groupby('id_student')['id_site'].nunique().reset_index(name='resources_accessed')
student_completions['completion_rate'] = student_completions['resources_accessed'] / total_resources

# Assignment Completion Rate
assignment_completion_rate = student_assessment_mock.groupby('id_student')['id_assessment'].nunique().reset_index(name='assignments_completed')

# Merge all metrics into one dataset
final_dataset = students_df[['student_id', 'name']].rename(columns={'student_id': 'id_student'})
final_dataset = final_dataset.merge(login_frequency.groupby('id_student').sum().reset_index(), on='id_student', how='left')
final_dataset = final_dataset.merge(resource_access_frequency, on='id_student', how='left')
final_dataset = final_dataset.merge(total_clicks, on='id_student', how='left')
final_dataset = final_dataset.merge(engagement_consistency, on='id_student', how='left')
final_dataset = final_dataset.merge(inactive_weeks, on='id_student', how='left')
final_dataset = final_dataset.merge(resource_diversity, on='id_student', how='left')
final_dataset = final_dataset.merge(student_completions[['id_student', 'completion_rate']], on='id_student', how='left')
final_dataset = final_dataset.merge(assignment_completion_rate, on='id_student', how='left')

# Fill missing values with 0
final_dataset.fillna(0, inplace=True)

# Save the final dataset to a CSV file
final_dataset.to_csv("/mnt/data/final_student_metrics.csv", index=False)

tools.display_dataframe_to_user(name="Final Dataset with Student Metrics", dataframe=final_dataset)
