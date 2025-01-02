from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Course, Module, Task, Session, Activity
from .forms import CourseForm,ModuleForm,SessionForm,TaskForm,ActivityForm  # Custom form for Course

class BaseListView(ListView):
    template_name = 'list.html'
    context_object_name = 'objects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = self.model_fields
        field_labels = self.field_labels
        context['fields'] = fields
        context['field_labels'] = [field_labels[field] for field in fields]
        context['data'] = [
            {field: getattr(obj, field) for field in fields}
            for obj in self.get_queryset()
        ]
        context['model_name_plural'] = self.model._meta.verbose_name_plural.title()
        context['create_url'] = f'{self.model_name}_create'
        context['detail_url'] = f'{self.model_name}_detail'
        context['update_url'] = f'{self.model_name}_update'
        context['delete_url'] = f'{self.model_name}_delete'
        return context


class BaseDetailView(DetailView):
    template_name = 'detail.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = self.model_fields
        field_labels = self.field_labels
        context['fields'] = fields
        context['field_labels'] = [field_labels[field] for field in fields]
        context['model_name'] = self.model._meta.verbose_name.title()
        context['update_url'] = f'{self.model_name}_update'
        context['list_url'] = f'{self.model_name}_list'
        return context


class BaseCreateUpdateView(CreateView):
    template_name = 'form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.verbose_name.title()
        context['redirect_url'] = f'{self.model_name}_list'
        return context


class BaseDeleteView(DeleteView):
    template_name = 'confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.verbose_name.title()
        context['redirect_url'] = f'{self.model_name}_list'
        return context

    def get_success_url(self):
        return reverse_lazy(f'{self.model_name}_list')



# Course List View
class CourseListView(BaseListView):
    model = Course
    model_fields = ['course_name', 'course_code', 'entry_qualification', 'course_fee']
    field_labels = {
        'course_name': 'Course Name',
        'course_code': 'Course Code',
        'entry_qualification': 'Entry Qualification',
        'course_fee': 'Fee (USD)',
    }
    model_name = 'course'


# Course Detail View
class CourseDetailView(BaseDetailView):
    model = Course
    model_fields = ['course_name', 'course_code', 'entry_qualification', 'course_fee']
    field_labels = {
        'course_name': 'Course Name',
        'course_code': 'Course Code',
        'entry_qualification': 'Entry Qualification',
        'course_fee': 'Fee (USD)',
    }
    model_name = 'course'


# Course Create View
class CourseCreateView(BaseCreateUpdateView):
    model = Course
    form_class = CourseForm
    success_url = reverse_lazy('course_list')
    model_name = 'course'


# Course Update View
class CourseUpdateView(BaseCreateUpdateView):
    model = Course
    form_class = CourseForm
    success_url = reverse_lazy('course_list')
    model_name = 'course'


# Course Delete View
class CourseDeleteView(BaseDeleteView):
    model = Course
    success_url = reverse_lazy('course_list')
    model_name = 'course'




# Module List View
class ModuleListView(BaseListView):
    model = Module
    model_fields = ['module_name', 'module_code', 'theory_hours', 'practical_hours', 'module_cost', 'module_duration_weeks']
    field_labels = {
        'module_name': 'Module Name',
        'module_code': 'Module Code',
        'theory_hours': 'Theory Hours',
        'practical_hours': 'Practical Hours',
        'module_cost': 'Cost (USD)',
        'module_duration_weeks': 'Duration (Weeks)',
    }
    model_name = 'module'


# Module Detail View
class ModuleDetailView(BaseDetailView):
    model = Module
    model_fields = ['module_name', 'module_code', 'theory_hours', 'practical_hours', 'module_cost', 'module_duration_weeks']
    field_labels = {
        'module_name': 'Module Name',
        'module_code': 'Module Code',
        'theory_hours': 'Theory Hours',
        'practical_hours': 'Practical Hours',
        'module_cost': 'Cost (USD)',
        'module_duration_weeks': 'Duration (Weeks)',
    }
    model_name = 'module'


# Module Create View
class ModuleCreateView(BaseCreateUpdateView):
    model = Module
    form_class = ModuleForm
    success_url = reverse_lazy('module_list')
    model_name = 'module'


# Module Update View
class ModuleUpdateView(BaseCreateUpdateView):
    model = Module
    form_class = ModuleForm
    success_url = reverse_lazy('module_list')
    model_name = 'module'


# Module Delete View
class ModuleDeleteView(BaseDeleteView):
    model = Module
    success_url = reverse_lazy('module_list')
    model_name = 'module'


