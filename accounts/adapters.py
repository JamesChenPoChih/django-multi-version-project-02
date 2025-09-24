from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect
from login.models import UserProfile

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just before a social user is logged in.
        We override this to handle both existing and new users,
        bypassing the default allauth flow to integrate with our custom user system.
        """
        # The sociallogin object contains user data from the social provider.
        user_email = sociallogin.user.email
        if not user_email:
            # If for some reason we don't get an email, we can't proceed.
            # You might want to handle this case more gracefully.
            return

        try:
            # Case 1: An existing user is logging in.
            profile = UserProfile.objects.get(email=user_email)
            print(f"[MySocialAccountAdapter] Existing user found: {profile.email}")
            # Log them in using our custom session logic.
            request.session['loginFlag'] = True
            request.session['username'] = profile.username

        except UserProfile.DoesNotExist:
            # Case 2: A new user is signing up.
            print(f"[MySocialAccountAdapter] New user. Creating profile for: {user_email}")
            # Use the full name from the social account, or the email as a fallback.
            username = sociallogin.user.get_full_name() or user_email
            # Create a new UserProfile instance for the new user.
            new_profile = UserProfile.objects.create(
                email=user_email,
                username=username
            )
            # Log the new user in using our custom session logic.
            request.session['loginFlag'] = True
            request.session['username'] = new_profile.username

        # In both cases, we have handled the login manually.
        # We raise ImmediateHttpResponse to stop allauth's default processing
        # and redirect the user to the homepage.
        print("[MySocialAccountAdapter] Login handled. Redirecting to /")
        raise ImmediateHttpResponse(redirect('/'))
