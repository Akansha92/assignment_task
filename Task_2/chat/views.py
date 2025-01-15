from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Message
from django.contrib.auth.models import User

# Signup View
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'chat/signup.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login after logout

# Chat View (for all users and individual user chat)
@login_required
def chat_view(request, username=None):
    users = User.objects.exclude(id=request.user.id)  # Exclude the logged-in user
    selected_user = None
    messages = []

    if username:
        selected_user = get_object_or_404(User, username=username)
        # Fetch messages exchanged between the logged-in user and the selected user
        messages = Message.objects.filter(
            sender__in=[request.user, selected_user],
            recipient__in=[request.user, selected_user]
        ).order_by('timestamp')  # Ensure messages are ordered by timestamp

    return render(request, 'chat/chat.html', {
        'users': users,
        'selected_user': selected_user,
        'messages': messages,
    })

# Send Message View
@login_required
def send_message(request, username):
    if request.method == 'POST':
        recipient = get_object_or_404(User, username=username)
        message_content = request.POST.get('message')

        if message_content.strip():
            Message.objects.create(sender=request.user, recipient=recipient, content=message_content)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/chat/'))  # Go back to previous page or /chat/

# Login View
def login_view(request):
    # If the user is already authenticated, redirect to chat page
    if request.user.is_authenticated:
        return redirect('chat')  # Redirect to chat if already logged in

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate the user and log them in
            user = form.get_user()
            login(request, user)

            # Get the 'next' URL from the GET parameters (if any)
            next_url = request.GET.get('next')

            # If there's no 'next' URL, redirect to the chat page
            if next_url:
                return redirect(next_url)  # Redirect to the requested next page
            else:
                return redirect('chat')  # Default redirect to chat page
    else:
        form = AuthenticationForm()

    return render(request, 'chat/login.html', {'form': form})
