from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.urls import resolve
from django.views.generic import DetailView, FormView, ListView, View

from . import exceptions, forms, models, services
from users.views import AdminOnlyMixin


class UserApplicationList(LoginRequiredMixin, ListView):
    model = models.Application
    template_name = "applications/application_list.html"
    context_object_name = "applications"
    paginate_by = 5


class ApplicationDetail(LoginRequiredMixin, DetailView):
    model = models.Application
    template_name = "applications/application_detail.html"
    context_object_name = "application"


class ApplicationForm(LoginRequiredMixin, FormView):
    template_name = "applications/application_form.html"

    def dispatch(self, request, *args, **kwargs):
        application = services.get_last_user_application(request.user)
        if services.is_application_active(application):
            messages.error(request, "You already have an active application.")
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)


class ApplicationLoan(ApplicationForm):
    form_class = forms.ApplicationForm

    def form_valid(self, form):
        services.create_application_from_form(form, self.request.user)
        return redirect(settings.LOGIN_REDIRECT_URL)


class ApplicationPayment(ApplicationForm):
    form_class = forms.PaymentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.debt == 0:
            messages.warning(request, "You do not have active debt.")
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user: models.User = self.request.user
        if form.cleaned_data['value'] > user.debt:
            messages.error(self.request, "You entered too big value. "
                                         f"Your current debt is {user.debt}.")
            return redirect(resolve(self.request.path_info).url_name)

        services.create_application_from_form(form, user)
        return redirect(settings.LOGIN_REDIRECT_URL)


class ApplicationCancel(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        try:
            services.cancel_application(request.user)
            messages.info(request, "You successfully canceled your application.")
        except exceptions.ApplicationIsNotActive:
            messages.error(request, "You do not have an active application.")
        return redirect(settings.LOGIN_REDIRECT_URL)


class ApplicationActiveList(AdminOnlyMixin, ListView):
    model = models.Application
    template_name = "applications/application_list.html"
    context_object_name = "applications"
    paginate_by = 5

    def get_queryset(self):
        return models.Application.objects.filter(answer_date=None).all()


class ApplicationApprove(AdminOnlyMixin, View):
    @staticmethod
    @transaction.atomic
    def get(request, pk):
        try:
            services.approve_application(pk)
            messages.info(request, f"Application #{pk} was approved.")
        except exceptions.ApplicationIsNotActive:
            messages.error(request, f"Application #{pk} has already been answered.")
        return redirect("application_active_list")


class ApplicationDecline(AdminOnlyMixin, View):
    @staticmethod
    def get(request, pk):
        try:
            services.decline_application(pk)
            messages.warning(request, f"Application #{pk} was declined.")
        except exceptions.ApplicationIsNotActive:
            messages.error(request, f"Application #{pk} has already been answered.")
        return redirect("application_active_list")
