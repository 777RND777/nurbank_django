from typing import Callable

from django.utils import timezone

from . import exceptions, forms, models


def create_application_from_form(form: forms.ApplicationForm, user: models.User) -> None:
    application = form.save(commit=False)
    application.user = user
    application.save()


def is_application_active(application: models.Application):
    return application and application.answer_date is None


def get_last_user_application(user: models.User):
    return user.applications.first()


def cancel_application(user: models.User) -> None:
    application = get_last_user_application(user)
    if not is_application_active(application):
        raise exceptions.ApplicationIsNotActive

    application.answer_date = timezone.now()
    application.save()


def check_if_application_is_active(func: Callable[[models.Application], None]) -> Callable[[int], None]:
    def inner(application_id: int) -> None:
        application = models.Application.objects.get(pk=application_id)
        if not is_application_active(application):
            raise exceptions.ApplicationIsNotActive

        func(application)

    return inner


@check_if_application_is_active
def approve_application(application: models.Application) -> None:
    application.answer_date = timezone.now()
    application.approved = True
    application.save()

    user = application.user
    user.debt += application.value
    user.save()


@check_if_application_is_active
def decline_application(application: models.Application) -> None:
    application.answer_date = timezone.now()
    application.save()
