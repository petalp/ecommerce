from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.decorators import login_required
from .tokens import account_activation_token
from .forms import RegistrationForm, UserEditForm
from .models import Userbase
from order.views import user_orders

@login_required
def dashboard(request):
    orders = user_orders(request)
    context = {'orders': orders}
    return render(request, 'account/user/dashboard.html',context)

@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
        
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, 'account/user/edit_details.html', {'user_form':user_form})

@login_required
def delete_user(request):
    user = Userbase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')


def account_register(request):
    # if request.user.is_authenticated:
    #     return redirect('/')
    
    if request.method == 'POST':
        registerform = RegistrationForm(request.POST)
        if registerform.is_valid():
            user = registerform.save(commit=False)
            user.email = registerform.cleaned_data['email']
            user.set_password(registerform.cleaned_data['password'])
            user.is_active = False
            user.save()

            #setup email
            current_site = get_current_site(request)
            subject = "Activate your Account"
            message = render_to_string('account/registration/account_activation_email.html', {
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })

            user.email_user(subject=subject, message=message)
            return HttpResponse('registered successfully and activation sent')
    else:
        registerform = RegistrationForm()
    return render(request,'account/registration/register.html', {'form':registerform})

def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Userbase.objects.get(pk=uid)
    except:
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')