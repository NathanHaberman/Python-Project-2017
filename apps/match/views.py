from django.shortcuts import render, redirect
from ..conversations.models import Conversation
from ..new_users.models import User, Profile, Preference

# Create your views here.
def index(request, page_num):
    logged_in_user = User.objects.get(id=request.session['logged_in_user'])
    logged_in_profile = Profile.objects.get(user=logged_in_user)
    logged_in_preference = Preference.objects.get(user=logged_in_user)


    # Getting thet start and end values for the query
    start = (int(page_num) - 1) * 10
    end = int(page_num) * 10

    # Excluding the same gender as the person logged on and from start to end
    possible_matches = Profile.objects.exclude(sex=logged_in_profile.sex)[start:end]
    
    matches = []

    for person in possible_matches:
        score = 50.0

        # Age matches what they want
        if person.age < logged_in_preference.age_max and person.age > logged_in_preference.age_min:
            score += 12.5
        
        # Age does not match what they want
        else:
            # Check deal breaker
            if logged_in_preference.age_deal_breaker:
                score -= 25
            else:
                score -= 12.5



        # Height in feet matches what they want
        if person.height_feet < logged_in_preference.height_feet_max and person.height_feet > logged_in_preference.height_feet_min:
            score += 12.5

        # Check is their height in feet is equal to the min height they want and see if with inches they are still taller
        elif person.height_feet == logged_in_preference.height_feet_min and person.height_inch >= logged_in_preference.height_inch_min:
            score += 12.5

        # Check is their height in feet is equal to the max height they want and see if with inches they are still shorter
        elif person.height_feet == logged_in_preference.height_feet_max and person.height_inch <= logged_in_preference.height_inch_max:
            score += 12.5

        # If they are outside of the range
        else:
            if logged_in_preference.height_deal_breaker:
                score -= 25
            else:
                score -= 12.5


        # Body type matches what they want
        if person.body_type == logged_in_preference.body_type:
            score += 12.5

        # Body type does not match what they want
        else:
            # Check deal breaker
            if logged_in_preference.body_deal_breaker:
                score -= 25
            else:
                score -12.5



        # Salary range matches what they want
        if person.salary_range == logged_in_preference.salary_range:
            score += 12.5
        
        # Salary range does not match what they want
        else:
            # Check deal breaker
            if logged_in_preference.salary_deal_breaker:
                score -= 25
            else:
                score -= 12.5

        
        # After calculating score
        if score < 0:
            score = 0

        dic = {
            'user' : person.user,
            'score' : score,
        }
        
        # Checking if the user and match have a conversation
        conversation = Conversation.objects.filter(user=logged_in_user).filter(user=person.user)
        if len(conversation) > 0:
            dic['conversation'] = conversation[0]

        matches.append(dic)

        context = {
            'page' : page_num,
            'matches' : matches,
        }

    return render(request, 'match/match.html', context)