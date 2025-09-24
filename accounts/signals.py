from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Member
from .models import generate_readable_id
from allauth.account.signals import user_logged_in
from allauth.socialaccount.models import SocialAccount
from django.dispatch import receiver
from django.apps import AppConfig

@receiver(pre_save, sender=Member)
def generate_unique_id(sender, instance, **kwargs):
    if not instance.unique_id:
        instance.unique_id = generate_readable_id()


@receiver(user_logged_in)
def populate_session_after_login(request, user, **kwargs):
    # Google 登入時會有 SocialAccount
    try:
        social_account = SocialAccount.objects.get(user=user)
        name = social_account.extra_data.get('name') or user.username
    except SocialAccount.DoesNotExist:
        name = user.username  # fallback: 一般登入或無 social data

    request.session['loginFlag'] = True
    request.session['username'] = name


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        import accounts.signals  # 確保啟用 signals