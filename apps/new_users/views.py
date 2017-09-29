from django.shortcuts import render, redirect
from django.contrib import messages
from models import User, Profile, Preference

import bcrypt


def index(request):
    return render(request, 'new_users/index.html')



def register(request):
    if request.method == 'POST':
        
        # Checking if there are errors from models
        errors = User.objects.validator(request.POST)
        if len(errors) > 0:
            for error in errors:
                messages.error(request, error)
            return redirect('/')
        
        else:
            # Encrypting Password
            password = request.POST['password']
            password = password.encode('utf8')
            hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

            # Adding user
            User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], username=request.POST['username'], email=request.POST['email'], password=hashed_pw)

            # Logging in person
            user = User.objects.get(email = request.POST['email'])
            request.session['logged_in_user'] = user.id
            
            # Creating empty Profile and Preference
            Profile.objects.create(user=user)
            Preference.objects.create(user=user)




            # Set Home Page
            return redirect('/users/profile/')

    else:
        return redirect('/')



def login(request):
    # Checking if there is a matching email
    user_in_db = User.objects.filter(email = request.POST['email'])
    
    if user_in_db:
        
        # Now checking if password matched the encrypted one in the database
        if bcrypt.checkpw(request.POST['password'].encode('utf8'), user_in_db[0].password.encode('utf8')):
            request.session['logged_in_user'] = user_in_db[0].id
            



            # Set Home Page
            return redirect('/users/' + str(request.session['logged_in_user']) + '/')

        else:
            # Error if passwords don't match
            messages.error(request, 'Password is incorrect')
            return redirect('/')
    
    else:
        # If email is not in database
        messages.error(request, 'Email is incorrect')
        return redirect('/')


# Logout the logged in user
def logout(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')


# Render a user profile page
def user_page(request, user_id):
    user = User.objects.get(id=user_id)
    user_profile = Profile.objects.get(user=user)
    user_preference = Preference.objects.get(user=user)

    body_type = {
        1 : 'Slim',
        2 : 'Average',
        3 : 'Heavyset',
    }

    salary_range = {
        1 : 'Less than $25,000',
        2 : '$25,000 - $40,000',
        3 : '$40,000 - $60,000',
        4 : '$60,000 - $80,000',
        5 : '$80,000 - $100,000',
        6 : '$100,000+',
    }

    context = {
        'user' : user,
        'profile' : user_profile,
        'preference' : user_preference,
        'profile_body_type' : body_type[user_profile.body_type],
        'profile_salary_range' : salary_range[user_profile.salary_range],
        'preference_body_type' : body_type[user_preference.body_type],
        'preference_salary_range' : salary_range[user_preference.salary_range],
    }

    return render(request, 'new_users/user_page.html', context)


# Render a page to update user profile info
def profile(request):
    context = {
        'user' : User.objects.get(id=request.session['logged_in_user']),
    }
    return render(request, 'new_users/profile_update.html', context)


# Submit update of user profile info
def profile_update(request):
    if request.method == "POST":
        user = Profile.objects.get(user=request.session['logged_in_user'])
        user.desc = request.POST['desc']
        user.sex = request.POST['sex']
        user.age = request.POST['age']
        user.height_feet = request.POST['height_feet']
        user.height_inch = request.POST['height_inch']
        user.body_type = request.POST['body_type']
        user.salary_range = request.POST['salary_range']

        user.save()

    return redirect('/users/preference/')


# Render a page to update user preferences
def preference(request):
    context = {
        'user' : User.objects.get(id=request.session['logged_in_user']),
    }
    return render(request, 'new_users/preference_update.html', context)


# Submit update to user prefereneces
def preference_update(request):
    if request.method == "POST":
        user = Preference.objects.get(user=request.session['logged_in_user'])

        user.age_min = request.POST['age_min']
        user.age_max = request.POST['age_max']

        user.height_feet_min = request.POST['height_feet_min']
        user.height_inch_min = request.POST['height_inch_min']
        user.height_feet_max = request.POST['height_feet_max']
        user.height_inch_max = request.POST['height_inch_max']

        user.body_type = request.POST['body_type']

        user.salary_range = request.POST['salary_range']

        user.save()

    return redirect('/users/' + str(request.session['logged_in_user']) + '/')