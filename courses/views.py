from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

from django.apps import apps

from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin

class BaseListView(LoginRequiredMixin, ListView):
    context_object_name = 'items'

    def get_queryset(self):
        try:
            model = apps.get_model(app_label=self.kwargs['app_name'], model_name=self.kwargs['model'])
            return model.objects.all()
        except LookupError:
            raise Http404("Model not found")

    def get_template_names(self):
        return [f"{self.kwargs['app_name']}/{self.kwargs['model'].lower()}_list.html"]


class BaseDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'item'

    def get_object(self):
        try:
            model = apps.get_model(app_label=self.kwargs['app_name'], model_name=self.kwargs['model'])
            return model.objects.get(pk=self.kwargs['pk'])
        except (LookupError, model.DoesNotExist):
            raise Http404("Object not found")

    def get_template_names(self):
        return [f"{self.kwargs['app_name']}/{self.kwargs['model'].lower()}_detail.html"]


class BaseCreateView(LoginRequiredMixin, CreateView):
    fields = '__all__'

    def get_queryset(self):
        try:
            model = apps.get_model(app_label=self.kwargs['app_name'], model_name=self.kwargs['model'])
            return model.objects.all()
        except LookupError:
            raise Http404("Model not found")

    def get_template_names(self):
        return [f"{self.kwargs['app_name']}/{self.kwargs['model'].lower()}_form.html"]

    def get_success_url(self):
        return reverse_lazy(f"{self.kwargs['app_name']}:{self.kwargs['model'].lower()}_list")


class BaseUpdateView(LoginRequiredMixin, UpdateView):
    fields = '__all__'

    def get_object(self):
        try:
            model = apps.get_model(app_label=self.kwargs['app_name'], model_name=self.kwargs['model'])
            return model.objects.get(pk=self.kwargs['pk'])
        except (LookupError, model.DoesNotExist):
            raise Http404("Object not found")

    def get_template_names(self):
        return [f"{self.kwargs['app_name']}/{self.kwargs['model'].lower()}_form.html"]

    def get_success_url(self):
        return reverse_lazy(f"{self.kwargs['app_name']}:{self.kwargs['model'].lower()}_list")


class BaseDeleteView(LoginRequiredMixin, DeleteView):

    def get_object(self):
        try:
            model = apps.get_model(app_label=self.kwargs['app_name'], model_name=self.kwargs['model'])
            return model.objects.get(pk=self.kwargs['pk'])
        except (LookupError, model.DoesNotExist):
            raise Http404("Object not found")

    def get_template_names(self):
        return [f"{self.kwargs['app_name']}/{self.kwargs['model'].lower()}_confirm_delete.html"]

    def get_success_url(self):
        return reverse_lazy(f"{self.kwargs['app_name']}:{self.kwargs['model'].lower()}_list")
