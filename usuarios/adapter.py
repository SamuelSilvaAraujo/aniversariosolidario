from django.shortcuts import redirect
from django.utils import timezone
from usuarios.models import Usuario
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email, user_username, user_field
from allauth.utils import valid_email_or_none
from allauth.account.adapter import DefaultAccountAdapter
from allauth.exceptions import ImmediateHttpResponse

from allauth.account.adapter import get_adapter as get_account_adapter


from django.core.urlresolvers import reverse


class UsuarioSocialAccountAdapter(DefaultSocialAccountAdapter):

    def populate_user(self, request, sociallogin, data):
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        name = data.get('name')
        user = sociallogin.user
        user_username(user, username or '')
        user_email(user, valid_email_or_none(email) or '')
        name_parts = (name or '').partition(' ')
        user_field(user, 'nome', '{} {}'.format(first_name or name_parts[0], last_name or name_parts[2]))
        if not user.data_ativacao_email:
            user.data_ativacao_email = timezone.now()
        return user


    def pre_social_login(self, request, sociallogin):
        super(UsuarioSocialAccountAdapter, self).pre_social_login(request, sociallogin)
        if not sociallogin.is_existing:
            try:
                user = Usuario.objects.get(email=sociallogin.user.email)
                sociallogin.connect(request, user)
                raise ImmediateHttpResponse(redirect(reverse('usuarios:index')))
            except Usuario.DoesNotExist:
                pass


class UsuarioAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        return reverse('usuarios:social_login_get_avatar')

    def add_message(self, *args, **kwargs):
        pass