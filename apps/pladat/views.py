from django.shortcuts import render

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login

from .forms import RegistrationForm

from django.contrib.auth.models import User
from .models import PladatUser

def main_page_view(request):
    ctx = {}

    if request.user.is_authenticated:
        ctx = {'user': request.user}

    return render(request, 'main_page.html', context=ctx)


def register_user(data):
    # Add a PladatUser
    user_dct = {
        'username': data['email'],
        'email' : data['email'],
        'password': data['password'],
    }
    user = User.objects.create_user(**user_dct)
    user.save()

    fields = ['first_name', 'last_name', 'phone_number', 'address', 'city', 'state', 'country', 'user_type']
    pladatuser_dct = {key: data[key] for key in fields}
    pladatuser_dct['user'] = user

    pladatuser = PladatUser.objects.create(**pladatuser_dct)
    pladatuser.save()

    if data['user_type'] == PladatUser.UserType.STUDENT:
        fields = ['degree', 'major', 'university', 'number_of_previous_work_experience', 'years_worked', 'is_currently_employed', 'skills_text']
        student_dct = {key: data[key] for key in fields}
        student_dct['pladatuser'] = pladatuser

        student = Student.objects.create(**student_dct)
        student.save()
        
    elif data['user_type'] == PladatUser.UserType.COMPANY:
        recruiter = Recruiter.objects.create(pladatuser = pladatuser)
        recruiter.save()

    return True


def registration_view(request):
    ctx = {}
    
    if request.user.is_authenticated:
        # This happens when an logged in user visits the register page
        # We might consider redirecting here instead
        return HttpResponse('Already a registered user')

    if request.method == 'GET':
        # Unregistered user trying to access the registration form
        registration_form = RegistrationForm()
        ctx['form'] = registration_form
        return render(request, 'user_register.html', context = ctx)

    elif request.method == 'POST':
        # Form filled and submitted
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            email = registration_form.data['email']
            if User.objects.filter(email = email).exists():
                # Email already in use
                registration_form.add_error('email', 'Email is already in use')
                ctx['form'] = registration_form
                return render(request, 'user_register.html', context = ctx)
            else:
                register_user(registration_form.data)
                return HttpResponse('Registered successfuly')
        else:
            # Something wrong with form
            ctx['form'] = registration_form
            return render(request, 'user_register.html', context = ctx)
    
    return HttpResponseForbidden()