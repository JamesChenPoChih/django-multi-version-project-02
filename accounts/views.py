from django.shortcuts import render

# Create your views here.


from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('/')