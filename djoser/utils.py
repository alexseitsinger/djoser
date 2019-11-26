import shortuuid
from django.contrib.auth import login, logout, user_logged_in, user_logged_out
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from djoser.conf import settings


def get_user_id_field(user):
    return getattr(user, settings.USER_ID_FIELD, getattr(user, "pk", None))


def get_user_id_field_kwargs(user):
    name = settings.USER_ID_FIELD
    value = get_user_id_field(user)
    return {name: value}


def get_user_id_field_random(user):
    uid = get_user_id_field(user)
    if isinstance(uid, int):
        return uid + 1
    return shortuuid.uuid()


def encode_uid(pk):
    return force_text(urlsafe_base64_encode(force_bytes(pk)))


def decode_uid(pk):
    return force_text(urlsafe_base64_decode(pk))


def login_user(request, user):
    token, _ = settings.TOKEN_MODEL.objects.get_or_create(user=user)
    if settings.CREATE_SESSION_ON_LOGIN:
        login(request, user)
    user_logged_in.send(sender=user.__class__, request=request, user=user)
    return token


def logout_user(request):
    if settings.TOKEN_MODEL:
        settings.TOKEN_MODEL.objects.filter(user=request.user).delete()
        user_logged_out.send(
            sender=request.user.__class__, request=request, user=request.user
        )
    if settings.CREATE_SESSION_ON_LOGIN:
        logout(request)


class ActionViewMixin(object):
    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self._action(serializer)
