from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.urls import resolve
from django.views.generic import DetailView, FormView, ListView, View

from .forms import ApplicationForm, PaymentForm
from .models import Application
from .services import (approve_application, cancel_application, create_application_from_form,
                       decline_application, get_last_user_application,
                       is_application_active)
from users.views import AdminOnlyView


class UserApplicationListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = "applications/application_list.html"
    context_object_name = "applications"
    paginate_by = 5


class ApplicationDetailView(LoginRequiredMixin, DetailView):
    model = Application
    template_name = "applications/application_detail.html"
    context_object_name = "application"


class ApplicationFormView(LoginRequiredMixin, FormView):
    template_name = "applications/application_form.html"

    def dispatch(self, request, *args, **kwargs):
        application = get_last_user_application(request.user)
        if is_application_active(application):
            messages.error(request, "You already have an active application.")
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)


class ApplicationLoanView(ApplicationFormView):
    form_class = ApplicationForm

    def form_valid(self, form):
        create_application_from_form(form, self.request.user)
        return redirect(settings.LOGIN_REDIRECT_URL)


class ApplicationPaymentView(ApplicationFormView):
    form_class = PaymentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.debt == 0:
            messages.warning(request, "You do not have active debt.")
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        if form.cleaned_data['value'] > user.debt:
            messages.error(self.request, "You entered too big value. "
                                         f"Your current debt is {user.debt}.")
            return redirect(resolve(self.request.path_info).url_name)

        create_application_from_form(form, user)
        return redirect(settings.LOGIN_REDIRECT_URL)


class ApplicationCancelView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        success = cancel_application(request.user)
        if success:
            messages.info(request, "You successfully canceled your application.")
        else:
            messages.error(request, "You do not have an active application.")
        return redirect(settings.LOGIN_REDIRECT_URL)


class ApplicationActiveListView(AdminOnlyView, ListView):
    model = Application
    template_name = "applications/application_list.html"
    context_object_name = "applications"
    paginate_by = 5

    def get_queryset(self):
        return Application.objects.filter(answer_date=None).all()


class ApplicationApproveView(AdminOnlyView, View):
    @staticmethod
    @transaction.atomic
    def get(request, pk):
        success = approve_application(pk)
        if success:
            messages.info(request, f"Application #{pk} was approved.")
        else:
            messages.error(request, f"Application #{pk} has already been answered.")
        return redirect("application_active_list")


class ApplicationDeclineView(AdminOnlyView, View):
    @staticmethod
    def get(request, pk):
        success = decline_application(pk)
        if success:
            messages.warning(request, f"Application #{pk} was declined.")
        else:
            messages.error(request, f"Application #{pk} has already been answered.")
        return redirect("application_active_list")
