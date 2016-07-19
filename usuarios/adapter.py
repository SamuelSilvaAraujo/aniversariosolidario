from django.utils import timezone
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email, user_username, user_field
from allauth.utils import valid_email_or_none

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