# Task List View
class TaskListView(BaseListView):
    model = Task
    model_fields = ['task_name', 'task_code', 'theory_hours', 'practical_hours', 'task_cost', 'task_duration_days']
    field_labels = {
        'task_name': 'Task Name',
        'task_code': 'Task Code',
        'theory_hours': 'Theory Hours',
        'practical_hours': 'Practical Hours',
        'task_cost': 'Cost (USD)',
        'task_duration_days': 'Duration (Days)',
    }
    model_name = 'task'


# Task Detail View
class TaskDetailView(BaseDetailView):
    model = Task
    model_fields = ['task_name', 'task_code', 'theory_hours', 'practical_hours', 'task_cost', 'task_duration_days']
    field_labels = {
        'task_name': 'Task Name',
        'task_code': 'Task Code',
        'theory_hours': 'Theory Hours',
        'practical_hours': 'Practical Hours',
        'task_cost': 'Cost (USD)',
        'task_duration_days': 'Duration (Days)',
    }
    model_name = 'task'


# Task Create View
class TaskCreateView(BaseCreateUpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('task_list')
    model_name = 'task'


# Task Update View
class TaskUpdateView(BaseCreateUpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('task_list')
    model_name = 'task'


# Task Delete View
class TaskDeleteView(BaseDeleteView):
    model = Task
    success_url = reverse_lazy('task_list')
    model_name = 'task'


class SessionListView(BaseListView):
    model = Session
    model_fields = ['session_code', 'session_type', 'session_minutes', 'session_cost']
    field_labels = {
        'session_code': 'Session Code',
        'session_type': 'Session Type',
        'session_minutes': 'Duration (Minutes)',
        'session_cost': 'Cost',
    }
    model_name = 'session'


class SessionDetailView(BaseDetailView):
    model = Session
    model_fields = ['session_code', 'session_type', 'session_minutes', 'session_cost']
    field_labels = {
        'session_code': 'Session Code',
        'session_type': 'Session Type',
        'session_minutes': 'Duration (Minutes)',
        'session_cost': 'Cost',
    }
    model_name = 'session'


class SessionCreateView(BaseCreateUpdateView):
    model = Session
    form_class = SessionForm
    success_url = reverse_lazy('session_list')
    model_name = 'session'


class SessionUpdateView(BaseCreateUpdateView):
    model = Session
    form_class = SessionForm
    success_url = reverse_lazy('session_list')
    model_name = 'session'


class SessionDeleteView(BaseDeleteView):
    model = Session
    success_url = reverse_lazy('session_list')
    model_name = 'session'

# Activity List View
class ActivityListView(BaseListView):
    model = Activity
    model_fields = ['activity_name', 'activity_type', 'start_date', 'end_date', 'duration_hours']
    field_labels = {
        'activity_name': 'Activity Name',
        'activity_type': 'Activity Type',
        'start_date': 'Start Date',
        'end_date': 'End Date',
        'duration_hours': 'Duration (Hours)',
    }
    model_name = 'activity'


# Activity Detail View
class ActivityListView(BaseListView):
    model = Activity
    model_fields = ['activity_name', 'activity_code', 'activity_type', 'activity_cost', 'no_of_sessions']
    field_labels = {
        'activity_name': 'Activity Name',
        'activity_code': 'Activity Code',
        'activity_type': 'Type',
        'activity_cost': 'Cost',
        'no_of_sessions': 'No. of Sessions',
    }
    model_name = 'activity'


class ActivityDetailView(BaseDetailView):
    model = Activity
    model_fields = ['activity_name', 'activity_code', 'activity_type', 'activity_cost', 'no_of_sessions']
    field_labels = {
        'activity_name': 'Activity Name',
        'activity_code': 'Activity Code',
        'activity_type': 'Type',
        'activity_cost': 'Cost',
        'no_of_sessions': 'No. of Sessions',
    }
    model_name = 'activity'


class ActivityCreateView(BaseCreateUpdateView):
    model = Activity
    form_class = ActivityForm
    success_url = reverse_lazy('activity_list')
    model_name = 'activity'


class ActivityUpdateView(BaseCreateUpdateView):
    model = Activity
    form_class = ActivityForm
    success_url = reverse_lazy('activity_list')
    model_name = 'activity'


class ActivityDeleteView(BaseDeleteView):
    model = Activity
    success_url = reverse_lazy('activity_list')
    model_name = 'activity'
