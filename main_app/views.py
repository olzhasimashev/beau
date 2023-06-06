from django.shortcuts import render, redirect
from django.views.generic.base import View, TemplateResponseMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .forms import RegistrationForm
from .models import ProcedureCategory, Procedure, ProcedureLimit, Schedule, Record, FavoriteProcedure, Customer
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .forms import CustomUserChangeForm

class RegistrationView(CreateView):
    template_name = 'registration/registration.html'

    def get(self, request, *args, **kwargs):
        registration_form = RegistrationForm()
        return self.render_to_response(
            {'registration_form': registration_form})

    def post(self, request, *args, **kwargs):
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            new_user=registration_form.save(commit=False)
            new_user.set_password(
                registration_form.cleaned_data['password']
            )
            new_user.save()
            authenticate_user = authenticate(
                username=registration_form.cleaned_data['username'],
                password=registration_form.cleaned_data['password']
            )
            login(request, authenticate_user)
            return redirect('main:procedure_category')
        return self.render_to_response(
            {'registration_form': registration_form})


class ProcedureCategoryView(TemplateResponseMixin, View):
    template_name = 'procedure_category.html'

    def get(self, request, *args, **kwargs):
        categories = ProcedureCategory.objects.all()
        return self.render_to_response({
            'categories': categories
            })

class ProcedureListView(TemplateResponseMixin, View):
    template_name = 'procedure_list.html'

    def get(self, request, *args, **kwargs):
        category = self.kwargs.get('category')
        category = ProcedureCategory.objects.get(id=category)
        procedures = Procedure.objects.filter(category=category)
        return self.render_to_response({
            'procedures': procedures, 'category': category
            })

class ProcedureDetailView(TemplateResponseMixin, View):
    template_name = 'procedure_detail.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        procedure = Procedure.objects.get(pk=pk)
        procedure_limit = ProcedureLimit.objects.get(procedure=procedure, user=request.user)
        is_favorite = FavoriteProcedure.objects.filter(user=request.user, procedure=procedure).exists()
        return self.render_to_response({
            'procedure': procedure, 'procedure_limit': procedure_limit, 'is_favorite': is_favorite
            })


class ScheduleView(TemplateResponseMixin, View):
    template_name = 'schedule.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        procedure = Procedure.objects.get(pk=pk)
        schedules = Schedule.objects.filter(procedure=procedure)
        return self.render_to_response({
            'schedules': schedules, 'pk': pk
            })

class MyScheduleView(TemplateResponseMixin, View):
    template_name = 'my_schedule.html'

    def get(self, request, *args, **kwargs):
        records = Record.objects.filter(user=request.user)
        return self.render_to_response({
            'records': records
            })

class RecordSaveView(View):

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user')
        procedure_id = request.POST.get('procedure')
        schedule_id = request.POST.get('schedule')
        procedure = Procedure.objects.get(pk=procedure_id)
        user = User.objects.get(id=user_id)
        schedule = Schedule.objects.get(id=schedule_id)
        Record.objects.create(user=user, schedule=schedule)
        schedule.places_left -= 1
        schedule.save()
        procedure_limit = ProcedureLimit.objects.get(user=user, procedure=procedure)
        procedure_limit.limit -= 1
        procedure_limit.save()
        return redirect('main:my_schedule')

class RecordCancelView(View):

    def post(self, request, *args, **kwargs):
        record_id = self.kwargs.get('pk')
        record = Record.objects.get(pk=record_id)
        record.is_canceled = True
        record.save()
        return redirect('main:my_schedule')

class AddRemoveFavoriteProcedure(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        procedure_id = request.POST.get('procedure_id')
        procedure = get_object_or_404(Procedure, id=procedure_id)
        action = request.POST.get('action')
        if action == 'add':
            if user.is_authenticated:
                FavoriteProcedure.objects.get_or_create(user=user, procedure=procedure)
                return JsonResponse({'status': 'ok'})
            else:
                return JsonResponse({'status': 'error', 'message': 'User is not authenticated'})
        elif action == 'remove':
            try:
                favorite_procedure = FavoriteProcedure.objects.get(user=user, procedure=procedure)
                favorite_procedure.delete()
                return JsonResponse({'status': 'ok'})
            except FavoriteProcedure.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Favorite procedure not found'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid action'})

class ProcedureCategoryFilterView(TemplateResponseMixin, View):
    template_name = 'procedure_category_list.html'

    def get(self, request, *args, **kwargs):
        category_type = request.GET.get('category_type')
        categories = ProcedureCategory.objects.all()
        if category_type:
            categories = ProcedureCategory.objects.filter(category_type=category_type)
            return self.render_to_response({
                'categories': categories
            })
        return self.render_to_response({
            'categories': categories
        })
class SubstructionView(TemplateResponseMixin, View):
    template_name = 'substruction.html'

    def get(self, request, *args, **kwargs):
        substruction = Customer.objects.get(user=request.user)
        duration = substruction.end - substruction.start
        duration_str = duration.days
        return self.render_to_response({
            'substruction': substruction, 'duration_str': duration_str
        })
class ProfileView(TemplateResponseMixin, View):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        favorite_procedures = FavoriteProcedure.objects.filter(user=request.user)
        return self.render_to_response({'favorite_procedures': favorite_procedures
        })



class EditProfileView(LoginRequiredMixin, UpdateView):
    form_class = CustomUserChangeForm
    template_name = 'profile_change.html'
    success_url = reverse_lazy('main:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your profile was updated successfully.')
        return response