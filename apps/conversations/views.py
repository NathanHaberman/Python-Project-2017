from django.shortcuts import render, redirect
from ..new_users.models import User
from models import Conversation, Message
from django.contrib import messages

# Create your views here.
def inbox(request):
    conversations = Conversation.objects.filter(user=request.session['logged_in_user'])

    context = {
        'conversations' : []
    }

    for convo in conversations:
        users = convo.user.all()

        user = users.exclude(id=request.session['logged_in_user'])
        
        dic = {
            'user' : user[0],
            'conversation_id' : convo.id,
        }

        context['conversations'].append(dic)


    return render(request, 'conversations/conversations.html', context)

def new(request, user_id):
    context = {
        'user' : User.objects.get(id=user_id),
    }
    return render(request, 'conversations/new_conversation.html', context)

def create_conversation(request, user_id):
    if request.method == 'POST':
        errors = Message.objects.validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, error)
            
            return redirect('/messages/new/')
        else:
            # Getting both people involved
            logged_in_user = User.objects.get(id=request.session['logged_in_user'])
            other_user = User.objects.get(id=user_id)

            # Creating the new conversation
            new_convo = Conversation.objects.create()
            # Adding both people to the conversation
            new_convo.user.add(logged_in_user, other_user)

            # Adding first message to conversation
            Message.objects.create(conversation=new_convo, sender=logged_in_user, message=request.POST['message'])

            return redirect('/messages/' + str(new_convo.id) + '/')
    
    else:
        return redirect('/messages/new/' + str(user_id) + '/')



def conversation(request, conversation_id):
    logged_in_user = User.objects.get(id=request.session['logged_in_user'])
    current_conversation = Conversation.objects.get(id=conversation_id)
    user = current_conversation.user.all().exclude(id=logged_in_user.id)

    context = {
        'logged_in_user' : logged_in_user,
        'user' : user[0],
        'conversation' : current_conversation,
        'messages' : Message.objects.filter(conversation=conversation_id),
    }
    return render(request, 'conversations/message.html', context)

def add_message(request, conversation_id):
    if request.method == 'POST':
        errors = Message.objects.validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, error)
        
        else:
            conversation = Conversation.objects.get(id=conversation_id)
            sender = User.objects.get(id=request.session['logged_in_user'])

            Message.objects.create(conversation=conversation, sender=sender, message=request.POST['message'])

    return redirect('/messages/' + str(conversation_id) + '/')