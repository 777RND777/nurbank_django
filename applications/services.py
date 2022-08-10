from typing import Callable

from django.utils import timezone

from .forms import ApplicationForm
from .models import Application, User


def create_application_from_form(form: ApplicationForm, user: User) -> None:
    application = form.save(commit=False)
    application.user = user
    application.save()


def is_application_active(application: Application):
    return application and application.answer_date is None


def get_last_user_application(user: User):
    return user.applications.first()


def cancel_application(user: User) -> bool:
    application = get_last_user_application(user)
    if not is_application_active(application):
        return False

    application.answer_date = timezone.now()
    application.save()
    return True


def check_if_application_is_active(func: Callable[[Application], None]) -> Callable[[int], bool]:
    def inner(application_id: int) -> bool:
        application = Application.objects.get(pk=application_id)
        if not is_application_active(application):
            return False

        func(application)
        return True

    return inner


@check_if_application_is_active
def approve_application(application: Application) -> None:
    application.answer_date = timezone.now()
    application.approved = True
    application.save()

    user = application.user
    user.debt += application.value
    user.save()


@check_if_application_is_active
def decline_application(application: Application) -> None:
    application.answer_date = timezone.now()
    application.save()
