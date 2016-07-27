from datetime import datetime

from django.shortcuts import redirect
from django.utils import timezone
from usuarios.models import Usuario
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email, user_username, user_field
from allauth.utils import valid_email_or_none
from allauth.account.adapter import DefaultAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.core.urlresolvers import reverse


class UsuarioSocialAccountAdapter(DefaultSocialAccountAdapter):

    def populate_user(self, request, sociallogin, data):
        user = sociallogin.user
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        if sociallogin.account.provider == 'twitter':
            email = '{}@twitter.com'.format(username)
        else:
            email = data.get('email')
            birthday = sociallogin.account.extra_data.get('birthday')
            if birthday:
                user_field(user, 'data_de_nascimento', '{}'.format(datetime.strptime(birthday, '%m/%d/%Y').strftime('%Y-%m-%d')))
        name = data.get('name')
        user_username(user, username or '')
        user_email(user, valid_email_or_none(email) or '')
        name_parts = (name or '').partition(' ')
        first_name = first_name or name_parts[0]
        last_name = last_name or name_parts[2]
        user_field(user, 'nome', u'{} {}'.decode('utf-8').format(first_name, last_name))
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