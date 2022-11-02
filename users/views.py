from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import DetailView, FormView, ListView, View

from . import forms, models


class Home(View):
    @staticmethod
    def get(request):
        return render(request, "users/home.html")


class GuestOnlyMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)


class LogIn(GuestOnlyMixin, FormView):
    form_class = forms.LogInForm
    template_name = "users/log_in.html"

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        request = self.request

        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

        login(request, form.user_cache)

        return redirect(settings.LOGIN_REDIRECT_URL)


class Register(GuestOnlyMixin, FormView):
    template_name = "users/register.html"
    form_class = forms.RegisterForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()

        login(self.request, user)

        return redirect(settings.LOGIN_REDIRECT_URL)


class LogOut(LoginRequiredMixin, LogoutView):
    pass


class AdminOnlyMixin(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)


class UserDetail(LoginRequiredMixin, DetailView):
    model = models.User
    template_name = "users/user_detail.html"
    context_object_name = "user_info"


class UserList(AdminOnlyMixin, ListView):
    model = models.User
    template_name = "users/user_list.html"
    context_object_name = "users"
    paginate_by = 5
